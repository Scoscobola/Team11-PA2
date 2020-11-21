# region Client

from serverworker import ServerWorker
import socket
import random


class Client:
    """The main client thread"""

    def __init__(self, ip: str = None, port: int = None):
        self.__ip = ip
        self.__port = port
        self.__client_socket = None
        self.__server_worker = None
        self.__is_connected = False

    # region Getters and Setters

    @property
    def ip(self):
        return self.__ip

    @ip.setter
    def ip(self, ip: str):
        self.__ip = ip

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, port: int):
        self.__port = port

    # endregion

    # region Methods

    def connect(self):
        #Connect to the server
        self.__client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client_socket.connect((self.__ip, self.__port))
        self.__is_connected = True

        #Generate a random port number and instatiate a background thread with a socket listening to the random port
        random_port = random.randrange(10002, 10010)
        self.__server_worker = ServerWorker(random_port)
        self.__server_worker.start()
        self.send_message(f"""PORT|{str(random_port)}""")

    def disconnect(self):
        self.__client_socket.close()
        self.__server_worker.terminate_connection()
        self.__is_connected = False

    def send_message(self, msg: str):
        self.__client_socket.send(msg.encode("UTF-16"))

    def receive_message(self):
        return self.__client_socket.recv(1024)[0].decode("UTF-16")

    def print_received(self):
        pass

    def sign_in_user(self, username: str, password: str):
        pass

    def display_menu(self):
        print("=" * 80)
        print(f"""{"Client Main Menu"}:^80""")
        print("=" * 80)
        print("1. Connect to server")
        print("2. Login")
        print("3. Send Message")
        print("4. Print Received Messages")
        print("5. Disconnect")
        print("-" * 80)
        return int(input("Select option [1-5/9]>"))

    # endregion


# endregion

# region ClientApp

if __name__ == "__main__":
    keep_running = True
    client = Client()

    while keep_running:
        option = client.display_menu()
        if option == 1:
            client.ip = input("IP Address>")
            client.port = int(input("Port>"))
            client.connect()
            print(client.receive_message())
        else:
            print("Invalid option, try again \n\n")

# endregion
