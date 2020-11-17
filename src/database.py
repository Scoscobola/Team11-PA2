# region Database

from user import User


class Database:
    """Stores the messages and users."""

    def __init__(self, users=None, outgoing_messages=None):
        if users is None:
            self.__users = []
        else:
            self.__users = users

        if outgoing_messages is None:
            self.__outgoing_messages = []
        else:
            self.__outgoing_messages = outgoing_messages

    # region Methods

    def sign_up_user(self, username: str, password: str, display_name: str):
        pass

    def send_message(self, user_from: User, user_to: User, message: str):
        pass

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
