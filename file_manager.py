import csv
from datetime import datetime

class FileManager:

    def __init__(self, file_path=None):
        if file_path is None:
            self.__file_path = input("Please enter your file path: ")
        else:
            self.__file_path = file_path

    def getFilePath(self):
        return self.__file_path

    @staticmethod
    def save_csv_file(ordered_dict_list, file_path=None):
        if ordered_dict_list is None:
            raise IndexError("Not any data need to save")
        if file_path is None:
            file_path = f"result-fitting{int(datetime.now().timestamp())}"
        save_count = 0
        with open(file_path, mode="w+", encoding='utf-8-sig') as csv_file:
            writer = csv.DictWriter(csv_file, ordered_dict_list[0].keys())
            writer.writeheader()
            for row in ordered_dict_list:
                writer.writerow(row)
                save_count += 1
            print(f"FileManager: {save_count} rows saved, {file_path}")


