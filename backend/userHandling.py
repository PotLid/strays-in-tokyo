import hashlib
import os
import bcrypt
import server
import secrets

'''
This file will handle all of the User Authentication and Handling.

@ Everything will be in byte format.

#####################################################

Login:
    When a User logs in for the first time, we will set a authentication cookie for them.

Register: 
    When a user sends a registration request, store their username and a salted hash of their password in your database.

Profile Picture:
    - If they have not submitted anything, they will issues the default profile picture of the cat.
    - If they have changed to something else, we will update it in the database.'''


def parse(TCP, path, body):
    print("This is the current path: ", path)
    print("This is the current body on line 26: ", body)
    actual_body = body[b'Body']
    #region...(Parsing the MultiFormData)
    Split = actual_body.find(b'\r\n')

    # Isolate the Multi-Form data boundaries 
    Border = actual_body[:Split]
    
    # Split all instances of a border to isolate the message and image
    SplitBorders = actual_body.split(Border)
    
    email = b''
    password = b''
    confirm_password = b''
    message = b''
    profile_picture_filename = b''
    profile_picture_data = b''
    xsrf_token = b''

    for data in SplitBorders:

        # For identifying the email and password
        if b'form-data; name="email"\r\n\r\n' in data:
            find_email = data.find(b'\r\n\r\n')
            email = data[find_email+4:len(data)-2]
            email = server.MyTCPHandler.escape_html(TCP, email)

        if b'form-data; name="password"\r\n\r\n' in data:
            find_password = data.find(b'\r\n\r\n')
            password = data[find_password+4:len(data)-2]

        if b'form-data; name="confirm_password"\r\n\r\n' in data:
            find_password = data.find(b'\r\n\r\n')
            confirm_password = data[find_password+4:len(data)-2]
        

        # For identifying the Comment/Caption.
        if b'form-data; name="comment"\r\n\r\n' in data:
            find_message = data.find(b'\r\n\r\n')
            message = data[find_message+4:len(data)-2]
            message = server.MyTCPHandler.escape_html(TCP, message)

        # For identifying the image filename and file data in bytes.
        if b'form-data; name="filename"' in data:
            profile_picture_filename = data.split(b'\r\n', 2)[1]
            profile_picture_filename = profile_picture_filename[profile_picture_filename.find(b'filename=')+10:len(profile_picture_filename)-1].decode()
            profile_picture_filename = profile_picture_filename.replace("/", "").replace("%20", " ")

            profile_picture_data = data[data.find(b'\r\n\r\n')+4:]
            
        # For identifying the xsrf tokens
        if b'form-data; name="xsrf_token"' in data:
            find_xsrf_token = data.find(b'\r\n\r\n')
            xsrf_token = data[find_xsrf_token+4:len(data)-2]

    print("Comment is: ", message, '\n')
    if path == b'/login':
        handleLogin(TCP, email, password)
    if path == b'/register':
        handleRegistration(TCP, email, password, confirm_password)
    if path == b'/settings':
        valid = authenticateXSRF(TCP, body, xsrf_token); print("Line 92 validility:", valid, '\n')
        if valid:
            handleProfilePicture(TCP, body, profile_picture_filename.encode(), profile_picture_data)
        if valid == False:
            return valid
    if path == b'/chatpage':
        return authenticateXSRF(TCP, body, xsrf_token)

'''
When a user sends a registration request, store their username and a salted hash of their password in your database.
The data will be stored in byte format.'''

