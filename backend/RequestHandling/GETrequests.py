import sys
import json
import socketserver
import pymongo
from backend.websocketHandler import handleWebSocket
import server
import os
from backend import websocketHandler
'''
This method will handle GET requests

The inputted data will be:
    -- The TCP object from the maiin server.
    -- A dictionary with Key-Value pairs from the Header and Body (Byte encoded already)
    '''

def handle(TCP, path, data):
    # Route for the homepage, AKA the index.html 
    if path == b'/':
        content = render_content("frontend/public/index.html")
        content = server.MyTCPHandler.generate_http_response(TCP, content.encode(), "text/html; charset=utf-8", "200 OK")
        TCP.request.sendall(content)

    elif path == b'/functions.js':
        content = render_content("functions.js")
        content = server.MyTCPHandler.generate_http_response(TCP, content.encode(), "text/javascript; charset=utf-8", "200 OK")
        TCP.request.sendall(content)

    elif path == b'/websocket':
        websocketHandler.websocket_request(TCP, data)

    elif path == b'/users':
        # GET /users
        
        data = server.MyTCPHandler.userCollection.find({}, {"_id": False})

        json_object = json.dumps((list(data)))

        response = server.MyTCPHandler.generate_http_response(TCP, json_object.encode(), 'application/json; charset=utf-8', '200 OK')
        return TCP.request.sendall(response)

    elif path.startswith(b'/users/'):
        # GET /users/{id}
        id = str(path.split(b'/')[-1])
        
        if id.isnumeric():
            
            id_object = server.MyTCPHandler.userCollection.find_one({'id': int(id)}, {"_id": False})
            
            if id_object:
                json_object = json.dumps(id_object)

                response = server.MyTCPHandler.generate_http_response(TCP, json_object.encode(), 'application/json; charset=utf-8', '200 OK')
                return TCP.request.sendall(response)
    
    # If path is not as expected.
    else:
        body = "The requested content was not found."

        response = server.MyTCPHandler.generate_http_response(TCP, body.encode(), 'text/plain; charset=utf-8', '404 Not Found')
        
        return TCP.request.sendall(response)
                

def render_content(html_filename: str):
    with open(html_filename) as html_file:
        content =  html_file.read()
        return content