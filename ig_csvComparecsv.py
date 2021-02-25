import sys
import csv
from datetime import datetime
from CSVidenComparer import CSVidenComparer

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

    CSVidenComparer(file_paths).compare()