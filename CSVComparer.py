import abc
import csv
from file_manager import FileManager


class CSVComparer(metaclass=abc.ABCMeta):

    def __init__(self, file_path):
        self.__filePath = file_path

    def getFilePaths(self):
        return self.__filePath

    @abc.abstractclassmethod
    def compare(self):
        raise NotImplementedError()

    def getFilePathsLength(self):
        return len(self.__filePath)

    def save(self, output_file_path, ordered_dict_list):
        FileManager.save_csv_file(ordered_dict_list, output_file_path)

    @staticmethod
    def getOrderedDictList(file_path):
        ordered_dict_list = []
        with open(file_path, mode='r', encoding='utf-8-sig') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                ordered_dict_list.append(row)
            return ordered_dict_list
