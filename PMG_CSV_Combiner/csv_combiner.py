import os
import sys
import pandas as pd


class CsvCombiner:

    @staticmethod
    def get_file_paths(args):
        """
        This function returns a list of file paths. If the input parameter is an empty list,
        then raise an exception.
        """
        if len(args) <= 1:
            raise Exception("No file entered. Please run the code with a correct command line.")
        return args[1:]

    @staticmethod
    def get_file_name(file_path):
        """
        This function returns a file name.
        """
        return os.path.basename(file_path)

    def validate_path(self, file_path):
        """
        This function checks if a file exists and if it's a valid csv file.
        """

        if not os.path.exists(file_path):
            raise Exception(f"File not found. {file_path} is not a valid path.")
        if os.stat(file_path).st_size == 0:
            raise Exception(f"{file_path} is an empty file.")

        filename = self.get_file_name(file_path)
        if not filename.endswith(".csv"):
            raise Exception(f"CSV file not found. {filename} is not a valid filename.")

        return True

    def csv_combiner(self, path_lists):
        """
        This function combines all the csv files.
        """
        for path in path_lists:
            if not self.validate_path(path):
                return

        chunk_list = []
        for file in path_lists:
            read_chunk = pd.read_csv(file, encoding='utf-8', chunksize=1000000)
            for chunk in read_chunk:
                file_name = self.get_file_name(file)
                chunk['filename'] = file_name
                chunk_list.append(chunk)

        df_base = pd.concat(chunk_list, axis=0)
        combined_file_path = 'combined.csv'
        df_base.to_csv(combined_file_path, index=False)


def main():
    combiner = CsvCombiner()
    path_lists = combiner.get_file_paths(sys.argv)
    combiner.csv_combiner(path_lists)

if __name__ == '__main__':
    main()


