import csv
import json
import requests
import time
from datetime import datetime
from CSV2Following_config import CSV2FollowingConfig
from command import Command
from file_manager import FileManager


class CSV2Following(Command):

    def __init__(self, trigger_user, file_path=None):
        super().__init__(trigger_user)
        self.__file_manager = FileManager(file_path)
        self.__config = CSV2FollowingConfig()
        self.__line_count = 0
        requests.adapters.DEFAULT_RETRIES = 5

    def follow(self):
        with open(self.__file_manager.getFilePath(), mode="r", encoding='utf-8-sig') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            error_count = 0
            for row in csv_reader:
                if self.__line_count == 0:
                    print(f'CSV: column names are {", ".join(row)}')
                try:
                    response = requests.post(f"https://www.instagram.com/web/friendships/{row['id']}/follow/",
                                             headers=self.getTriggerUser().getAccessAPICookies())
                    jsonData = json.loads(response.text)
                    now = datetime.now()
                    if jsonData["spam"] == True or jsonData["spam"] == "True" :
                        print("Error: Instagram blocked your account follow function. Program will end.")
                        exit()
                    if jsonData["result"] == "requested":
                        print(f'CSV2Following: requested {row["username"]}({row["id"]}) at {now}')
                    elif jsonData["result"] == "following":
                        print(f'CSV2Following: following {row["username"]}({row["id"]}) at {now}')
                    else:
                        print(f'CSV2Following: Error {row["username"]}({row["id"]}) at {now}')
                    self.__line_count += 1
                    response.close()
                except:
                    error_count += 1
                    if error_count == self.__config.getConfig()["error_count"]:
                        print(f"Failed {error_count} times, it will sleep 3 hours")
                        time.sleep(60*60*3)
                    elif error_count == self.__config.getConfig()["error_count"]+1:
                        print("Program end: Due to the server request blocked")
                        exit()
                    else:
                        print("Request Error: Due to the server request blocked, it will sleep 10min")
                        time.sleep(600)
                        print("Login again.")
                        try:
                            self.getTriggerUser().restartSession()
                        except:
                            print("Session Restart Failed, the program will End")
                            exit()
                time.sleep(self.__config.getConfig()["time"])
            print(f'Processed {self.__line_count} lines.')

    @staticmethod
    def fitting(file_path):
        ordered_dict_list = []
        with open(file_path, mode="r", encoding='utf-8-sig') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            total_row_count = 0
            total_followed_count = 0
            for row in csv_reader:
                if row["followed_by_viewer"].lower() == 'true' or row["requested_by_viewer"].lower() == 'true':
                    total_followed_count += 1
                else:
                    ordered_dict_list.append(row)
                total_row_count += 1

            FileManager.save_csv_file(ordered_dict_list, "fitting-" + file_path)
            print(f"CSV2Following(CSV: {file_path}): {total_row_count} rows found, {total_followed_count} rows is "
                  f"followed or requested")
