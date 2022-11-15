import unittest
import pandas as pd
from csv_combiner import CsvCombiner


class Test(unittest.TestCase):

    combiner = CsvCombiner()

    def test_no_file_entered(self):
        """
        Check the output when no files are entered
        """

        with self.assertRaises(Exception) as context:
            self.combiner.get_file_paths(['./csv_combiner.py'])
        self.assertEqual(str(context.exception), "No file entered. Please run the code with a correct command line.")

    def test_empty_file(self):
        """
        Check the output when an input file is empty
        """
        with self.assertRaises(Exception) as context:
            self.combiner.validate_path('./fixtures/empty_file.csv')
        self.assertEqual(str(context.exception), "./fixtures/empty_file.csv is an empty file.")

    def test_non_existing_file(self):
        """
        Check the output when an input file doesn't exist
        """
        with self.assertRaises(Exception) as context:
            self.combiner.csv_combiner(['./fixtures/a.csv', './fixtures/clothing.csv'])
        self.assertEqual(str(context.exception), "File not found. ./fixtures/a.csv is not a valid path.")

    def test_invalid_csv_file(self):
        """
        Check the output when an input file is not a csv file
        """
        with self.assertRaises(Exception) as context:
            self.combiner.csv_combiner(['./fixtures/test.docx', './fixtures/clothing.csv'])
        self.assertEqual(str(context.exception), "CSV file not found. test.docx is not a valid filename.")

    def test_successfully_combined(self):
        """
        Check if files are successfully combined. New combined file should contain all columns of each file
        and a column named 'filename'
        """

        self.combiner.csv_combiner(['./fixtures/accessories2.csv', './fixtures/clothing.csv'])
        all_columns = []

        combined_columns = pd.read_csv('combined.csv').columns.values
        for c in pd.read_csv('./fixtures/accessories2.csv').columns.values:
            all_columns.append(c)

        for c in pd.read_csv('./fixtures/clothing.csv').columns.values:
            all_columns.append(c)

        all_columns.append('filename')

        for column in all_columns:
            self.assertIn(column, combined_columns)


    def test_length_of_combined_file(self):
        """
        Check if files are successfully combined. The sum of the number
        of rows in each file should be equal to the number of rows in the new file
        """

        args = ['./csv_combiner.py', './fixtures/accessories.csv','./fixtures/clothing.csv','./fixtures/household_cleaners.csv']
        path_lists = self.combiner.get_file_paths(args)
        self.combiner.csv_combiner(path_lists)

        df_accessories = pd.read_csv('./fixtures/accessories.csv')
        df_clothing = pd.read_csv('./fixtures/clothing.csv')
        df_household_cleaners = pd.read_csv('./fixtures/household_cleaners.csv')
        combined_df = pd.read_csv('combined.csv')
        length = len(df_accessories) + len(df_clothing) + len(df_household_cleaners)

        self.assertEqual(len(combined_df), length)
