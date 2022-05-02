import sys
import json
import socketserver
import pymongo
import server

'''
This method will handle the POST requests

The inputted data will be:
    -- The TCP object from the main server.
    -- A dictionary with Key-Value pairs from the Header and Body (Byte encoded already)
'''

users_id_collection = {}

def handle(TCP, path, data):

    # POST /users

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

    response = TCP.generate_http_response(TCP, body.encode(), 'text/plain; charset=utf-8', '404')
    
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