#Team11-PA2

Sam Hilfer, Webster Kimoni, and Jack Lewis.

###Required Packages

* Threading
* Socket
* json
* queue

##Client App

The client app has a number of functionalities. The user will first want
to connect to the server. They'll be asked for an IP and Port and will 
then be asked for the port that the background thread in the client app
should listen for connections on. When the connection between the client
and client worker is established, a message with this extra port number
is sent to the client worker which then starts the background 
client worker. The background client worker connects to the server worker.
Once the user is signed in, they can select
the "login" option which then presents two sub-options. They can either
sign in an existing user or sign up a new user. Creating a new user prompts
the user for a username, password, and phone number. Once they enter that
information, a message is sent to the client worker. The client worker
verifies that a user with the username doesn't already exist and then creates
a new user and adds it to the database. If the user wants to sign in,
they provide username and password. The client sends a message to the 
client worker and the client worker verifies that a user with the
supplied credentials exists and that the user isn't already signed in. 
Once signed in, the user can send messages. Sending a message prompts
the user for the username of the user they want to contact, and the 
content of their message. The client then tells the client worker
the information needed to send the message. It confirms that both
users exist and then places the message in a queue in the database. 
The background client worker is constantly checking this queue to see if
the top message is meant for the currently logged in user. If it is,
it pops the message and sends it off to the clients background thread 
which then stores it in a list. The last thing the user can do is print
these received message from this list. When a message makes it to a 
users client background thread, a message in the form of a notification
is created and placed in another queue. The notification is meant to
notify the sending user that the receiving user did in fact get the 
message. Finally, the user can choose to disconnect which sends a 
message to the client worker telling it and the background client worker
to stop and close sockets. It also removes the reference to the client 
worker from the list in the server object.

##Server App

The server app has a number of functionalities. The first thing a user
can do is load a database object from a .json file. The user provides
a filename and the function deserializes the data in the dictionary
for reconstruction of a database object. Conversely, the user can save
the database object to a .json file. The function serializes all the
data which might have changed into dictionaries and puts it into a .json
file. The user once again is asked to provide a name for the file.
The file is saved to the current src folder. From there, the user can 
start the messenger service. A server thread is started which listens on
localhost and port 10001. It will continuously accept connections from 
clients, creating client worker threads as it goes. It keeps a list of 
client workers. The client worker is meant to handle requests from the
client and is also in charge of establishing the connection between
the background client worker and the server worker. Finally, the user can
stop the messenger service which stops the server from accepting more
connections and stops all client workers.