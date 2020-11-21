# region Server

import socket
from clientworker import ClientWorker
from database import Database

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
        self.__database = Database()
        self.__list_of_cw = []
        self.__connection_count = 0

    # region Methods

    def terminate_server(self):
        self.__keep_running = False
        self.__server_socket.close()

    def run(self):
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server_socket.bind((self.__ip, self.__port))
        self.__server_socket.listen()

        while self.__keep_running:
            print(f"""[SRV] Waiting for a client connection""")
            try:
                self.__client_socket, client_address = self.__server_socket.accept()
                self.__connection_count += 1
                print(f"""[SRC] Got a connection from {client_address}""")
                cw = ClientWorker(self.__connection_count, self.__client_socket, self.__database)
                self.__list_of_cw.append(cw)
                cw.start()
            except Exception as e:
                print(e)

        cw: ClientWorker
        for cw in self.__list_of_cw:
            cw.terminate_connection()
            cw.join()

    def load_from_file(self, filename: str):
        pass

    def save_to_file(self, filname: str):
        pass

    def display_menu(self):
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


# region ServerApp


if __name__ == "__main__":
    keep_running = True
    server = Server("localhost", 10001, 20)

    while keep_running:
        option = server.display_menu()
        if option == 2:
            server.run()
        else:
            print("Invalid option, try again \n\n")

# endregion
