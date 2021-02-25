import abc
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
