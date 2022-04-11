import sys
import json
import socketserver
import pymongo
from server import mydb, userCollection

'''
This method will handle DELETE requests

The inputted data will be:
    -- The TCP object from the main server.
    -- A dictionary with Key-Value pairs from the Header and Body (Byte encoded already)
'''

def handle(TCP, path, data):
    # DELETE /users/{id}

    if path.startswith(b'/users/'):
        id = str(path.split(b'/')[-1])

        if id.isnumeric():
            id_object = userCollection.find_one({'id': int(id)})

            if id_object:
                query = {'id': int(id)}
                userCollection.delete_one(query)
                response = TCP.generate_http_response(TCP, b'', 'text/plain; charset=utf-8', '204')
                return TCP.request.sendall(response)
    
    # If no record of requested ID / record has already been deleted.
    body = "The requested content was not found."

    response = TCP.generate_http_response(TCP, body.encode(), 'text/plain; charset=utf-8', '404')
    
    return TCP.request.sendall(response)
