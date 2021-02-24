import requests, json, csv

class TargetUser:

    def __init__(self, trigger_user, target_username=None):
        if target_username is None:
            self.setTargetUsername()
        else:
            self.__target_username = target_username
        self.__trigger_user = trigger_user
        self.__userInf = self.__getUserInf()

    def setTargetUsername(self):
        self.__target_username = input("Please enter your target username: ")

    def __getUserInf(self):
        response = requests.get(f'https://www.instagram.com/{self.__target_username}/?__a=1', headers=self.__trigger_user.getAccessAPICookies())
        return json.loads(response.text)["graphql"]["user"]

    def getUserId(self):
        return self.__userInf["id"]

    def getUsername(self):
        return self.__target_username

