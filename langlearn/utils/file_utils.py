import os

from langlearn.file_handlers.csv_handler import CSVHandler
from langlearn.file_handlers.txt_handler import TXTHandler


def read_words_from_file(file_path, required_columns=1):
    """
    Read words from a file.

    Args:
        file_path (str): The path to the file.
        required_columns (int, optional): The number of required columns.

    Returns:
        list: A list of words or word pairs.
    """
    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension == '.csv':
        return CSVHandler.read_words(file_path, required_columns)
    elif file_extension == '.txt':
        return TXTHandler.read_words(file_path, required_columns)
    else:
        print(f"Unsupported file type: {file_extension}")


def write_translations_to_file(translations, output_file_path):
    """
    Write translations to a file.

    Args:
        translations (dict): A dictionary of translations.
        output_file_path (str): The path to the output file.
    """
    file_extension = os.path.splitext(output_file_path)[1].lower()
    if file_extension == '.csv':
        CSVHandler.write_words(translations, output_file_path)
    elif file_extension == '.txt':
        TXTHandler.write_words(translations, output_file_path)
    else:
        print(f"Unsupported file type: {file_extension}")


def is_file_valid(input_file_path, txt_file=False):
    """
    Checks if the specified file is valid for processing.

    Args:
        input_file_path (str): The path to the file to be checked.
        txt_file (bool, optional): bool: True if input_file_path has to be text file, False otherwise.

    Returns:
        bool: True if the file is valid (exists, has a valid extension, and is not empty), False otherwise.
    """
    if not os.path.isfile(input_file_path):
        print(f"Error: The file '{input_file_path}' does not exist.")
        return False

    base, file_extension = os.path.splitext(input_file_path)

    if not file_extension:
        print("Error: The input file must have a valid extension.")
        return False
    elif file_extension not in ['.txt', '.csv']:
        print(f"Unsupported file extension: {file_extension}")
        return False

    if txt_file:
        if not input_file_path.endswith('.txt'):
            print(f"Unsupported file extension: {file_extension}")
            return False

    if not os.path.getsize(input_file_path):
        print(f"Error: The file '{input_file_path}' is empty.")
        return False

    return True
