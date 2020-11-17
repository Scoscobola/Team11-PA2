# region ClientWorker

from threading import Thread
from socket import socket
from database import Database
from server import Server
from user import User


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
    def server(self):
        return self.__server

    @server.setter
    def server(self, server: Server):
        self.__server = server

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

    def sign_in_user(self, username: str, password: str):
        pass

    def sign_out_user(self):
        pass

    def run(self):
        pass

    def terminate_connection(self):
        pass

    def process_client_request(self, msg: str):
        pass

    def receive_message(self, max_length: int = 1024):
        pass

    def send_message(self, msg: str):
        pass

    # endregion

# endregion
