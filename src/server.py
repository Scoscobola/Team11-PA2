# region Server
class Server:
    """Server main thread"""

    def __init__(self, ip: str, port: int, backlog: int):
        self.__ip = ip
        self.__port = port
        self.__backlog = backlog
        self.__server_socket = None
        self.__client_socket = None
        self.__keep_running = True
        self.__keep_running_client = True
        self.__database = Database
        self.__list_of_cw = []
        self.__connection_count = 0

    # region Methods

    def terminate_server(self):
        pass

    def run(self):
        pass

    def load_from_file(self, filename: str):
        pass

    def save_to_file(self, filname: str):
        pass

    def display_menu(self):
        pass

    # endregion


# endregion


# region ServerApp


if __name__ == "__main__":
    pass

# endregion
