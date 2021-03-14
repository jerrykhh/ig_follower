from CSVComparer import CSVComparer
from CSVidenComparer import CSVidenComparer
from datetime import datetime
from file_manager import FileManager


class CSVDiffComparer(CSVComparer):

    def __init__(self, file_paths):
        super().__init__(file_paths)

    def compare(self):
        if self.getFilePathsLength() < 2:
            raise ValueError("Only file paths > 1 can compare")

        output_path = f"diff-{int(datetime.now().timestamp())}.csv"

        ident_ordered_dict_list = CSVidenComparer.compareCSV(self.getFilePaths()[0], self.getFilePaths()[1])
        orderd_dicts = self.getOrderedDictList(self.getFilePaths()[0]) + self.getOrderedDictList(self.getFilePaths()[1])
        print(f"Total rows: {len(orderd_dicts)}")
        for ident_row in ident_ordered_dict_list:
            orderd_dicts.remove(ident_row)
        print(f"Remove {len(ident_ordered_dict_list)} rows")

        for index in range(2, len(self.getFilePaths())):
            ident_ordered_dict_list = CSVidenComparer.compareOrderedList(orderd_dicts, self.getOrderedDictList(
                self.getFilePaths()[index]))
            orderd_dicts += self.getOrderedDictList(self.getFilePaths()[index]);

            print(f'{self.getFilePaths()[index]}, total rows: {len(orderd_dicts)}')
            for ident_row in ident_ordered_dict_list:
                orderd_dicts.remove(ident_row)
            print(f'Remove {len(ident_ordered_dict_list)} rows')

        FileManager.save_csv_file(orderd_dicts, output_path)
