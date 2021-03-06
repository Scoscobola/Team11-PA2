# region Server

# from clientworker import ClientWorker
from threading import Thread
import socket
from database import Database
from user import User
from background_clientworker import BackgroundClientWorker
import json
import queue
from message import Message


class Server(Thread):
    """Server main thread"""

    def __init__(self, ip: str, port: int, backlog: int):
        super().__init__()
        self.__ip = ip
        self.__port = port
        self.__backlog = backlog
        self.__server_socket = None
        self.__client_socket = None
        self.__keep_running = True
        self.__keep_running_client = True
        self.__database = Database()
        self.__list_of_cw = []
        self.__connection_count = 0

    # region Getters and setters

    @property
    def database(self):
        return self.__database

    @property
    def list_of_cw(self):
        return self.__list_of_cw

    @property
    def keep_running(self):
        return self.__keep_running

    @keep_running.setter
    def keep_running(self, status: bool):
        self.__keep_running = status

    # endregion

    # region Methods

    def terminate_server(self):
        """Turns off the loop in the run method and stops listening for connections."""
        self.__keep_running = False
        self.__server_socket.close()

    def run(self):
        """The method that runs when the thread is started. It listens for connections and accepts them as they come in,
        it starts a new client worker thread and adds it to a list."""
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server_socket.bind((self.__ip, self.__port))
        self.__server_socket.listen()

        while self.__keep_running:
            print(f"""[SRV] Waiting for a client connection""")
            try:
                self.__client_socket, client_address = self.__server_socket.accept()
                self.__connection_count += 1
                print(f"""[SRV] Got a connection from {client_address}""")
                cw = ClientWorker(self.__connection_count, self.__client_socket, self.__database, self)
                self.__list_of_cw.append(cw)
                cw.start()
            except Exception as e:
                print(e)

        cw: ClientWorker
        for cw in self.__list_of_cw:
            cw.terminate_connection()
            cw.join()

    def load_from_file(self):
        """Asks for the name of a .json file and loads it as the database for the server."""
        filename = input("Enter the name of the file you'd like to load (no file extension)>")
        try:
            with open(f"{filename}.json", "r") as database_file:
                database_dict = json.load(database_file)
        except FileNotFoundError as fe:
            print(fe)
            return

        users_list = []
        for user_dict in database_dict["user_dict"]:
            user = User(user_dict.get("_User__username"), user_dict.get("_User__password"),
                        user_dict.get("_User__phone"))
            users_list.append(user)

        messages_queue = []
        for message_dict in database_dict["messages_dict"]:
            user_from_dict = message_dict["_Message__user_from"]
            user_to_dict = message_dict["_Message__user_to"]
            user_from = User(user_from_dict.get("_User__username"), user_from_dict.get("_User__password"),
                             user_from_dict.get("_User__phone"))
            user_to = User(user_to_dict.get("_User__username"), user_to_dict.get("_User__password"),
                           user_to_dict.get("_User__phone"))
            message_to_put = Message(user_from, user_to, message_dict.get("_Message__content"))
            messages_queue.append(message_to_put)

        notification_queue = []
        for notification_dict in database_dict["notifications_dict"]:
            user_from_dict = notification_dict["_Message__user_from"]
            user_to_dict = notification_dict["_Message__user_to"]
            user_from = User(user_from_dict.get("_User__username"), user_from_dict.get("_User__password"),
                             user_from_dict.get("_User__phone"))
            user_to = User(user_to_dict.get("_User__username"), user_to_dict.get("_User__password"),
                           user_to_dict.get("_User__phone"))
            message_to_put = Message(user_from, user_to, notification_dict.get("_Message__content"))
            messages_queue.append(message_to_put)

        self.__database = Database(users_list, messages_queue, notification_queue)

    def save_to_file(self):
        """Saves the database in the server to a .json file."""
        database_dict = {"user_dict": [], "messages_dict": [], "notifications_dict": []}
        for user in self.__database.users:
            serialized_user = user.__dict__
            database_dict["user_dict"].append(serialized_user)
        for message in self.__database.outgoing_messages:
            serialized_message = {"id": message.id, "user_to": {message.user_to.__dict__},
                                  "user_from": {message.user_from.__dict__}, "content": message.content}
            database_dict["messages_dict"].append(serialized_message)
        for notification in self.__database.outgoing_notifications:
            serialized_notification = {"id": notification.id, "user_to": {notification.user_to.__dict__},
                                       "user_from": {notification.user_from.__dict__}, "content": notification.content}
            database_dict["messages_dict"].append(serialized_notification)

        filename = input("Name the file you want to save the database to (no file extension)>")
        try:
            with open(f'{filename}.json', 'w') as database_file:
                json.dump(database_dict, database_file)
        except Exception as e:
            print(e)

    def display_menu(self):
        """Used to display the options available to the server app."""
        print("=" * 80)
        print(f"""{"Server Main Menu"}:^80""")
        print("=" * 80)
        print("1. Load data from file")
        print("2. Start messenger service")
        print("3. Stop messenger service")
        print("4. Save data to file")
        print("-" * 80)
        return int(input("Select option [1-4]>"))

    # endregion


# endregion

