import random
class CSV2FollowingConfig:

    def __init__(self, time=None):
        print("The sleeping time is optional, if empty the sleeping time will randomly assign 190-600")
        if time is None:
            while True:
                user_input = float(input("Please enter the sleeping time (seconds): "))
                print("Program will assign more 0-150 seconds to reduce ban opportunity")
                if user_input == '':
                    self.__time = -1
                    break
                else:
                    try:
                        self.__time = float(user_input)
                        break
                    except ValueError:
                        print('Please input the numerical')
        else:
            self.__time = time

    def getConfig(self):
        return {
            "time": self.__time,
            "error_count": 5
        }

    def getSleepTime(self):
        if self.__time == -1:
            return random.uniform(190.0, 600.0)
        else
            return self.__time + random.uniform(0.0, 150.0)

