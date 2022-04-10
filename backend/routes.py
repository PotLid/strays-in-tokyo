def request(path):
  
  ## Obj 4: RESTful API 1
  
   if type == "POST" and path == "/users":
            # POST /users w/ body content
            data = self.headers["BODY"]

            info = json.loads(data)

            info['id'] = get_next_id()

            users_collection.insert_one(info)
            info.pop('_id')

            json_object = json.dumps(info)

            response = responseBuilder(201, "application/json; charset=utf-8", str(byteSize(json_object)), "") 
            self.request.sendall((response.encode()) + (json_object.encode()))
  
    elif type == "PUT" and path.startswith("/users/"):
            # PUT /users/{id}
            id = path.split('/')[-1]
            
            # update the record with the id of {id} using the data from body of the request
            data = self.headers["BODY"]
            info = json.loads(data)
            
            if id.isnumeric():
                id_object = users_collection.find_one({'id': int(id)})

                if id_object:
                    query = {"id": int(id)}
                    newvalues = {"$set": info}
                    users_collection.update_one(query, newvalues)

                    user_info = users_collection.find_one({'id': int(id)}, {"_id": False})
                    
                    json_object = json.dumps(user_info)

                    response = responseBuilder(200, "application/json; charset=utf-8", str(byteSize(json_object)), "")
                    self.request.sendall((response.encode()) + (json_object.encode()))
                else:
                    response = responseBuilder(404, "text/plain; charset=utf-8", "36", "") + "The requested content was not found."
                    self.request.sendall(response.encode())
  
  
  
  
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