def handleRegistration(TCP, email, password, confirm_password):
    print("##########################")
    print("We are now handling the registration")
    print("##########################", '\n')

    # If the user has typed any email and password, we redirect them to the login page.   
    if len(email) != 0 and len(password) != 0 and (password == confirm_password):
        print("Registration successful")
        # Generating a random salt
        random_salt = bcrypt.gensalt()
        # Append the random salt to the given passcode
        password = password + random_salt
        # Hash the passcode
        hashed = bcrypt.hashpw(password, random_salt)
        server.MyTCPHandler.userCollection.insert_one({'email': email, 'salt':random_salt, 'hash': hashed, 'profile_picture':b'kitty.png', 'authenticated_token':b'', "authenticated_xsrf_token":b''})
        # Redirect to the homepage after registering
        RedirectResponse = 'HTTP/1.1 301 Moved Permanently\r\nContent-Type: text/plain\r\nContent-Length: 0\r\nLocation: /login\r\n\r\n'
        return TCP.request.sendall(RedirectResponse.encode())

    # If the user hasn't typed any email or password, we just redirect them back to the same page.   
    else:
        RedirectResponse = 'HTTP/1.1 301 Moved Permanently\r\nContent-Type: text/plain\r\nContent-Length: 0\r\nLocation: /register\r\n\r\n'
        return TCP.request.sendall(RedirectResponse.encode())


'''
When a user successfully logs in, set an authentication token as a cookie for that user with the HttpOnly directive set. 
These tokens should be random values that are associated with the user. 
You must store a hash of each token in your database so you can verify them on subsequent requests.
The data will be stored in byte format.'''

def handleLogin(TCP, email, password):
    print("##########################")
    print("We are now handling the login")
    print("##########################", '\n')

    # Retrieve the user info from when they registered.
    user_info = server.MyTCPHandler.userCollection.find_one({'email':email})
    print("This is the current user info: ", user_info)
    if user_info != None:
        user_authentication_token = user_info['authenticated_token']
        # Check to make sure that the inputted password matches the hashed password in the database.
        user_salt = user_info['salt']
        password += user_salt
        hashed_passcode = bcrypt.hashpw(password, user_salt)
        if hashed_passcode == user_info['hash']:
            print("Login successful", '\n')
            # Setting up the hashed authentication token id for the cookie
            authentication_token = secrets.token_urlsafe()
            hashed_authenticated_token = hashlib.sha256(authentication_token.encode()).digest()
            # Add the hashed authentication token to the database if they have never signed in before and redirect to the chat page
            if len(user_authentication_token) == 0:
                
                server.MyTCPHandler.userCollection.update_one({'email':email}, {"$set":{"authenticated_token":hashed_authenticated_token}})
                # Redirect to the chatpage after successfuly updating the database
                RedirectResponse = 'HTTP/1.1 301 Moved Permanently\r\nContent-Type: text/plain\r\nContent-Length: 0\r\nSet-Cookie: id=' + str(authentication_token) + '; Max-Age=3600' + '; HttpOnly' + '\r\nLocation: /chatpage\r\n\r\n'
                return TCP.request.sendall(RedirectResponse.encode())

            # Update the hashed authentication token to the database if they signed in before and redirect to the chat page
            if len(user_authentication_token) != 0:
                print("They logged in again", '\n')
                print("This is the new authentication token: ", authentication_token, '\n')
                server.MyTCPHandler.userCollection.update_one({'email':email}, {"$set":{"authenticated_token":hashed_authenticated_token}})
                # Redirect to the chatpage after successfuly updating the database and cookie
                RedirectResponse = 'HTTP/1.1 301 Moved Permanently\r\nContent-Type: text/plain\r\nContent-Length: 0\r\nSet-Cookie: id=' + str(authentication_token) + '; Max-Age=3600' + '; HttpOnly' + '\r\nLocation: /chatpage\r\n\r\n'
                return TCP.request.sendall(RedirectResponse.encode())
        else:
            # If the password is incorrect, we will just keep redirecting them to the login page
            RedirectResponse = 'HTTP/1.1 301 Moved Permanently\r\nContent-Type: text/plain\r\nContent-Length: 0\r\nLocation: /login\r\n\r\n'
            return TCP.request.sendall(RedirectResponse.encode())

    else:
        # If there is no such user, we will just keep redirecting them to the login page
        RedirectResponse = 'HTTP/1.1 301 Moved Permanently\r\nContent-Type: text/plain\r\nContent-Length: 0\r\nLocation: /login\r\n\r\n'
        return TCP.request.sendall(RedirectResponse.encode())

    


