def request(path):
  
  
  
  
  
  
  
  
  
  ##  Obj 5: RESTful API 2
  elif 'GET /users/' in parsed['Request']:
            components = parsed['Request'].split("/users/", 1)      # splits request header into [users, (userid) i.e. 1]
            filename = 'users/' + components[1]  
            user = userinfo.find_one({'id' : int(components[1])}, {'_id' : False})
            
            # if user id exists then return; else 404
            if user:
                # print(str(user))
                userJson = json.dumps(user)
                ctype = builder(filename)
                status = 'HTTP/1.1 200 OK\r\n'
                length = 'Content-Length: ' + str(len(str(userJson))) + '\r\n'
                response = status + length + ctype + '\r\n'
                self.request.sendall((response).encode() + (userJson.encode()))
            else:
                filename = '404.html'
                response, retFile = builder(filename)
                self.request.sendall((response).encode() + retFile)


        elif 'PUT /users/' in parsed['Request']:
            components = parsed['Request'].split("/users/", 1)      # splits request header into [users, (userid) i.e. 1]
            filename = 'users/' + components[1] 
            update = json.loads(parsed['json'])
            user = userinfo.find_one_and_update({'id' : int(components[1])}, {'$set' : update}, {'_id' : False}, new = True)
            
            if user:
                userJson = json.dumps(user)
                ctype = builder(filename)
                status = 'HTTP/1.1 200 OK\r\n'
                length = 'Content-Length: ' + str(len(str(userJson))) + '\r\n'
                response = status + length + ctype + '\r\n'
                self.request.sendall((response).encode() + (userJson.encode()))
            else:
                filename = '404.html'
                response, retFile = builder(filename)
                self.request.sendall((response).encode() + retFile)
        

        elif 'DELETE /users/' in parsed['Request']:
            components = parsed['Request'].split("/users/", 1)      # splits request header into [users, (userid) i.e. 1]
            filename = 'users/' + components[1] 
            deleted = userinfo.find_one_and_delete({'id' : int(components[1])}, {'_id' : False})
            
            if deleted:
                print("\nSERVER DELETED: " + str(deleted) + "\n")
                userJson = json.dumps(str(deleted))
                ctype = builder(filename)
                status = 'HTTP/1.1 204 No Content\r\n'
                length = 'Content-Length: ' + str(len(str(userJson))) + '\r\n'
                response = status + length + ctype + '\r\n'
                self.request.sendall((response).encode())
            else:
                filename = '404.html'
                response, retFile = builder(filename)
                self.request.sendall((response).encode() + retFile)


