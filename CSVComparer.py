import abc
import csv

class CSVComparer(metaclass=abc.ABCMeta):

    def __init__(self, file_path):
        self.__filePath = file_path

    def getFilePaths(self):
        return self.__filePath

    @abc.abstractclassmethod
    def compare(self):
        raise NotImplementedError()

    def save(self, output_file_path, ordered_dict_list):
        with open(output_file_path, mode="w+", encoding='utf-8-sig') as csv_file:
            print(ordered_dict_list[0].keys())
            writer = csv.DictWriter(csv_file, ordered_dict_list[0].keys())
            writer.writeheader()
            for row in ordered_dict_list:
                writer.writerow(row)


