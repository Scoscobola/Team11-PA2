# region Database

from user import User
from message import Message
import threading

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
            self.__outgoing_messages = []
        else:
            self.__outgoing_messages = outgoing_messages

        if outgoing_notifications is None:
            self.__outgoing_notifications = []
        else:
            self.__outgoing_notifications = outgoing_notifications

        self.__locks = {"outgoing_messages": threading.Lock(), "outgoing_notifications": threading.Lock()}

    # region Getters

    @property
    def users(self):
        return self.__users

    @property
    def outgoing_messages(self):
        return self.__outgoing_messages


    @property
    def outgoing_notifications(self):
        return self.__outgoing_notifications

    @property
    def locks(self):
        return self.__locks

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
                response = "1|A user with this username already exists."
                break
        # if we didn't already find a user, create a new user and add it to the list.
        if success:
            user_to_add = User(username, password, phone_number)
            self.__users.append(user_to_add)
            response = "0|OK"

        return response

    def send_message(self, name_from: str, name_to: str, message: str):
        """Checks that both users exist, then constructs the message and puts it in the outgoing queue."""
        user_from_found = False
        user_to_found = False
        user_obj_from = None
        user_obj_to = None
        response = ''
        # check that the user sending the message exists.
        for user in self.__users:
            if name_from == user.username:
                user_from_found = True
                user_obj_from = user
                break
            else:
                response = f"""1|no source user"""
        # and that the user to exists
        for user in self.__users:
            if name_to == user.username:
                user_to_found = True
                user_obj_to = user
                break
            else:
                response = f"""2|no target user"""

        # if both users exist, put this message into the outgoing message queue
        if user_to_found and user_from_found:
            message_to_send = Message(user_obj_from, user_obj_to, message)
            self.__locks["outgoing_messages"].acquire()
            self.__outgoing_messages.insert(0, message_to_send)
            self.__locks["outgoing_messages"].release()
            response = f"""0|{message_to_send.id}"""

        return response

    def send_notification(self, user_from: User, user_to: User, message_id: str):
        """This method is called when a background client worker takes a message from the databases outgoing
        message queue. This method checks both users exist, and then constructs a message such that the
        content of the message is the id of the message that was seen by the background client worker. It then
        puts the new message in the outgoing notifications queue."""
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
            self.__locks["outgoing_notifications"].acquire()
            self.__outgoing_notifications.insert(0, message_to_send)
            self.__locks["outgoing_notifications"].release()
            response = f"""{success}|Notification of relay sent to server."""

        return response

    # endregion

# endregion
