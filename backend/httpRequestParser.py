
'''
The returned data from this function will be a List in the format:

[ http_request_type, http_request-path, A dictionary with the Key-Value pairs from the Header and Body]

* The Dictionary will hold all Key-Value pairs in Bytes.

* The Dictionary will also hold the Body of the request:
    These are the example Keys of the returned Dictionary:
        dic[b'Host']
        dic[b'User-Agent']
        dic[b'Accept']
        dic[b'Accept-Language']
        dic[b'Body'] (If there is no Body then the value will be an empty byte string)

'''

# Initial structure to parse general HTTP requests
def parseRequest(data):
    dic = {}
    # Turn the HTTP request to a string
    # stringDecode = data.decode() 
    data = data

    # isolte the Request Line and put it in a string
    ParsingRequest = data.split(b'\r\n', 1) 
    
    # Remove any spaces from the Request Line
    RequestLine = ParsingRequest[0].split(b" ")
    
    # Creates an array for the header contents, each header is in its own index
    Header_Boundary = ParsingRequest[1].find(b'\r\n\r\n')
    Header = ParsingRequest[1][:Header_Boundary] #We take the complete header, with the exlusion of the body
    Header = Header.split(b'\r\n') #Splitting to get all header keys

    '''For Loop that will go through each element.
     -- Replaces the first instance of a space.
     -- Gets the length of the whole header.
     -- Finds the index of the : character. 
     -- Utilizes splittling to isolate the key value pairs
     -- Assigns the key and value pairs to each other'''
    
    for host in Header:
        DictHeaderKey = host.replace(b" ", b"", 1)
        HeaderLen = len(DictHeaderKey)
        if b":" in host:
            HeaderSplitIndex = DictHeaderKey.find(b":")
            Key = DictHeaderKey[0:HeaderSplitIndex]
            Value = DictHeaderKey[HeaderSplitIndex+1:HeaderLen]
            if Key in dic:
                List = []
                ValueToAppend = dic[Key]
                List.append(ValueToAppend)
                List.append(Value)
                dic[Key] = List
            if Key not in dic:
                dic[Key] = Value

    # -----Extracting the Body -----------------------------#
    Body = data.find(b'\r\n\r\n')
    Body = data[Body+4:len(data)]
    dic[b'Body'] = Body
    #-------------------------------------------------------#

    return [RequestLine[0], RequestLine[1], dic]  
