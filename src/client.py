# region Client

from serverworker import ServerWorker


class Client:
    """The main client thread"""

    def __init__(self, ip: str, port: int):
        self.__ip = ip
        self.__port = port
        self.__client_socket = None
        self.__server_worker = None
        self.__is_connected = False

    # region Methods

    def connect(self):
        pass

    def disconnect(self):
        pass

    def send_message(self, msg: str):
        pass

    def print_received(self):
        pass

    def sign_in_user(self, username: str, password: str):
        pass

    def display_menu(self):
        pass

    # endregion


# endregion

# region ClientApp

if __name__ == "__main__":
    pass

# endregion
