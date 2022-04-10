
def parseContentLength(data):
        dic = {}
        # isolte the Request Line and put it in a string
        ParsingRequest = data.split(b'\r\n', 1) 
        # Remove any spaces from the Request Line
        RequestLine = ParsingRequest[0].split(b" ") 
        if RequestLine[0] != b'POST':
             return {"Content-Length":0, "Body-Length":0}
        # Creates an array for the header contents, each header is in its own index
        Header = ParsingRequest[1].split(b'\r\n')
        
        Body = data.find(b'\r\n\r\n')
        Body = data[Body+4:len(data)]
        
        for host in Header:
            DictHeaderKey = host.replace(b" ", b"", 1)
            HeaderLen = len(DictHeaderKey)
            if b":" in host:
                HeaderSplitIndex = DictHeaderKey.find(b":")
                Key = DictHeaderKey[0:HeaderSplitIndex]
                Value = DictHeaderKey[HeaderSplitIndex+1:HeaderLen]
                # If key is already in the dictionary, put the values in the list and append to it
                if Key in dic:
                    # Check if the form-data is comment or upload? Then make new keys for them with the values being the actual message or image submission.
                    List = []
                    ValueToAppend = dic[Key]
                    List.append(ValueToAppend)
                    List.append(Value)
                    dic[Key] = List
                if Key not in dic:
                    dic[Key] = Value

        Content_Length = int(dic[b'Content-Length'])
        
        dic_to_return = {"Content-Length":Content_Length, "Body-Length":len(Body), "Body":Body}
        return dic_to_return