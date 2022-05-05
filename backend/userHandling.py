import bcrypt
import server

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
    #region...(Parsing the MultiFormData)
    Split = body.find(b'\r\n')

    # Isolate the Multi-Form data boundaries 
    Border = body[:Split]
    
    # Split all instances of a border to isolate the message and image
    SplitBorders = body.split(Border)
    
    email = b''
    password = b''
    confirm_password = b''
    message = b''
    profile_picture_filename = b''
    xsrf_token = ""

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
            
            
        # For identifying the xsrf tokens
        if b'form-data; name="xsrf_token"' in data:
            find_xsrf_token = data.find(b'\r\n\r\n')
            xsrf_token = data[find_xsrf_token+4:len(data)-2].decode()

    print("email is: ", email, '\n')
    print("password is: ", password, '\n')
    print("confirm password is: ", confirm_password, '\n')
    print("Profile picture filename is: ", profile_picture_filename, '\n')

    if path == b'/login':
        handleLogin(TCP, email, password)
    if path == b'/register':
        handleRegistration(TCP, email, password, confirm_password)
    if path == b'/settings':
        handleProfilePicture(TCP, profile_picture_filename)

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
        server.MyTCPHandler.userCollection.insert_one({'email': email, 'salt':random_salt, 'hash': hashed})
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

'''
Handling the Profile Picture:
    - When handling the profile picture, the user must have submitted something.
    - If they have not submitted anything, they will issues the default profile picture of the cat.
    - If they have changed to something else, we will update it in the database.'''

def handleProfilePicture(TCP, profile_picture_filename):
    print("##########################")
    print("We are now handling the profile picture being updated")
    print("##########################", '\n')



def authenticateXSRF(TCP, xsrf_token):
    print("##########################")
    print("We are now handling the xsrf")
    print("##########################", '\n')

def retrieveAuthenticationToken(username):
    print("##########################")
    print("We are now retrieving the authenticated token")
    print("##########################", '\n')

