from server import MyTCPHandler
import hashlib
import base64

#
def handleWebSocket(TCP: MyTCPHandler, data):

    # Implement the handshake of the WebSocket protocol at the path “/websocket”.
    # Upgrade the TCP socket to a WebSocket connection.

    websocket_key = data[b'Sec-WebSocket-Key']
    websocket_key += b'258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

    # compute the SHA1 hash and Base64 encoding.
    hashed_key = hashlib.sha1(websocket_key).digest()
    hash_to_base64 = base64.b64encode(hashed_key)

    # Create a response to upgrade the TCP socket to a WebSocket connection
    handshake_response = b'HTTP/1.1 101 Switching Protocols\r\nConnection: Upgrade\r\nUpgrade: websocket\r\nSec-WebSocket-Accept: ' + hash_to_base64 + b'\r\n\r\n' 

    TCP.request.sendall(handshake_response)

    # This while statement will listen to the messages sent over by the user.
    while True:
        recieved_data = TCP.request.recv(1024)
     