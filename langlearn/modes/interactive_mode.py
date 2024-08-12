import os
import csv

from termcolor import colored

from langlearn.utils.file_utils import is_file_valid


class InteractiveMode:
    """
    Handles the interactive mode for the translation application.
    """

    def run(self, input_filename):
        """
        Runs the interactive mode, where the user can input words to search in the specified file.

        Args:
            input_filename (str): The path to the file to search in.
        """
        if not is_file_valid(input_filename, True):
            return

        print(f"Interactive mode: Searching in file '{input_filename}'")

        while True:
            word = input("Enter word to search (or press Enter to exit): ").strip()
            if not word:
                print("Exited.")
                break

            self.search_in_file(input_filename, word)

    @staticmethod
    def search_in_file(input_filename, word):
        """
        Searches for the given word in the specified file.

        Args:
            input_filename (str): The path to the file to search in.
            word (str): The word to search for.
        """
        found = False
        file_extension = os.path.splitext(input_filename)[1].lower()
        os.system('color')

        with open(input_filename, 'r', encoding='utf-8') as infile:
            if file_extension == '.csv':
                reader = csv.reader(infile)
                for row in reader:
                    if row:
                        first_column_words = [w.strip() for w in row[0].split(';')]
                        if word in first_column_words:
                            formatted_row = ', '.join(row)
                            print(colored(formatted_row, 'blue'))
                            found = True
            else:
                for line in infile:
                    line = line.strip()
                    if line:
                        if ':' in line:
                            parts = line.split(':', 1)
                            line = f"{parts[0]}:{colored(parts[1], 'blue')}"
                        else:
                            parts = [line]

                        first_column_words = [w.strip() for w in parts[0].split(';')] if len(parts) > 0 else []
                        if word in first_column_words:
                            print(line)
                            found = True

        if not found:
            print(f"No occurrences of '{word}' found.")
