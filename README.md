# InstaChat

## Backend Task

#### Live on Heroku: [InstaChat](http://insta-chat-app.herokuapp.com/)

### Setup:

* You will need Python and Django to run this application
* Install all dependencies with this command
```
pip install -r requirements.txt
```
* Setup a MySQL Database with the configuration below
```
'NAME': 'InstaChat',
'USER': 'root', 
'PASSWORD': '',
'HOST': 'localhost',
'PORT': '3306'
```
* Run the commands in terminal from the directory where manage.py is located
```
python manage.py makemigrations
python manage.py migrate
```
* You can view the application in browser by typing in
```
http://localhost:8000/
```
### Tools:

* Python
* Django
* Django REST framework
* Websockets
* Redis as backing store for channels layer
* JSON Web Tokens
* MySQL Database 

### Features:
#### User authentication and session management
- User logs in to the application using username and password (Authentication will happen over HTTP using REST API) using Django REST framework.
- User doesn't need to login again unless he logs out.
- If user is logged in, no one can login using that account from another client.
- After logging in, user will land in a room called "lobby" where any one can chat.
#### One to One chat - the message sent would include only text
- Selects a username to send messages to, a connection is established between server and client for message transmission using websockets.
- If the receiver is offline then the messages will be encrypted and stored in the MySQL database and be delivered once the user is back online.
#### A web based interface to send, receive and view messages
- Interface developed using HTML, CSS, JavaScript, jQuery.
#### End-to-End encryption for chats
- If the receiver is online then the messages will be End-to-End encrypted using CryptoJS AES.
#### Deployed the application
- Deployed the application on Heroku - http://insta-chat-app.herokuapp.com/
