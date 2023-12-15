#User class, creates object for each user to be passed to oracle database


class User:
    user_id = 0

    def __init__(self, username, email, password, age):
        self._id = User.user_id + 1
        self._username = username
        self._email = email
        self._password = password
        self._age = age
        User.user_id += 1

    def __str__(self):
        return f"<User {self._username}>"
    
    def get_id(self):
        return self._id
    def get_username(self):
        return self._username
    def get_email(self):
        return self._email
    def get_password(self):
        return self._password
    def get_age(self):
        return self._age
    
    def set_id(self, id):
        self._id = id
    def set_username(self, username):
        self._username = username
    def set_email(self, email):
        self._email = email
    def set_password(self, pw):
        self._password = pw
    def set_age(self, age):
        self._age = age
