import sys
from file_manager import FileManager
from CSV2Following import CSV2Following

def main():
    len_args = len(sys.argv) - 1

    if len_args == 0:
        file = FileManager()
    elif len_args == 1:
        file = FileManager(sys.argv[1])
    else:
        print("Command Arguments incorrect: python ig_cs2followingfitting.py [CSV filePath]")

    CSV2Following.fitting(file.getFilePath())


if __name__ == "__main__":
    main()