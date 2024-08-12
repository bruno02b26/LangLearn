import csv
import os
import random


class CSVHandler:
    """
    A utility class for handling CSV file operations.
    """

    @staticmethod
    def _is_file_empty(input_file_path):
        """
        Checks if a file is empty and prints an error message if it is.

        Args:
            input_file_path (str): The path to the file to check.

        Returns:
            bool: True if the file is not empty; otherwise, prints an error message and returns False.
        """
        if not os.path.getsize(input_file_path):
            print(f"Error: The file '{input_file_path}' is empty.")
            return
        return True

    @staticmethod
    def read_words(file_path, required_columns=1, delimiter=':'):
        """
        Reads words from a CSV file and checks for column count consistency.

        Args:
            file_path (str): The path to the CSV file.
            required_columns (int, optional): The expected number of columns in each row (default is 1).
            delimiter (str, optional): The delimiter used in the CSV file (default is ':').

        Returns: list: A list of rows, where each row is a list of values from the CSV file. If the number of columns
        in a row does not match `required_columns`, an error message is printed and the function returns None.
        """
        words = []
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=delimiter)
            for row in reader:
                if len(row) != required_columns:
                    print(f"CSV format error: Expected {required_columns} columns but found {len(row)} in "
                          f"row {row}")
                    return
                words.append(row)
        return words

    @staticmethod
    def write_words(translations, output_file_path, delimiter=':'):
        """
        Write translations to a CSV file.

        Args:
            translations (dict): A dictionary where keys are words and values are their translations.
            output_file_path (str): The path to the output CSV file.
            delimiter (str, optional): The delimiter used in the CSV file (default is ':').
        """
        with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=delimiter)
            for word, translation in translations.items():
                translation = ' ' + translation
                writer.writerow([word, translation])
                csvfile.flush()

    @staticmethod
    def swap_order_csv(input_filename, output_filename, delimiter=':'):
        """
        Swap the order of columns in a CSV file.

        Args:
            input_filename (str): The path to the input CSV file.
            output_filename (str): The path to the output CSV file.
            delimiter (str, optional): The delimiter separating the columns in the CSV file (default is ':').
        """
        if not CSVHandler._is_file_empty(input_filename):
            return

        temp_output = []

        with open(input_filename, 'r', encoding='utf-8') as infile:
            reader = csv.reader(infile, delimiter=delimiter)
            for row in reader:
                if row:
                    if len(row) == 2:
                        row[1] = row[1].strip()
                        row[0] = ' ' + row[0]
                        temp_output.append([row[1], row[0]])
                    else:
                        print(f"Error: Expected 2 columns but found {len(row)} in row: {row}")
                        return

        if temp_output:
            with open(output_filename, 'w', newline='', encoding='utf-8') as outfile:
                writer = csv.writer(outfile, delimiter=delimiter)
                writer.writerows(temp_output)
                outfile.flush()

            print(f"File '{input_filename}' has been processed and saved as '{output_filename}'")
        else:
            print(f"Error: No valid rows to write to '{output_filename}'.")

    @staticmethod
    def shuffle_file_csv(input_file_path, output_file_path):
        """
        Shuffle the rows of a CSV file and save the result to a new file.

        Args:
            input_file_path (str): The path to the input CSV file.
            output_file_path (str): The path to the output CSV file.
        """
        try:
            if not CSVHandler._is_file_empty(input_file_path):
                return

            with open(input_file_path, 'r', newline='', encoding='utf-8') as infile:
                reader = list(csv.reader(infile))

            reader = [row for row in reader if any(cell.strip() for cell in row)]

            if not reader:
                print(f"Error: No valid rows to shuffle in '{input_file_path}'.")
                return

            random.shuffle(reader)

            with open(output_file_path, 'w', newline='', encoding='utf-8') as outfile:
                writer = csv.writer(outfile)
                writer.writerows(reader)
                outfile.flush()

            print(f'File {input_file_path} has been shuffled and saved as {output_file_path}')

        except Exception as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def format_file_csv(input_file_path, output_file_path):
        """
        Format a CSV file by adding a space after each ':' and ';' in each cell.

        Args:
            input_file_path (str): The path to the input CSV file.
            output_file_path (str): The path to the output CSV file.
        """
        try:
            if not CSVHandler._is_file_empty(input_file_path):
                return

            temp_output = []
            with open(input_file_path, 'r', newline='', encoding='utf-8') as infile:
                reader = csv.reader(infile)
                for row in reader:
                    processed_row = [': '.join([cell.strip() for cell in segment.split(':')])
                                     for segment in row]
                    processed_row = ['; '.join([cell.strip() for cell in segment.split(';')])
                                     for segment in processed_row]

                    if any(cell.strip() for cell in processed_row):
                        temp_output.append(processed_row)

            CSVHandler.save_processed_csv(output_file_path, temp_output)

        except Exception as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def add_delimiter_and_space_extension_csv(input_file_path, output_file_path):
        """
        Process a CSV file to add a delimiter and space to each cell.

        Args:
            input_file_path (str): The path to the input CSV file.
            output_file_path (str): The path to the output CSV file where processed data will be saved.
        """
        try:
            if not CSVHandler._is_file_empty(input_file_path):
                return

            temp_output = []
            with open(input_file_path, 'r', newline='', encoding='utf-8') as infile:
                reader = csv.reader(infile)
                for row in reader:
                    if row:
                        processed_row = [cell.strip() + ': ' for cell in row]
                        temp_output.append(processed_row)

            CSVHandler.save_processed_csv(output_file_path, temp_output)

        except Exception as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def save_processed_csv(output_file_path, processed_data):
        """
        Save the processed data to a new CSV file.

        Args:
            output_file_path (str): The path to the output CSV file where the processed data will be saved.
            processed_data (list): A list of processed rows to be written to the output file.
        """
        try:
            if processed_data:
                with open(output_file_path, 'w', newline='', encoding='utf-8') as outfile:
                    writer = csv.writer(outfile)
                    writer.writerows(processed_data)
                    outfile.flush()

                print(f"File has been processed and saved as '{output_file_path}'")
            else:
                print(f"Error: No valid rows to write to '{output_file_path}'")
        except Exception as e:
            print(f"An error occurred during saving: {e}")

    @staticmethod
    def sort_file_csv(input_file_path, output_file_path, delimiter=':'):
        """
        Sort the rows of a CSV file by the first character of the first column in each row.

        Args:
            input_file_path (str): The path to the input CSV file.
            output_file_path (str): The path to the output CSV file.
            delimiter (str, optional): The delimiter used in the CSV file (default is ':').
        """
        try:
            if not CSVHandler._is_file_empty(input_file_path):
                return

            with open(input_file_path, 'r', newline='', encoding='utf-8') as infile:
                reader = list(csv.reader(infile, delimiter=delimiter))

            reader = [row for row in reader if any(cell.strip() for cell in row)]

            if not reader:
                print(f"Error: No valid rows to sort in '{input_file_path}'.")
                return

            reader.sort(key=lambda row: row[0].strip().lower())

            with open(output_file_path, 'w', newline='', encoding='utf-8') as outfile:
                writer = csv.writer(outfile, delimiter=delimiter)
                writer.writerows(reader)
                outfile.flush()

            print(f"File '{input_file_path}' has been sorted and saved as '{output_file_path}'")

        except Exception as e:
            print(f"An error occurred: {e}")