'''
Handling the Profile Picture:
    - When handling the profile picture, the user must have submitted something.
    - If they have not submitted anything, they will issues the default profile picture of the cat.
    - If they have changed to something else, we will update it in the database.'''

def handleProfilePicture(TCP, data, profile_picture_filename, profile_picture_data):
    print("##########################")
    print("We are now handling the profile picture being updated")
    print("##########################", '\n')
    cookie_id = retrieveAuthenticationCookieId(data[b'Cookie'])
    email = authenticatedUser(cookie_id)
    if len(profile_picture_filename) == 0:
        profile_picture_filename = b'kitty.png'
    path = 'frontend/static/' + profile_picture_filename.decode()
    check_existense = os.path.exists(path)
    if check_existense == False:
        with open(path, "wb") as f:
            f.write(profile_picture_data)
    user_info = server.MyTCPHandler.userCollection.find_one({"email": email})
    if user_info != None:
        server.MyTCPHandler.userCollection.update_one({"email": email}, {"$set":{"profile_picture": profile_picture_filename}})
    
    return




def authenticateXSRF(TCP, body, xsrf_token):
    print("##########################")
    print("We are now handling the xsrf")
    print("##########################", '\n')
    cookie_id = retrieveAuthenticationCookieId(body[b'Cookie'])
    email = authenticatedUser(cookie_id)

    get_db_xsrf_token = server.MyTCPHandler.userCollection.find_one({"email": email})
    get_db_xsrf_token = get_db_xsrf_token['authenticated_xsrf_token']
    print("This is the current xsrf token waiting to be validated: ", get_db_xsrf_token, '\n')
    if get_db_xsrf_token != xsrf_token.decode():
        return False

    return True

'''
@ handleVisit will be ran every time someone makes a GET request to the chatapp page and settings page
*** The User MUST be authenitcated (logged in) and MUST have a valid XSRF token
- The returned result will be either the xsrf token being added or an empty string
'''
def handleVisit(TCP, cookie_id, email):
    print("##########################")
    print("We are now handling the tokens")
    print("##########################", '\n')
    xsrf_token = ""

    if cookie_id != b'':
                    
        valid_xsrf_token = server.MyTCPHandler.userCollection.find_one({"email": email})
        print("Valid xsrf token: ", valid_xsrf_token, '\n')
        if valid_xsrf_token != None:
            xsrf_token = valid_xsrf_token["authenticated_xsrf_token"]
            if len(email) != 0 and xsrf_token != b'':
                print("Adding to the database since the user is refreshing the page")
                return xsrf_token
            if len(email) != 0 and xsrf_token == b'':
                xsrf_token = secrets.token_urlsafe()
                print("This is the xsrf for the authenticated user when they first visit: ", xsrf_token, '\n')
                server.MyTCPHandler.userCollection.update_one({"email": email}, {"$set":{"authenticated_xsrf_token": xsrf_token}})
                return xsrf_token

    return ""


def authenticatedUser(cookie_id):
    hashed_token = hashlib.sha256(cookie_id).digest()
    user_info = server.MyTCPHandler.userCollection.find_one({'authenticated_token':hashed_token})
    print("Line 232 user info: ", user_info, '\n')
    if user_info != None:
        if len(user_info) != 0:
            return user_info['email']
    return ""

def retrieveAuthenticationCookieId(cookie_data):
    print("This is the cookie data: ", cookie_data, '\n')
    if b'id' in cookie_data:
        beginning_cookie_id = cookie_data.find(b"=")+1
        return cookie_data[beginning_cookie_id:]

    return None

def retrieveProfilePicture(email:bytes):
    user_info = server.MyTCPHandler.userCollection.find_one({'email':email})
    return user_info["profile_picture"]


def handleLogout(cookie_data):
    cookie_id = retrieveAuthenticationCookieId(cookie_data)
    print("This is the cookie id returned while logging out: ", cookie_id)
    email = authenticatedUser(cookie_id)
    user_info = server.MyTCPHandler.userCollection.find_one({'email':email})
    if user_info != None:
        server.MyTCPHandler.userCollection.update_one({"email": email}, {"$set":{"authenticated_token": b''}})
    return