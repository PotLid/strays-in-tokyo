from pymongo import MongoClient
import socketserver
import sys
from backend.httpRequestParser import parseRequest

# Creating a pymongo client
MongoClient = MongoClient('localhost', 27017)

# Important: In MongoDB, a database is not created until it gets content!
mydb = MongoClient["312Project"]

# Creating database collections
userCollection = mydb["Users"]
postCollection = mydb["Posts"]



class MyTCPHandler(socketserver.BaseRequestHandler):

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




    def handle(self):

        # This will store all of the data with or without buffers.
        data = b''            
        #Get the initial data from the client, this will be the headers (chance that some of the body is here as well)
        received_data = self.request.recv(1024)
        '''Add Buffering'''
        #For debugging purposes~
        sys.stdout.flush()
        sys.stderr.flush()
        
        #After getting the data from the client, we will parse the data.
        parseRequest(data)



if __name__ == "__main__":

    Host = "0.0.0.0"
    Port = 8000

    print('Listening on port %s ...' % Port)

    server = socketserver.ThreadingTCPServer((Host, Port), MyTCPHandler)
    server.serve_forever()