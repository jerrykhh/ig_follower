import requests, json
from datetime import datetime

class User:

    def __init__(self, username=None, password=None, user_agent=None):
        self.__username = username
        self.__password = password
        self.__user_agent = user_agent
        if self.checkInputDataIsNotNone():
            self.__csrftoken = self.__getLoginTOKEN()
        else:
            self.__csrftoken = None
        self.__loggined = False

    def getUsername(self):
        return self.__username

    def getPassword(self):
        return self.__password

    def getUserAgent(self):
        return self.__user_agent

    def setUsername(self, username=None):
        self.__username = username

    def setPassword(self, password=None):
        self.__password = password

    def setUserAgent(self, user_agent=None):
        self.__user_agent = user_agent

    def checkInputDataIsNotNone(self):
        return self.__username is not None and self.__password is not None and self.__user_agent is not None

    def __getLoginTOKEN(self):
        response = requests.get('https://www.instagram.com/accounts/login/', headers={'User-agent': self.__user_agent})
        token = response.cookies['csrftoken']
        print(f'Token: {token}')
        return token

    def getAccessAPICookies(self):
        if not self.__loggined:
            raise ValueError("User not login")
        return {
            "User-Agent": self.__user_agent,
            "Cookie": f"sessionid={self.__sessionId};csrftoken={self.__csrftoken}",
            "x-csrftoken": self.__csrftoken,
            "content-type": "application/x-www-form-urlencoded",
            "x-instagram-ajax": "9ad59a145017"

        }

    def login(self):
        if self.__csrftoken is None:
            self.__csrftoken = self.__getLoginTOKEN()

        if not self.__loggined:
            time = int(datetime.now().timestamp())
            response = requests.post("https://www.instagram.com/accounts/login/ajax/", data={
                'username': self.__username,
                'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{self.__password}',
                'queryParams': {},
                'optIntoOneTap': 'false'
            }, headers={
                "User-Agent": self.__user_agent,
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "https://www.instagram.com/accounts/login/",
                "x-csrftoken": self.__csrftoken
            })

            json_data = json.loads(response.text)
            try:
                if json_data["authenticated"]:
                    print("Login successful")
                    cookies = response.cookies
                    cookie_jar = cookies.get_dict()
                    self.__csrftoken = cookie_jar['csrftoken']
                    print("csrf_token:", self.__csrftoken)
                    self.__sessionId = cookie_jar['sessionid']
                    print("session_id:", self.__sessionId)
                    self.__loggined = True
                else:
                    raise ValueError("Login failed: username or password incorrect")
            except ValueError as e:
                raise e
            except Exception as e:
                raise TimeoutError("Please enter common User-agent")

        else:
            raise Exception("User is loggined")





