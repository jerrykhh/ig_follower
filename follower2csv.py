import requests, json, csv
from command import Command


class Follower2CSV(Command):

    def __init__(self, target_user, trigger_user):
        super().__init__(trigger_user)
        self.__target_user = target_user
        self.__save_count = 0
        self.__query_hash = input("Please input the query_hash: ")

    def save(self):
        self.__follower2JSON()

    def __follower2JSON(self):
        if self.__query_hash is None:
            raise ValueError("Missing the query hash")

        variables = {
            "id": self.__target_user.getUserId(),
            "include_reel": True,
            "fetch_mutual": False,
            "first": 50,
        }

        has_next_page = True
        count_request = 1
        while has_next_page :
            response = requests.get(f'https://www.instagram.com/graphql/query/?query_hash={self.__query_hash}&variables={json.dumps(variables)}', headers=self.getTriggerUser().getAccessAPICookies())
            jsonData = json.loads(response.text)
            print(jsonData)
            edge = jsonData["data"]["user"]["edge_followed_by"]
            users = edge["edges"]
            print(users)
            print(f"Request {count_request}:", len(users), "found")
            for userNode in users:
                user = userNode["node"]
                #user["biography"] = self.getUserBiography(user["username"], self.getTriggerUser())
                del user["reel"]
                self.__save2CSV(user)

            count_request += 1
            has_next_page = edge["page_info"]["has_next_page"]

            if has_next_page:
                next_page_cursor = edge["page_info"]["end_cursor"]
                variables["after"] = next_page_cursor

        print(f'Finish: save {self.__save_count} rows')

    def __save2CSV(self, user):
        try:
            with open(f'{self.__target_user.getUsername()}-{self.__query_hash}.csv', 'a+', encoding='utf-8-sig') as csvfile:
                writer = csv.DictWriter(csvfile, user.keys())
                if self.__save_count == 0:
                    writer.writeheader()
                    writer.writerow(user)
                else:
                    writer.writerow(user)
                self.__save_count += 1
        except IOError:
            print("I/O error")

    @staticmethod
    def getUserBiography(username, trigger_user):
        response = requests.get(f'https://www.instagram.com/{username}/?__a=1',
                                headers=trigger_user.getAccessAPICookies())
        print("get Bio")
        jsonData = json.loads(response.text)
        return jsonData["graphql"]["user"]["biography"]

