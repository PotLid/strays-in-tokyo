from server import MyTCPHandler
from backend.userHandling import retrieveAuthenticationCookieId, authenticatedUser, retrieveProfilePicture
import random
import json
import hashlib
import base64

# <<<<<<< Updated upstream
# #
# def handleWebSocket(TCP: MyTCPHandler, data):

#     # Implement the handshake of the WebSocket protocol at the path “/websocket”.
#     # Upgrade the TCP socket to a WebSocket connection.

#     websocket_key = data[b'Sec-WebSocket-Key']
#     websocket_key += b'258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

#     # compute the SHA1 hash and Base64 encoding.
#     hashed_key = hashlib.sha1(websocket_key).digest()
#     hash_to_base64 = base64.b64encode(hashed_key)

#     # Create a response to upgrade the TCP socket to a WebSocket connection
#     handshake_response = b'HTTP/1.1 101 Switching Protocols\r\nConnection: Upgrade\r\nUpgrade: websocket\r\nSec-WebSocket-Accept: ' + hash_to_base64 + b'\r\n\r\n'

#     TCP.request.sendall(handshake_response)

#     # This while statement will listen to the messages sent over by the user.
#     while True:
#         recieved_data = TCP.request.recv(1024)


'''
    Web sockets are received and sent in the following framework.

    0                   1                   2                   3
      0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
     +-+-+-+-+-------+-+-------------+-------------------------------+
     |F|R|R|R| opcode|M| Payload len |    Extended payload length    |
     |I|S|S|S|  (4)  |A|     (7)     |             (16/64)           |
     |N|V|V|V|       |S|             |   (if payload len==126/127)   |
     | |1|2|3|       |K|             |                               |
     +-+-+-+-+-------+-+-------------+ - - - - - - - - - - - - - - - +
     |     Extended payload length continued, if payload len == 127  |
     + - - - - - - - - - - - - - - - +-------------------------------+
     |                               |Masking-key, if MASK set to 1  |
     +-------------------------------+-------------------------------+
     | Masking-key (continued)       |          Payload Data         |
     +-------------------------------- - - - - - - - - - - - - - - - +
     :                     Payload Data continued ...                :
     + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
     |                     Payload Data continued ...                |
     +---------------------------------------------------------------+

    This websocket handler parses the payload (message) sent by a client
    and sends to the payload (message) to other active clients.
'''

def handleWebSocket(TCP: MyTCPHandler, username):

    data = b''

    while True:
        received_data = TCP.request.recv(1024)

        i = 0
        # FIN, 2 RSV's
        first_int = int(received_data[i])
        opcode = first_int & 15
        if opcode == 8:
            # delete socket connection
            json_message = {'messageType':'user_disconnect','username':username}

            message_as_bytes = json.dumps(json_message).encode()
            webframe = convert_webframe(TCP, message_as_bytes)

            for client in TCP.websocket_connections:
                if client['socket'] != TCP:
                    client['socket'].request.sendall(webframe)

            profile_picture = retrieveProfilePicture(username).decode()
            MyTCPHandler.websocket_connections.remove({'username':username, 'socket':TCP, 'profile_picture': profile_picture})
            break

        i += 1

        mask = int(received_data[i]) & 128
        payload_length = int(received_data[i]) & 127

        if payload_length == 126:
            new_payload = 0
            for x in range(0,2):
                i += 1
                new_payload = (new_payload << 8) | received_data[i]
            payload_length = new_payload
        elif payload_length == 127:
            new_payload = 0
            for x in range(0,8):
                i += 1
                new_payload = (new_payload << 8) | received_data[i]
            payload_length = new_payload

        data += received_data

        if payload_length > 1024:
            buffer_length = payload_length
            buffer_length -= 1024

            while buffer_length > 0:
                received_data = TCP.request.recv(1024)
                buffer_length -= 1024
                data += received_data

        masking_key = []

        if mask == 128:
            for x in range(0,4):
                i += 1
                masking_key.append(data[i])

        buffer_data_length = payload_length
        payload_data = b''

        while buffer_data_length >= 4:
            for x in range(0,4):
                i += 1
                payload_data += (data[i] ^ masking_key[x]).to_bytes(1, "big")
            buffer_data_length -= 4

        if buffer_data_length != 0:
            for x in range(0, buffer_data_length):
                i += 1
                payload_data += (data[i] ^ masking_key[x]).to_bytes(1, "big")
            buffer_data_length -= 4