# region ClientWorker
class ClientWorker(Thread):
    """Threads that listen to client requests."""

    def __init__(self, client_id: int, client_socket: socket, database: Database, server: Server):
        super().__init__()
        self.__id = client_id
        self.__client_socket = client_socket
        self.__database = database
        self.__server = server
        self.__user = None
        self.__keep_running_client = True
        self.__background_client_worker = BackgroundClientWorker()

    # region Setters and Getters
    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, client_id: int):
        self.__id = client_id

    @property
    def client_socket(self):
        return self.__client_socket

    @client_socket.setter
    def client_socket(self, client_socket: socket):
        self.__client_socket = client_socket

    @property
    def database(self):
        return self.__database

    @database.setter
    def database(self, database: Database):
        self.__database = database

    @property
    def user(self):
        return self.__user

    @property
    def server(self):
        return self.__server

    @server.setter
    def server(self, server: Server):
        self.__server = server

    @user.setter
    def user(self, user: User):
        self.__user = user

    @property
    def keep_running_client(self):
        return self.__keep_running_client

    @keep_running_client.setter
    def keep_running_client(self, state: bool):
        self.__keep_running_client = state

    # endregion

    # region Methods

    def sign_in_user(self, username: str, password: str):
        """Takes a username and password and checks that a user exists with the matching credentials. It also checks
        that the user isn't signed in elsewhere."""
        user_to_sign_in = None
        response = ""
        user: User
        cw: ClientWorker
        signed_in = False
        # search for user where the username and password match
        for user in self.__database.users:
            if user.username == username and user.password == password:
                # then search thru the list of connected clients to make sure the user isn't already signed in
                for cw in self.__server.list_of_cw:
                    if cw.user is user:
                        response = "2|Already signed in."
                        signed_in = True
                        break
                # if the user isn't already signed in...
                if not signed_in:
                    self.__user = user
                    self.__background_client_worker.user = user
                    self.display_message(f"Successfully signed in {self.__user.username}")
                    response = "0|OK"
            # if the user name matches but the password doesn't...
            elif user.username is username and password is not user.password:
                self.display_message("Incorrect password")
                response = "1|Invalid Credentials"
        # if the user isn't found...
        if not self.__user:
            self.display_message("That user doesn't exist")
            response = "1|That user doesn't exist."

        return response

    def sign_out_user(self):
        pass

    def connect_to_client_background(self, port):
        """This method is called when the client-clientworker connection is established and the clientworker
        receives a message with the port the server worker is listening on."""
        self.__background_client_worker.client_socket = self.__client_socket
        self.__background_client_worker.database = self.__database
        self.__background_client_worker.port = port
        self.__background_client_worker.start()

    def run(self):
        """The method called when the thread is started. It continuously tried to process client requests."""
        self.display_message("Connected to Client. Attempting connection to client background thread")
        while self.__keep_running_client:
            self.process_client_request()

        self.__client_socket.close()
        for client in self.__server.list_of_cw:
            if client.id == self.__id:
                self.__server.list_of_cw.remove(client)

    def terminate_connection(self):
        """Called when the user disconnects. It tells the loop in the run method to stop, and then asks the
        server worker to terminate."""
        self.__keep_running_client = False
        self.__background_client_worker.terminate_connection()
        return "0|OK"

    def process_client_request(self):
        """Receive messages from the client, process them accordingly, and then send a response."""
        client_message = self.receive_message()
        self.display_message(f"""CLIENT SAID >> {client_message}""")

        arguments = client_message.split("|")
        response = ""

        try:
            if arguments[0] == "PORT":
                # Need to figure out how to handle response here. The background clientworker may need to time out
                # after a certain number of tries.
                self.connect_to_client_background(int(arguments[1]))
                response = "OK"
            elif arguments[0] == "LOG":
                response = self.sign_in_user(arguments[1], arguments[2])
            elif arguments[0] == "USR":
                response = self.database.sign_up_user(arguments[1], arguments[2], arguments[3])
            elif arguments[0] == "MSG":
                response = self.database.send_message(arguments[1], arguments[2], arguments[3])
            elif arguments[0] == "OUT":
                response = self.terminate_connection()
            else:
                response = "ERR|Unknown Command."
        except ValueError as ve:
            response = "ERR|" + str(ve)

        self.send_message(response)

    def receive_message(self, max_length: int = 1024):
        """Receive a message from the client."""
        msg = self.__client_socket.recv(max_length).decode("UTF-8")
        while "\n" not in msg:
            msg += self.__client_socket.recv(max_length).decode("UTF-8")
        print(f"""RECV>> {msg}""")
        return msg.rstrip()

    def send_message(self, msg: str):
        """Send a response back to the client."""
        msg += "\n"
        self.display_message(f"""SEND>> {msg}""")
        self.__client_socket.send(msg.encode("UTF-8"))

    def display_message(self, msg: str):
        """Prints a message out."""
        print(f"""CW >> {msg}""")

    # endregion


# endregion

# region ServerApp

if __name__ == "__main__":
    keep_running = True
    server = Server("localhost", 10001, 20)

    while keep_running:
        option = server.display_menu()
        if option == 1:
            server.load_from_file()
        elif option == 2:
            server.start()
        elif option == 3:
            server.terminate_server()
            server.join()
            keep_running = False
        elif option == 4:
            server.save_to_file()
        elif option == 9:
            print(len(server.list_of_cw))
        else:
            print("Invalid option, try again \n\n")

# endregion
