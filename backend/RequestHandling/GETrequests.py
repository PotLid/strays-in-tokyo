import secrets
import sys
import json
import socketserver
import pymongo
from backend.websocketHandler import handleWebSocket
from backend.userHandling import authenticatedUser, handleVisit, authenticateXSRF, retrieveAuthenticationCookieId, handleLogout, retrieveProfilePicture, onlineUsers
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
    # Route for the homepage, AKA the homepage.html
    if path == b'/':
        content = render_content("frontend/templates/homepage.html")
        content = server.MyTCPHandler.generate_http_response(TCP, content.encode(), "text/html; charset=utf-8", "200 OK")
        TCP.request.sendall(content)

    elif b'.jpg' in path:
        path = path[1:].decode()
        Exist = os.path.exists(path)
        if Exist:
            openJPG = open(path, "rb")
            readJPG = openJPG.read()
            JPGbyteSize = os.path.getsize(path)
            JPGresponse = 'HTTP/1.1 200 OK\r\nContent-Type: image/png; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\nContent-Length: ' + str(JPGbyteSize) + '\r\n\r\n'
            JPGresponse = JPGresponse.encode()
            JPGresponse += readJPG
            TCP.request.sendall(JPGresponse)

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

    elif path == b'/javascript/chat.js':
        content = render_content("frontend/javascript/chat.js")
        content = server.MyTCPHandler.generate_http_response(TCP, content.encode(), "text/javascript; charset=utf-8", "200 OK")
        TCP.request.sendall(content)

    elif path == b'/login':
        content = render_content("frontend/templates/login.html")
        content = server.MyTCPHandler.generate_http_response(TCP, content.encode(), "text/html; charset=utf-8", "200 OK")
        TCP.request.sendall(content)

    elif path == b'/logout':
        handleLogout(data[b'Cookie'])
        # If the user has logged out, redirect them back to the home page
        RedirectResponse = 'HTTP/1.1 301 Moved Permanently\r\nContent-Type: text/plain\r\nContent-Length: 0\r\nLocation: /\r\n\r\n'
        return TCP.request.sendall(RedirectResponse.encode())

    elif path == b'/register':
        content = render_content("frontend/templates/register.html")
        content = server.MyTCPHandler.generate_http_response(TCP, content.encode(), "text/html; charset=utf-8", "200 OK")
        TCP.request.sendall(content)

    # The user MUST be authenticated to even access this page
    elif path == b'/settings':
        # We must add authentication to the chatapp page.
        if b'Cookie' in data:
            cookie_id = retrieveAuthenticationCookieId(data[b'Cookie'])
            authenticated = authenticatedUser(cookie_id)
            print("This is the username: ", authenticated, '\n')
            xsrf_token = handleVisit(TCP, data, authenticated)
            print("This is the XSRF token: ", xsrf_token)
            if authenticated != None and authenticated != "":
                profile_picture_name = retrieveProfilePicture(authenticated).decode()
                content = render_template("frontend/templates/settings.html", {"xsrf_token":xsrf_token,
                                                                            "profile_picture_name":profile_picture_name,
                                                                            "loop_data": ''})
                content = server.MyTCPHandler.generate_http_response(TCP, content.encode(), "text/html; charset=utf-8", "200 OK")
                return TCP.request.sendall(content)
            else:
                Message = "You must log in to view this page"
                LenOfMessage = len(Message)
                NotFoundResponse = 'HTTP/1.1 403 Forbidden\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: ' + str(LenOfMessage) + '\r\n\r\n' + Message
                return TCP.request.sendall(NotFoundResponse.encode())
        else:
            Message = "You must log in to view this page"
            LenOfMessage = len(Message)
            NotFoundResponse = 'HTTP/1.1 403 Forbidden\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: ' + str(LenOfMessage) + '\r\n\r\n' + Message
            return TCP.request.sendall(NotFoundResponse.encode())


    elif path == b'/chatpage':
        # We must add authentication to the chatapp page.
        if b'Cookie' in data:
            cookie_id = retrieveAuthenticationCookieId(data[b'Cookie'])
            authenticated = authenticatedUser(cookie_id)
            print("This is the username: ", authenticated, '\n')
            xsrf_token = handleVisit(TCP, data, authenticated)
            print("This is the XSRF token: ", xsrf_token)
            if authenticated != None and authenticated != "":
                online_users = onlineUsers()
                print("These are all of the online users so far: ", online_users)
                content = render_template("frontend/templates/chat.html", {"xsrf_token":xsrf_token,
                                                                            "loop_data": online_users})
                content = server.MyTCPHandler.generate_http_response(TCP, content.encode(), "text/html; charset=utf-8", "200 OK")
                TCP.request.sendall(content)
            else:
                Message = "You must log in to view this page"
                LenOfMessage = len(Message)
                NotFoundResponse = 'HTTP/1.1 403 Forbidden\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: ' + str(LenOfMessage) + '\r\n\r\n' + Message
                return TCP.request.sendall(NotFoundResponse.encode())
        else:
            Message = "You must log in to view this page"
            LenOfMessage = len(Message)
            NotFoundResponse = 'HTTP/1.1 403 Forbidden\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: ' + str(LenOfMessage) + '\r\n\r\n' + Message
            return TCP.request.sendall(NotFoundResponse.encode())


    elif path == b'/websocket':
        websocketHandler.websocket_request(TCP, data)

    elif path == b'/chat-history':

        response = {}

        return TCP.request.sendall(response)

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



def render_template(html_filename, data):
    #region...(Render the HTML template)
    with open(html_filename) as html_file:
        template = html_file.read()
        template = replace_placeholders(template, data)
        template = render_loop(template, data)
        return template
    #endregion

def replace_placeholders(template, data):
    print("This is the data: ", data)
    #region...(Replace all placeholders in the HTML template)
    replaced_template = template
    for placeholder in data.keys():
        if isinstance(data[placeholder], str):
            replaced_template = replaced_template.replace("{{"+placeholder+"}}", data[placeholder])
    return replaced_template
    #endregion

def render_loop(template, data):
    #region...(Going through the html template loop)
    if "loop_data" in data:
        loop_start_tag = "{{loop}}"
        loop_end_tag =  "{{end_loop}}"

        start_index = template.find(loop_start_tag)
        end_index = template.find(loop_end_tag)

        loop_template = template[start_index + len(loop_start_tag): end_index]
        loop_data = data["loop_data"]
        loop_content = ""
        for single_piece_of_content in loop_data:
            loop_content += replace_placeholders(loop_template, single_piece_of_content)
        final_content = template[:start_index] + loop_content + template[end_index+len(loop_end_tag):]
        return final_content
    #endregion

def escape_html(input):
    #region...(Removing any HTML characters; for Security reasons)
    return input.replace(b'&', b'&amp;').replace(b'<', b'&lt;').replace(b'>', b'&gt;')
    #endregion
