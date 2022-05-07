import sys
import json
import socketserver
import pymongo
import server
import backend.userHandling
import backend.MultiPartFormParser

'''
This method will handle the POST requests

The inputted data will be:
    -- The TCP object from the main server.
    -- A dictionary with Key-Value pairs from the Header and Body (Byte encoded already)
'''

users_id_collection = {}

def handle(TCP, path, data):
    print("This is the data in line 20 of POST handling: ", data, '\n')
    # POST /users

    #This is where we will authenticate the users
    if path == b'/login':
        backend.userHandling.parse(TCP, path, data)
        
    if path == b'/register':
        backend.userHandling.parse(TCP, path, data)
       
    if path == b'/settings':
       backend.userHandling.parse(TCP, path, data)

    if path == b'/chatpage':
        print("This is the data that was submitted in the chatapp: ", data)
        # Handle XSRF authentication
        validate_xsrf_token = backend.userHandling.parse(TCP, path, data)
        # If the xsrf_token doesn't match anything the database, we return a 403 Forbidden
        if validate_xsrf_token == False:
            # Return 403 Forbidden
            Message = "This XSRF token does not belong to this user"
            LenOfMessage = len(Message)
            NotFoundResponse = 'HTTP/1.1 403 Forbidden\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: ' + str(LenOfMessage) + '\r\n\r\n' + Message
            return TCP.request.sendall(NotFoundResponse.encode())

        # If the xsrf_token exists in the database, we simply redirect them back to the chatapp page
        RedirectResponse = 'HTTP/1.1 301 Moved Permanently\r\nContent-Type: text/plain\r\nContent-Length: 0\r\nLocation: /chatpage\r\n\r\n'
        return TCP.request.sendall(RedirectResponse.encode())

    ##########################################################################################

    if path == b'/users' or path == b'/users/':
        # body of the request is a JSON object with email and username fields
        body = data[b'Body']

        record = json.loads(body)

        record['id'] = get_next_id()

        server.MyTCPHandler.userCollection.insert_one(record)
        record.pop('_id')

        json_object = json.dumps(record)

        response = TCP.generate_http_response(TCP, json_object.encode(), 'application/json; charset=utf-8', '201')

        return TCP.request.sendall(response)
    
    # If path is not as expected.

    body = "The requested content was not found."

    response = server.MyTCPHandler.generate_http_response(TCP, body.encode(), 'text/plain; charset=utf-8', '404')
    
    return TCP.request.sendall(response)


def get_next_id():
    users_id_collection = server.MyTCPHandler.mydb["Users_ID"]
    id_object = users_id_collection.find_one({})
    if id_object:
        next_id = int(id_object['last_id']) + 1
        users_id_collection.update_one({}, {'$set': {'last_id': next_id}})
        return next_id
    else:
        users_id_collection.insert_one({'last_id':1})
        return 1