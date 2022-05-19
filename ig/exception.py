class UserLoginFailedException(Exception):
    def __init__(self, mes: str="Username or Password Incorrect"):
        super().__init__(mes)
        
class UserLoginChallengeFailed(UserLoginFailedException):
    def __init__(self, mes: str="Challenge Failed"):
        super().__init__(mes)
    
class SpamDetectedException(Exception):
    def __init__(self, mes: str="Spam Detected"):
        super().__init__(mes)

class RequestRateLimitedException(Exception):
    def __init__(self, mes: str="Request Rate Limited, instagram limited ~ 200 request") -> None:
        super().__init__(mes)
        
class RequestOverException(Exception):
    def __init__(self, mes: str="Over 200 requests, Please wait a few minutes before you try again.") -> None:
        super().__init__(mes)

class SelectContactPointRecoveryFormException(Exception):
    def __init__(self, mes: str="Your account may need to recovery, please login using your computer/mobile") -> None:
        super().__init__(mes)