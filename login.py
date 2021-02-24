from user import User
import getpass


class Login:

    def __init__(self, args=None):
        if args is None:
            self.user = User()
        else:
            self.user = User(args[1], args[2])

    def display(self):
        if self.user.getUserAgent() is None:
            input_user_agent = input("Please enter your User-Agent: ")
            self.user.setUserAgent(input_user_agent)

        if self.user.getUsername() is None:
            input_username = input("Please enter your username: ")
            self.user.setUsername(input_username)

        if self.user.getPassword() is None:
            input_password = getpass.getpass("Please enter your password: ")
            self.user.setPassword(input_password)

    def login(self):
        while not self.user.checkInputDataIsNotNone():
            self.display()
        self.user.login()

    def getUser(self):
        return self.user
