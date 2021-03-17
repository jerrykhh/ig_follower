
class CSV2FollowingConfig:

    def __init__(self, time=None):
        if time is None:
            self.__time = float(input("Please enter the sleeping time (30min = 60sec * 30min = input 1800): "))
        else:
            self.__time = time

    def getConfig(self):
        return {
            "time": self.__time,
            "error_count": 10
        }
