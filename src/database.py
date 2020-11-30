# region Database

from user import User
from message import Message
import queue

class Database:
    """Stores the messages and users."""

    def __init__(self, users=None, outgoing_messages=None, outgoing_notifications=None):
        if users is None:
            self.__users = []
            admin = User("admin", "admin", "1")
            self.__users.append(admin)
        else:
            self.__users = users

        if outgoing_messages is None:
            self.__outgoing_messages = queue.Queue()
        else:
            self.__outgoing_messages = outgoing_messages

        if outgoing_notifications is None:
            self.__outgoing_notifications = queue.Queue()
        else:
            self.__outgoing_notifications = outgoing_notifications

    # region Getters

    @property
    def users(self):
        return self.__users

    @property
    def outgoing_messages(self):
        return self.__outgoing_messages

    @property
    def outgoing_notifications(self):
        return self.__outgoing_messages

    # endregion

    # region Methods

    def sign_up_user(self, username: str, password: str, phone_number: str):
        """Checks to see that the username doesn't already exist and then adds the user to the database"""
        success = True
        response = ""
        # check that a user with this name doesn't exist.
        for user in self.__users:
            if username is user.username:
                success = False
                response = "A user with this username already exists."
                break
        # if we didn't already find a user, create a new user and add it to the list.
        if success:
            user_to_add = User(username, password, phone_number)
            self.__users.append(user_to_add)
            response = "OK"

        return response

    def send_message(self, user_from: User, user_to: User, message: str):
        """Checks that the user the message is being sent to exists, then sends the message and returns a response."""
        success = 0
        response = ''
        # check that the user sending the message exists.
        if user_from not in self.__users:
            success = 1
            response = f"""{success}|no source user"""
        # and that the user to exists
        elif user_to not in self.__users:
            success = 2
            response = f"""{success}|no target user"""

        # if both users exist, put this message into the outgoing message queue
        if success == 0:
            message_to_send = Message(user_from, user_to, message)
            self.__outgoing_messages.put(message_to_send)
            response = f"""{success}|{message_to_send.id}"""

        return response

    def send_notification(self, user_from: User, user_to: User, message_id: str):
        """Checks that the user the notification is being sent to exists,
        then sends the message and returns a response."""
        success = 0
        response = ''
        # check that the user that received the message exists
        if user_from not in self.__users:
            success = 1
            response = f"""{success}|no source user"""
        # check that the user that sent the message exists
        elif user_to not in self.__users:
            success = 2
            response = f"""{success}|no target user"""
        # if both exist, put notification in outgoing notification queue.
        if success == 0:
            message_to_send = Message(user_from, user_to, message_id)
            self.__outgoing_notifications.put(message_to_send)
            response = f"""{success}|Notification of relay sent to server."""

        return response

    def relay_message_to(self, user_from: User, message_id: int, message: str):
        pass

    def message_relayed(self, user_from: User, user_to: User, message_id: int):
        pass

    # We may not need these two methods. Just leave them until we know for sure.
    def save_to_file(self, filename: str):
        pass

    def load_from_file(self, filename: str):
        pass

    # endregion

# endregion
