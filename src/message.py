# region Message

class Message:
    """Stores message content and the message id"""

    ID = 1

    def __init__(self, content: str):
        self.__id = str(Message.ID).zfill(6)
        self.__content = content
        Message.ID += 1

    # region Getters and Setters

    @property
    def id(self):
        return self.__id

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, content):
        self.__content = content

    # endregion

    # region Utility

    @classmethod
    def reset_id_numbering(cls):
        cls.ID = 1

    # endregion

# endregion
