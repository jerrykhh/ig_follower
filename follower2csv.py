import requests, json, csv, time
from command import Command
from file_manager import FileManager


class Follower2CSV(Command):

    def __init__(self, target_user, trigger_user):
        super().__init__(trigger_user)
        self.__target_user = target_user
        self.__save_count = 0
        self.__query_hash = input("Please input the query_hash: ")

    def save(self):
        self.__follower2JSON()

    def __follower2JSON(self):
        if self.__query_hash is None or self.__query_hash == "":
            self.__query_hash = "5aefa9893005572d237da5068082d8d5"

        variables = {
            "id": self.__target_user.getUserId(),
            "include_reel": True,
            "fetch_mutual": False,
            "first": 50,
        }

        has_next_page = True
        count_request = 1
        userRecords = []

        while has_next_page :
            response = requests.get(f'https://www.instagram.com/graphql/query/?query_hash={self.__query_hash}&variables={json.dumps(variables)}', headers=self.getTriggerUser().getAccessAPICookies())
            jsonData = json.loads(response.text)
            print(jsonData)
            try:
                edge = jsonData["data"]["user"]["edge_followed_by"]
                users = edge["edges"]
                print(users)
                print(f"Request {count_request}:", len(users), "found")
                
                for userNode in users:
                    user = userNode["node"]
                    #user["biography"] = self.getUserBiography(user["username"], self.getTriggerUser())
                    del user["reel"]
                    userRecords.append(user)

                count_request += 1
                has_next_page = edge["page_info"]["has_next_page"]

                if has_next_page:
                    next_page_cursor = edge["page_info"]["end_cursor"]
                    variables["after"] = next_page_cursor
            except KeyError as e:
                print(e)
                if jsonData['status'] == 'fail':
                    print(jsonData)
                    print(f"Follower2CSV: Due to {jsonData['message']}, program will break 10 sec.")
                    time.sleep(10)
                    has_next_page = True

        FileManager.reponse_save_csv_file(userRecords, f'{self.__target_user.getUsername()}-follower-{self.__query_hash}.csv')


    @staticmethod
    def getUserBiography(username, trigger_user):
        response = requests.get(f'https://www.instagram.com/{username}/?__a=1',
                                headers=trigger_user.getAccessAPICookies())
        print("get Bio")
        jsonData = json.loads(response.text)
        return jsonData["graphql"]["user"]["biography"]

