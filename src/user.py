#region User

class User:
    """Stores user data"""

    def __init__(self, username: str, password: str, phone: str):
        self.__username = username
        self.__password = password
        self.__display_name = phone

    #region Getters and Setters

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, username: str):
        self.__username = username

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, phone: str):
        self.__phone = phone

    @property
    def password(self):
        return self.__password

    #endregion

#endregion