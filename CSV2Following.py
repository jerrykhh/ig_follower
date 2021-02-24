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

    def follow(self):
        with open(self.__file_manager.getFilePath(), mode="r", encoding='utf-8-sig') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if self.__line_count == 0:
                    print(f'CSV: column names are {", ".join(row)}')
                response = requests.post(f"https://www.instagram.com/web/friendships/${row['id']}/follow/",
                                         headers=self.getTriggerUser().getAccessAPICookies())
                jsonData = json.loads(response.text)
                now = datetime.now()
                if jsonData["result"] == "requested":
                    print(f'CSV2Following: requested {row["username"]}({row["id"]}) at {now}')
                elif jsonData["result"] == "following":
                    print(f'CSV2Following: following {row["username"]}({row["id"]}) at {now}')
                else:
                    print(f'CSV2Following: Error {row["username"]}({row["id"]}) at {now}')
                self.__line_count += 1
                time.sleep(self.__config.getConfig()["time"])
            print(f'Processed {self.__line_count} lines.')
