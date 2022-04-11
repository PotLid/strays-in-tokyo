import sys
import json
import socketserver
import pymongo
from server import mydb, userCollection

'''
This method will handle PUT requests

The inputted data will be:
    -- The TCP object from the main server.
    -- A dictionary with Key-Value pairs from the Header and Body (Byte encoded already)
'''

def handle(TCP, path, data):

    # PUT /users/{id}
    if path.startswith(b'/users/'):
        id = str(path.split(b'/')[-1])

        if id.isnumeric():
            body = data[b'Body']

            record = json.loads(body)

            id_object = userCollection.find_one({'id': int(id)})

            if id_object:
                query = {'id': int(id)}
                updated_info = {'$set': record}
                userCollection.update_one(query, updated_info)

                user_info = userCollection.find_one({'id': int(id)}, {'_id': False})

                json_object = json.dumps(user_info)

                response = TCP.generate_http_response(TCP, json_object.encode(), 'application/json; charset=utf-8', '200')

                return TCP.request.sendall(response)

    # If no record of requested ID / record has already been deleted.
    body = "The requested content was not found."

    response = TCP.generate_http_response(TCP, body.encode(), 'text/plain; charset=utf-8', '404')
    
    return TCP.request.sendall(response)
