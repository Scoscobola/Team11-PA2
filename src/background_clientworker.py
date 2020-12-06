# region ClientWorker
import time
from threading import Thread
import socket
from database import Database
# from server import Server
from user import User


class BackgroundClientWorker(Thread):
    """Threads that listen to client requests."""

    def __init__(self, client_socket: socket = None, database: Database = None, user: User = None, port: int = None):
        super().__init__()
        self.__client_socket = client_socket
        self.__server_socket = None
        self.__port = port
        self.__database = database
        # self.__server = server
        self.__user = user
        self.__keep_running_client = True

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
    def port(self):
        return self.__port

    @port.setter
    def port(self, port: int):
        self.__port = port

    # @property
    # def server(self):
    #     return self.__server
    #
    # @server.setter
    # def server(self, server: Server):
    #     self.__server = server

    @property
    def user(self):
        return self.__user

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

    def run(self):
        self.display_message("Connected to Client. Attempting connection to client background thread")
        while True:
            try:
                self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.__server_socket.connect((str(self.__client_socket.getpeername()[0]), self.__port))
                # self.__client_socket.send("OK|".encode("UTF-16"))
                self.display_message("Successfully connected to client's server worker.")
                break
            except socket.error as se:
                print("Connection refused. Retrying...")
                time.sleep(2)

        while self.__keep_running_client:
            self.check_for_messages()
            # time.sleep(5)
        self.__server_socket.close()

    def terminate_connection(self):
        self.__keep_running_client = False
        self.send_message("OUT|OK")

    def check_for_messages(self):
        if not list(self.__database.outgoing_messages.queue):
            # self.display_message("Outgoing Messages queue empty.")
            pass
        elif list(self.__database.outgoing_messages.queue)[-1].user_to is self.__user:
            message_obj = self.__database.outgoing_messages.get()
            message = f"""R|{message_obj.user_from.username}|{message_obj.id}|{message_obj.content}"""
            self.send_message(message)
            self.display_message(self.receive_message())
            self.display_message(self.__database.send_notification(message_obj.user_from, message_obj.user_to,
                                                                   message_obj.id))

        if not list(self.__database.outgoing_notifications.queue):
            # self.display_message("Outgoing notification queue empty")
            pass
        elif list(self.__database.outgoing_notifications.queue)[-1].user_from is self.__user:
            message_obj = self.__database.outgoing_notifications.get()
            message = f"""OK|{message_obj.user_from.username}|{message_obj.user_to.username}|{message_obj.content}"""
            self.send_message(message)
            self.display_message(self.receive_message())

    def receive_message(self, max_length: int = 1024):
        msg = self.__server_socket.recv(max_length).decode("UTF-8")
        print(f"""RECV (BG)>> {msg}""")
        return msg

    def send_message(self, msg: str):
        self.display_message(f"""SEND (BG)>> {msg}""")
        self.__server_socket.send(msg.encode("UTF-8"))

    def display_message(self, msg: str):
        print(f"""BGCW >> {msg}""")

    # endregion

# endregion
