import requests
import json
import csv
import sys
import os
from command import Command
from file_manager import FileManager

class Following2CSV(Command):

    def __init__(self, target_user, trigger_user):
        super().__init__(trigger_user)
        self.__target_user = target_user
        self.__save_count = 0
        self.__query_hash = input("Please input the query_hash: ")

    def save(self):
        self.__following2JSON()

    def __following2JSON(self):
        if self.__query_hash is None or self.__query_hash == "":
            self.__query_hash = "3dec7e2c57367ef3da3d987d89f9dbc8"

        variables = {
            "id": self.__target_user.getUserId(),
            "include_reel": True,
            "fetch_mutual": False,
            "first": 50,
        }

        has_next_page = True
        count_request = 1

        while has_next_page:
            response = requests.get(
                f'https://www.instagram.com/graphql/query/?query_hash={self.__query_hash}&variables={json.dumps(variables)}',
                headers=self.getTriggerUser().getAccessAPICookies())
            jsonData = json.loads(response.text)
            print(jsonData)
            edge = jsonData["data"]["user"]["edge_follow"]
            users = edge["edges"]
            print(users)
            print(f"Request {count_request}:", len(users), "found")
            for userNode in users:
                user = userNode["node"]
                # user["biography"] = self.getUserBiography(user["username"], self.getTriggerUser())
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
            output_file_name = f'{self.__target_user.getUsername()}-following-{self.__query_hash}.csv'
            if self.__save_count == 0:
                if FileManager.file_exist(output_file_name):
                    user_input = input("The file is exits, you want to override it? (YES/no)")
                    if user_input == "no":
                        sys.exit()
                    elif user_input == "YES":
                        os.remove(output_file_name)

            with open(output_file_name, 'a+', encoding='utf-8-sig') as csvfile:
                writer = csv.DictWriter(csvfile, user.keys())
                if self.__save_count == 0:
                    writer.writeheader()
                    writer.writerow(user)
                else:
                    writer.writerow(user)
                self.__save_count += 1
        except IOError:
            print("I/O error")
