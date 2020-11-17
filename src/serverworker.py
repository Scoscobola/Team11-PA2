# region ServerWorker

from socket import socket

from threading import Thread


class ServerWorker(Thread):
    """Background thread within the client that allows asynchronous sending and receiving of messages"""

    def __init__(self, client_socket: socket):
        super().__init__()
        self.__client_socket = client_socket
        self.__incoming_messages = []

    # region Getters and Setters

    @property
    def client_socket(self):
        return self.__client_socket

    @client_socket.setter
    def client_socket(self, client_socket: socket):
        self.__client_socket = client_socket

    @property
    def incoming_messages(self):
        return self.__incoming_messages

    # endregion

    # region Methods

    def receive_message(self, max_length: int = 1024):
        pass

    def run(self):
        pass

    # endregion

# endregion
