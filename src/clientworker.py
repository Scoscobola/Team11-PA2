# # region ClientWorker
#
# from threading import Thread
# import socket
# from database import Database
# from server import Server
# from user import User
# from background_clientworker import BackgroundClientWorker
#
#
# class ClientWorker(Thread):
#     """Threads that listen to client requests."""
#
#     def __init__(self, client_id: int, client_socket: socket, database: Database, server: Server):
#         super().__init__()
#         self.__id = client_id
#         self.__client_socket = client_socket
#         self.__database = database
#         self.__server = server
#         self.__user = None
#         self.__keep_running_client = True
#         self.__background_client_worker = None
#
#     # region Setters and Getters
#     @property
#     def id(self):
#         return self.__id
#
#     @id.setter
#     def id(self, client_id: int):
#         self.__id = client_id
#
#     @property
#     def client_socket(self):
#         return self.__client_socket
#
#     @client_socket.setter
#     def client_socket(self, client_socket: socket):
#         self.__client_socket = client_socket
#
#     @property
#     def database(self):
#         return self.__database
#
#     @database.setter
#     def database(self, database: Database):
#         self.__database = database
#
#     @property
#     def user(self):
#         return self.__user
#
#     # @property
#     # def server(self):
#     #     return self.__server
#     #
#     # @server.setter
#     # def server(self, server: Server):
#     #     self.__server = server
#
#     @property
#     def user(self):
#         return self.__user
#
#     @user.setter
#     def user(self, user: User):
#         self.__user = user
#
#     @property
#     def keep_running_client(self):
#         return self.__keep_running_client
#
#     @keep_running_client.setter
#     def keep_running_client(self, state: bool):
#         self.__keep_running_client = state
#
#     # endregion
#
#     # region Methods
#
#     def sign_in_user(self, username: str, password: str):
#         user_to_sign_in = None
#         response = ""
#         user: User
#         cw: ClientWorker
#         signed_in = False
#         for user in self.__database.users:
#             if user.username is username and password is user.password:
#                 for cw in self.__server.list_of_cw:
#                     if cw.user is user:
#                         response = "2|Already signed in."
#                         signed_in = True
#                         break
#                 if not signed_in:
#                     self.__user = user
#                     self.display_message(f"Successfully signed in {self.__user.display_name}")
#                     response = "0|OK"
#             elif user.username is username and password is not user.password:
#                 self.display_message("Incorrect password")
#                 response = "1|Invalid Credentials"
#
#         if not self.__user:
#             self.display_message("That user doesn't exist")
#             response = "1|Invalid Credentials"
#
#         self.send_message(response)
#
#     def sign_out_user(self):
#         pass
#
#     def connect_to_client_background(self, port):
#         #print(f"""{str(self.__client_socket.getpeername()[0])}{port}""")
#         self.__background_client_worker = BackgroundClientWorker(self.__client_socket, self.__database, self.__user,
#                                                                  port)
#         self.__background_client_worker.run()
#
#     def run(self):
#         self.display_message("Connected to Client. Attempting connection to client background thread")
#
#         while self.__keep_running_client:
#             self.process_client_request()
#
#         self.__client_socket.close()
#
#     def terminate_connection(self):
#         self.__keep_running_client = False
#         self.__client_socket.close()
#         #self.__server_socket.close()
#
#     def process_client_request(self):
#         client_message = self.receive_message()
#         self.display_message(f"""CLIENT SAID >> {client_message}""")
#
#         arguments = client_message.split("|")
#         response = ""
#
#         try:
#             if arguments[0] == "PORT":
#                 #Need to figure out how to handle response here. The background clientworker may need to time out
#                 #after a certain number of tries.
#                 self.connect_to_client_background(int(arguments[1]))
#             if arguments[0] == "LOG":
#                 self.sign_in_user(arguments[1], arguments[2])
#                 response = self.sign_in_user()
#             else:
#                 response = "ERR|Unknown Command."
#         except ValueError as ve:
#             response = "ERR|" + str(ve)
#
#         self.send_message(response)
#
#     def receive_message(self, max_length: int = 1024):
#         msg = self.__client_socket.recvmsg(max_length)[0].decode("UTF-16")
#         print(f"""RECV>> {msg}""")
#         return msg
#
#     def send_message(self, msg: str):
#         self.display_message(f"""SEND>> {msg}""")
#         self.__client_socket.send(msg.encode("UTF-16"))
#
#     def display_message(self, msg: str):
#         print(f"""CW >> {msg}""")
#
#     # endregion
#
# # endregion
