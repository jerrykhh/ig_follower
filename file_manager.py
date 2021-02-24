class FileManager:

    def __init__(self, file_path=None):
        if file_path is None:
            self.__file_path = input("Please enter your file path: ")
        else:
            self.__file_path = file_path

    def getFilePath(self):
        return self.__file_path
