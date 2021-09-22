import sys
import csv
from datetime import datetime
from CSVidenComparer import CSVidenComparer
from CSVDiffComparer import CSVDiffComparer

def main():
    len_args = len(sys.argv) - 1

    file_paths = []

    if len_args == 0:

        while True:
            print("if want to end the input filepath stage, please enter 'exit'")
            file_path = input("Please enter the csv file path: ")
            if file_path.lower() == "exit":
                break
            else:
                file_paths.append(file_path)

    else:
        for index in range(1, len_args):
            file_paths.append(sys.argv[index])

    CSVDiffComparer(file_paths).compare()
#CSVidenComparer(file_paths).compare()

if __name__ == "__main__":
    main()