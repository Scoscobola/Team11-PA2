#region User

class User:
    """Stores user data"""

    def __init__(self, username: str, password: str, display_name: str):
        self.__username = username
        self.__password = password
        self.__display_name = display_name

    #region Getters and Setters

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, username: str):
        self.__username = username

    @property
    def display_name(self):
        return self.__display_name

    @display_name.setter
    def display_name(self, display_name: str):
        self.__display_name = display_name

    @property
    def password(self):
        return self.__password

    #endregion

#endregion