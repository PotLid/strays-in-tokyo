from pymongo import MongoClient
import socketserver
import sys
from backend.httpRequestParser import parseRequest
from backend.httpContentLengthParser import parseContentLength
from backend.RequestHandling import GETrequests, POSTrequests, PUTrequests, DELETErequests


class MyTCPHandler(socketserver.BaseRequestHandler):

    # Creating a pymongo client
    MongoClient = MongoClient('localhost', 27017)

    # Important: In MongoDB, a database is not created until it gets content!
    mydb = MongoClient["312Project"]

    # Creating database collections

    '''
    The UserCollection will consist of the following keys:
    {'email':email, 'salt':random_salt, 'hash': hashed_password, 'profile_picture':image_file,'authenticated_token': authenticated_token when they first sign in, 'authenticated_xsrf_token':xsrf_token}
    '''
    userCollection = mydb["Users"]
    '''
    The postCollection will consist of the following keys:
    {'email':email, 'comment':comment}
    '''
    postCollection = mydb["Posts"]

    buffer_length = 0
    Content_Length = 0

    # Escapes the HTML for security
    def escape_html(self, input):
        return input.replace(b'&', b'&amp;').replace(b'<', b'&lt;').replace(b'>', b'&gt;')


    # Generates a HTTP response in bytes
    def generate_http_response(self, body: bytes, content_type: str, response_code: str):
        response = b'HTTP/1.1 ' + response_code.encode()
        response += b'\r\nContent-Length: ' + str(len(body)).encode()
        response += b'\r\nContent-Type: ' + content_type.encode()
        response += b'\r\n\r\n'
        response += body
        return response

    # SUBJECT TO CHANGE
    websocket_connections = {}


    def handle(self):

        # This will store all of the data with or without buffers.
        data = b''            

        #Get the initial data from the client, this will be the headers
        received_data = self.request.recv(1024)
        
        print("{} sent:".format(self.client_address[0]))
        print(received_data, '\n')

        # Parse the initial data to extract the content length
        parser = parseContentLength(received_data)
        # Get the Content Length from the returned dictionary
        self.Content_Length = parser['Content-Length']
    
        data += received_data
        
        # If the body length is greater than 0, then we will add the Body to the existing data
        if parser['Body-Length'] > 0:
            self.buffer_length = parser['Body-Length']
            data += parser["Body"]

        # If the Content Length is not 0, we will start buffering for more data
        if self.Content_Length != 0:
            while self.buffer_length != self.Content_Length:
                buffer_data = self.request.recv(1024)
                self.buffer_length += len(buffer_data)
                data += buffer_data
                # If we have reached the Content Length, we will break out the While Loop
                if self.buffer_length >= self.Content_Length:
                    break
        # If the length of the recieved data is 0, we don't handle anything  
        if len(data) == 0:
            return

        #For debugging purposes~
        sys.stdout.flush()
        sys.stderr.flush()

        #After getting all the data from the client, we will parse the data.
        parsed_data = parseRequest(data)

        request_type = parsed_data[0]
        request_path = parsed_data[1]
        data_to_handle = parsed_data[2]

        # This is where we will be handling the Request Types
        if request_type == b'GET':
            GETrequests.handle(self, request_path, data_to_handle)
        if request_type == b'POST':
            POSTrequests.handle(self, request_path, data_to_handle)
        if request_type == b'PUT':
            PUTrequests.handle(self, request_path, data_to_handle[b'Body'])
        if request_type == b'DELETE':
            DELETErequests.handle(self, request_path, data_to_handle[b'Body'])


if __name__ == "__main__":

    Host = "0.0.0.0"
    Port = 8000

    print('Listening on port %s ...' % Port)

    server = socketserver.ThreadingTCPServer((Host, Port), MyTCPHandler)
    server.serve_forever()
