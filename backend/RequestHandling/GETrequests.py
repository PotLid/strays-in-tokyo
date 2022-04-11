import sys
import json
import socketserver
import pymongo
from server import mydb, userCollection

'''
This method will handle GET requests

The inputted data will be:
    -- The TCP object from the maiin server.
    -- A dictionary with Key-Value pairs from the Header and Body (Byte encoded already)
    '''

def handle(TCP, path, data):
    if path == b'/':
        Message = b'Website still under construction!'
        Message_Length = str(sys.getsizeof(Message))
        initial = b'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length:' + Message_Length.encode() + b'\r\n\r\n' + Message
        TCP.request.sendall(initial)

    elif path == b'/users':
        # GET /users
        
        data = userCollection.find({}, {"_id": False})

        json_object = json.dumps((list(data)))

        response = TCP.generate_http_response(TCP, json_object.encode(), 'application/json; charset=utf-8', '200')
        return TCP.request.sendall(response)

    elif path.startswith(b'/users/'):
        # GET /users/{id}
        id = str(path.split(b'/')[-1])
        
        if id.isnumeric():
            
            id_object = userCollection.find_one({'id': int(id)}, {"_id": False})
            
            if id_object:
                json_object = json.dumps(id_object)

                response = TCP.generate_http_response(TCP, json_object.encode(), 'application/json; charset=utf-8', '200')
                return TCP.request.sendall(response)
    
    # If path is not as expected.

    body = "The requested content was not found."

    response = TCP.generate_http_response(TCP, body.encode(), 'text/plain; charset=utf-8', '404')
    
    return TCP.request.sendall(response)
                
