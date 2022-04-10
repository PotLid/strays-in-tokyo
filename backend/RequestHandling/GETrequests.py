import sys
'''
This method will handle GET requests

The inputted data will be:
    -- The TCP object from the maiin server.
    -- A dictionary with Key-Value pairs from the Header and Body (Byte encoded already)
    '''

def handle(TCP, path, data):
    if path == b'/':
        Message = b'Website still under construction!'
        Message_Length = str(len(Message)).encode()
        initial = b'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length:' + Message_Length + b'\r\n\r\n' + Message
        TCP.request.sendall(initial)

