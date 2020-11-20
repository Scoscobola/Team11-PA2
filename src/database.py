# region Database

from user import User
from message import Message
import queue

class Database:
    """Stores the messages and users."""

    def __init__(self, users=None, outgoing_messages=None, outgoing_notifications=None):
        if users is None:
            self.__users = []
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

    def sign_up_user(self, username: str, password: str, display_name: str):
        """Checks to see that the username doesn't already exist and then adds the user to the database"""
        success = True
        for user in self.__users:
            if username is user.username:
                success = False
                break
        if success:
            user_to_add = User(username, password, display_name)
            self.__users.append(user_to_add)

        return success

    def send_message(self, user_from: User, user_to: User, message: str):
        """Checks that the user the message is being sent to exists then sends the message and returns a response."""
        success = 0
        response = ''
        if user_from not in self.__users:
            success = 1
            response = f"""{success}|no source user"""
        elif user_to not in self.__users:
            success = 2
            response = f"""{success}|no target user"""

        if success == 0:
            message_to_send = Message(user_from, user_to, message)
            self.__outgoing_messages.put(message_to_send)
            response = f"""{success}|{message_to_send.id}"""

        return response

    def send_notification(self, user_from: User, user_to: User, message_id: str):
        """Checks that the user the message is being sent to exists then sends the message and returns a response."""
        success = 0
        response = ''
        if user_from not in self.__users:
            success = 1
            response = f"""{success}|no source user"""
        elif user_to not in self.__users:
            success = 2
            response = f"""{success}|no target user"""

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
