import csv
from CSVComparer import CSVComparer
from datetime import datetime

class CSVidenComparer(CSVComparer):

    def __init__(self, file_paths):
        super().__init__(file_paths)

    def compare(self):
        if len(self.getFilePaths()) < 2:
            raise ValueError("Only file paths > 1 can compare")

        output_file_path = f"result-{int(datetime.now().timestamp())}.csv"

        for index in range(1, len(self.getFilePaths())):
            if index == 1:
                pre_file_path = self.getFilePaths()[index - 1]
            else:
                pre_file_path = output_file_path

            post_file_path = self.getFilePaths()[index]
            duplicate_orderddict = []
            with open(pre_file_path, mode='r', encoding='utf-8-sig') as pre_csv_file:
                with open(post_file_path, mode='r', encoding='utf-8-sig') as post_csv_file:

                    pre_csv_reader = csv.DictReader(pre_csv_file)
                    post_csv_reader = csv.DictReader(post_csv_file)

                    # skip header
                    next(pre_csv_reader)

                    for pre_csv_row in pre_csv_reader:
                        post_csv_file.seek(0)
                        next(post_csv_reader)

                        for post_csv_row in post_csv_reader:
                            if pre_csv_row['id'] == post_csv_row['id']:
                                duplicate_orderddict.append(pre_csv_row)
                                break

            self.save(output_file_path, duplicate_orderddict)







