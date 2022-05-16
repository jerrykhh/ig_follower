class UserLoginFailedException(Exception):
    def __init__(self, mes: str="Username or Password Incorrect"):
        super().__init__(mes)
        
class UserLoginChallengeFailed(UserLoginFailedException):
    def __init__(self, mes: str="Challenge Failed"):
        super().__init__(mes)
    
class SpamDetectedException(Exception):
    def __init__(self, mes: str="Spam Detected"):
        super().__init__(mes)