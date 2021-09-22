from command import Command
from file_manager import FileManager
from datetime import datetime
import requests
import json
import time

class Like2CSV(Command):

    def __init__(self, trigger_user, post:list):
        super().__init__(trigger_user)
        self.__post = post
        self.save_count = 0
        self.__query_hash = input("Please input the query_hash: ")
        

    def save(self):
        for postId in self.__post:
            self.__like2JSON(postId)
            print("break 5 sec, due to avoid to ban account")
            time.sleep(5)

    def __like2JSON(self, postId):
        if self.__query_hash is None or self.__query_hash == "":
            self.__query_hash = "d5d763b1e2acf209d62d22d184488e57"

        variables = {
            "shortcode": postId,
            "include_reel": True,
            "first": 50,
        }

        has_next_page = True
        count_request = 1
        userRecords = []

        while has_next_page:
            response = requests.get(
                f'https://www.instagram.com/graphql/query/?query_hash={self.__query_hash}&variables={json.dumps(variables)}',
                headers=self.getTriggerUser().getAccessAPICookies())
            jsonData = json.loads(response.text)
            print(jsonData)
            edge = jsonData["data"]["shortcode_media"]["edge_liked_by"]
            users = edge["edges"]
            print(users)
            print(f"Request {count_request}:", len(users), "found")

            for userNode in users:
                user = userNode["node"]
                # user["biography"] = self.getUserBiography(user["username"], self.getTriggerUser())
                del user["reel"]
                userRecords.append(user)
                

            count_request += 1
            has_next_page = edge["page_info"]["has_next_page"]

            if has_next_page:
                next_page_cursor = edge["page_info"]["end_cursor"]
                variables["after"] = next_page_cursor
        
        FileManager.reponse_save_csv_file(userRecords, f'likes-{postId}.csv')