import csv
from CSVComparer import CSVComparer
from datetime import datetime


class CSVidenComparer(CSVComparer):

    def __init__(self, file_paths):
        super().__init__(file_paths)

    def compare(self):
        if self.getFilePathsLength() < 2:
            raise ValueError("Only file paths > 1 can compare")

        output_file_path = f"result-{int(datetime.now().timestamp())}.csv"

        for index in range(1, len(self.getFilePaths())):
            if index == 1:
                pre_file_path = self.getFilePaths()[index - 1]
            else:
                pre_file_path = output_file_path

            post_file_path = self.getFilePaths()[index]
            duplicate_orderddict_list = self.compareCSV(pre_file_path, post_file_path)

            print(f"CSVIdenComparer: {len(duplicate_orderddict_list)} duplicate rows found")
            if len(duplicate_orderddict_list) < 1:
                print('some file not find a identical row')
                return

            self.save(output_file_path, duplicate_orderddict_list)

    @staticmethod
    def compareCSV(pre_csv_file_path, post_csv_file_path):
        duplicate_orderddict = []
        with open(pre_csv_file_path, mode='r', encoding='utf-8-sig') as pre_csv_file:
            with open(post_csv_file_path, mode='r', encoding='utf-8-sig') as post_csv_file:
                pre_csv_reader = csv.DictReader(pre_csv_file)
                post_csv_reader = csv.DictReader(post_csv_file)

                for pre_csv_row in pre_csv_reader:
                    post_csv_file.seek(0)

                    for post_csv_row in post_csv_reader:
                        if pre_csv_row['id'] == post_csv_row['id']:
                            duplicate_orderddict.append(pre_csv_row)
                            break
        return duplicate_orderddict

    @staticmethod
    def compareOrderedList(pre_ordered_list, post_ordered_list):
        result = [];
        for ordered_dict in post_ordered_list:
            if ordered_dict in pre_ordered_list:
                result.append(ordered_dict)
        return result;