#         payload_data = payload_data
        payload_data = TCP.escape_html(payload_data)

        payload_data = payload_data.decode("utf-8")

        payload_as_json = json.loads(payload_data)



        if payload_as_json['messageType'] == 'user_to_server':
            timeID = payload_as_json['id']
            json_message = {'messageType': 'server_to_user', 'sender': username, 'id': timeID, 'comment': payload_as_json['comment'] }

            # create message for database storage
            db_message = {'sender': username, 'receiver': None, 'messageType': 'user_to_server','id': timeID, 'comment': payload_as_json['comment'], 'totalLike':0}
            TCP.chatCollection.insert_one(db_message)

            message_as_bytes = json.dumps(json_message).encode()
            webframe = convert_webframe(TCP, message_as_bytes)

            for client in TCP.websocket_connections:
                client['socket'].request.sendall(webframe)

        elif payload_as_json['messageType'] == 'like':
            timeID = payload_as_json['id']
            # updates postInfo DB element ({'id': unique_time_stamp, 'sender': username, 'comment': comment,  'likes': 0 (int)}) with incremented like count
            # (returns element with updated likes without '_id' attribute if needed)
            updatedElem = TCP.chatCollection.find_one_and_update({'id' : timeID}, {'$inc' : {'totalLike': 1}}, {'_id' : False}, new = True)
            # parse return Frame
            json_message = {'messageType': 'like_update', 'id': timeID, 'totalLike': updatedElem['totalLike']}

            message_as_bytes = json.dumps(json_message).encode()
            webframe = convert_webframe(TCP, message_as_bytes)

            for client in TCP.websocket_connections:
                client['socket'].request.sendall(webframe)
        elif payload_as_json['messageType'] == 'dislike':
            timeID = payload_as_json['id']
            # updates postInfo DB element with decremented like count
            # (returns element with updated likes without '_id' attribute if needed)
            updatedElem = TCP.chatCollection.find_one_and_update({'id' : timeID}, {'$inc' : {'totalLike': -1}}, {'_id' : False}, new = True)
            # parse return Frame
            json_message = {'messageType': 'like_update', 'id': timeID, 'totalLike': updatedElem['totalLike']}

            message_as_bytes = json.dumps(json_message).encode()
            webframe = convert_webframe(TCP, message_as_bytes)

            for client in TCP.websocket_connections:
                client['socket'].request.sendall(webframe)
        elif payload_as_json['messageType'] == 'dm':
            timeID = payload_as_json['id']
            sender = payload_as_json['sender']
            receiver = payload_as_json['receiver']

            json_message = payload_as_json

            db_message = {'sender': sender, 'receiver': receiver, 'messageType': 'dm', 'id': timeID, 'comment': payload_as_json['comment'], 'totalLike':0}
            TCP.chatCollection.insert_one(db_message)

            message_as_bytes = json.dumps(json_message).encode()
            webframe = convert_webframe(TCP, message_as_bytes)
            # message will display only for the sender and the receiver of the message
            for client in TCP.websocket_connections:
#                 if client['username'] == sender or client['username'] == receiver:
                if client['username'] == receiver:
                    client['socket'].request.sendall(webframe)

        data = b''

    return


def websocket_request(TCP: MyTCPHandler, Headers):
    key = Headers[b'Sec-WebSocket-Key'].decode()
    accept = compute_accept(key)
    response = generate_socket_response('101 Switching Protocols', accept)
    TCP.request.sendall(response)

    # SUBJECT TO CHANGE
    # username = "User" + str(random.randint(0,1000))
    cookieID = retrieveAuthenticationCookieId(Headers[b'Cookie'])
    username = authenticatedUser(cookieID).decode()
    profile_picture = retrieveProfilePicture(username.encode()).decode()
    MyTCPHandler.websocket_connections.append({'username': username, 'socket': TCP, 'profile_picture': profile_picture})
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$", '\n')
    print(MyTCPHandler.websocket_connections, '\n')

    json_message = {'messageType':'user_connect','username':username}

    message_as_bytes = json.dumps(json_message).encode()
    webframe = convert_webframe(TCP, message_as_bytes)

    for client in TCP.websocket_connections:
        if client['socket'] != TCP:
            client['socket'].request.sendall(webframe)

    handleWebSocket(TCP, username)


def compute_accept(key: str):
    websocket_key = key + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
    hash_object = hashlib.sha1(websocket_key.encode()).digest()
    base64_encoded = base64.b64encode(hash_object)
    return base64_encoded


def generate_socket_response(response_code: str, accept_response: bytes):
    response = b'HTTP/1.1 ' + response_code.encode()
    response += b'\r\nConnection: Upgrade'
    response += b'\r\nUpgrade: websocket'
    response += b'\r\nSec-WebSocket-Accept: ' + accept_response
    response += b'\r\n\r\n'
    return response

def convert_webframe(TCP: MyTCPHandler, message: bytes):

    length = len(message)
    frame = 0

    if length < 126:
        frame = (129).to_bytes(1, "big") + (length).to_bytes(1, "big")
    elif length >= 126 and length < 65536:
        frame = (129).to_bytes(1, "big") + (126).to_bytes(1, "big") + (length).to_bytes(2, "big")
    else:
        frame = (129).to_bytes(1, "big") + (127).to_bytes(1, "big") + (length).to_bytes(8, "big")

    frame += message
    return frame

