import requests, json, csv

class TargetUser:

    def __init__(self, target_username, trigger_user):
        self.__save_count = 0
        self.__target_username = target_username
        self.__trigger_user = trigger_user
        self.__userInf = self.__getUserInf()
        self.__query_hash = None

    def __getUserInf(self):
        response = requests.get(f'https://www.instagram.com/{self.__target_username}/?__a=1', headers=self.__trigger_user.getAccessAPICookies())
        return json.loads(response.text)["graphql"]["user"]

    def getUserId(self):
        return self.__userInf["id"]

    def follower2JSON(self):
        if self.__query_hash is None:
            raise ValueError("Missing the query hash")

        variables = {
            "id": self.getUserId(),
            "include_reel": True,
            "fetch_mutual": False,
            "first": 50,
        }

        has_next_page = True
        count_request = 1
        while(has_next_page):
            response = requests.get(f'https://www.instagram.com/graphql/query/?query_hash={self.__query_hash}&variables={json.dumps(variables)}', headers=self.__trigger_user.getAccessAPICookies())
            jsonData = json.loads(response.text)
            print(jsonData)
            edge = jsonData["data"]["user"]["edge_followed_by"]
            users = edge["edges"]
            print(users)
            print(f"Request {count_request}:", len(users), "found")
            for userNode in users:
                user = userNode["node"]
                #user["biography"] = self.getUserBiography(user["username"], self.__trigger_user)
                del user["reel"]
                self.save2CSV(user)

            count_request += 1
            has_next_page = edge["page_info"]["has_next_page"]

            if has_next_page:
                next_page_cursor = edge["page_info"]["end_cursor"]
                variables["after"] = next_page_cursor

        print(f'Finish: save {self.__save_count - 1} rows')

    def save2CSV(self, user):
        try:
            with open(f'{self.__target_username}-{self.__query_hash}.csv', 'a+', encoding='utf-8-sig') as csvfile:
                writer = csv.DictWriter(csvfile, user.keys())
                if self.__save_count == 0:
                    writer.writeheader()
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

    def setQueryHash(self, query_hash):
        self.__query_hash = query_hash
