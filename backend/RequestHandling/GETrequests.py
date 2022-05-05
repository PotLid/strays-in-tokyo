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
    print("This is the GET request path: ", path, '\n')
    print('This is the GET request data: ', data, '\n')
    # Route for the homepage, AKA the index.html 
    if path == b'/':
        content = render_content("frontend/templates/homepage.html")
        content = server.MyTCPHandler.generate_http_response(TCP, content.encode(), "text/html; charset=utf-8", "200 OK")
        TCP.request.sendall(content)
    
    elif b'.png' in path:
        path = path[1:].decode()
        Exist = os.path.exists(path)
        if Exist:
            openPNG = open(path, "rb")
            readPNG = openPNG.read()
            PNGbyteSize = os.path.getsize(path)
            PNGresponse = 'HTTP/1.1 200 OK\r\nContent-Type: image/png; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\nContent-Length: ' + str(PNGbyteSize) + '\r\n\r\n'
            PNGresponse = PNGresponse.encode()
            PNGresponse += readPNG
            TCP.request.sendall(PNGresponse)

    elif b'.css' in path:
        path = path[1:].decode()
        Exist = os.path.exists(path)
        if Exist:
            openCSS = open(path, "rb")
            readCSS = openCSS.read()
            CSSpath = path
            CSSbyteSize = os.path.getsize(CSSpath)
            CSSresponse = 'HTTP/1.1 200 OK\r\nContent-Type: text/css; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\nContent-Length: ' + str(CSSbyteSize) + '\r\n\r\n'
            CSSresponse += readCSS.decode()
            TCP.request.sendall(CSSresponse.encode())

    elif path == b'/functions.js':
        content = render_content("functions.js")
        content = server.MyTCPHandler.generate_http_response(TCP, content.encode(), "text/javascript; charset=utf-8", "200 OK")
        TCP.request.sendall(content)

    elif path == b'/login':
        content = render_content("frontend/templates/login.html")
        content = server.MyTCPHandler.generate_http_response(TCP, content.encode(), "text/html; charset=utf-8", "200 OK")
        TCP.request.sendall(content)

    elif path == b'/register':
        content = render_content("frontend/templates/register.html")
        content = server.MyTCPHandler.generate_http_response(TCP, content.encode(), "text/html; charset=utf-8", "200 OK")
        TCP.request.sendall(content)

    # The user MUST be authenticated to even access this page
    elif path == b'/settings':
        content = render_content("frontend/templates/settings.html")
        content = server.MyTCPHandler.generate_http_response(TCP, content.encode(), "text/html; charset=utf-8", "200 OK")
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

