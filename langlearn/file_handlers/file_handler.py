import os

from langlearn.file_handlers.file_processing import (
    remove_duplicates,
    check_repeated_columns,
    swap_order_extension,
    shuffle_file_extension,
    format_file_extension,
    add_delimiter_and_space_extension,
    sort_file_extension
)


class FileHandler:
    """
    A utility class for handling file operations and delegating to specific handlers.
    """

    @staticmethod
    def check_and_report_duplicates(directory=None, remove=False):
        """
        Checks for duplicate words in files within a specified directory and optionally removes them.

        Args:
            directory (str, optional): The directory path to check for duplicates. If None, uses a default directory.
            remove (bool, optional): Whether to remove duplicates. Defaults to False, only reports duplicates if False.
        """
        directory = directory or FileHandler._get_directory()

        if not os.path.exists(directory):
            print(f"Error: The directory '{directory}' does not exist.")
            return

        has_repeats, occurrences = check_repeated_columns(directory)

        if has_repeats:
            if remove:
                print("Removing duplicates...")
                remove_duplicates(directory, occurrences)

    @staticmethod
    def shuffle_file(input_file_path=None):
        """
        Shuffle the lines of a file and save to a new file with a suffix.

        Args:
            input_file_path (str, optional): The path to the input file. If not provided, prompts the user.
        """
        FileHandler._process_file(input_file_path, 'shuffled', shuffle_file_extension)

    @staticmethod
    def swap_order(input_file_path=None):
        """
        Swap the order of columns in the file.

        Args:
            input_file_path (str, optional): The path to the input file. If not provided, prompts the user.
        """
        FileHandler._process_file(input_file_path, 'reversed', swap_order_extension)

    @staticmethod
    def format_file(input_file_path=None):
        """
        Format the file by adding a space after each colon and each semicolon.

        Args:
            input_file_path (str, optional): The path to the input file. If not provided, prompts the user.
        """
        FileHandler._process_file(input_file_path, 'formatted', format_file_extension)

    @staticmethod
    def add_delimiter_and_space(input_file_path=None):
        """
        Adds a delimiter ':' followed by a space to each line of the file.

        Args:
            input_file_path (str, optional): The path to the input file. If not provided, prompts the user.
        """
        FileHandler._process_file(input_file_path, 'with_delimiter', add_delimiter_and_space_extension)

    @staticmethod
    def sort_file(input_file_path=None):
        """
        Sort the lines of a file by the first character of each line.

        Args:
            input_file_path (str, optional): The path to the input file. If not provided, prompts the user.
        """
        FileHandler._process_file(input_file_path, 'sorted', sort_file_extension)

    @staticmethod
    def _process_file(input_file_path, suffix, process_function):
        """
        Process a file using a given processing function.

        Args:
            input_file_path (str): The path to the input file.
            suffix (str): The suffix to add to the output file.
            process_function (callable): The function to process the file.
        """
        if not input_file_path:
            input_file_path = input("Enter the file path: ").strip()

        if not os.path.isfile(input_file_path):
            print(f"Error: The file '{input_file_path}' does not exist.")
            return

        output_file_path = FileHandler.get_output_file_path(input_file_path, suffix)

        if output_file_path is None:
            print("Error generating output file path.")
            return

        process_function(input_file_path, output_file_path)

    @staticmethod
    def _get_directory():
        """
        Prompt the user for a directory path and return it.

        Returns:
            str: The directory path entered by the user.
        """
        return input("Enter the directory path: ").strip()

    @staticmethod
    def get_output_file_path(input_file_path, suffix):
        """
        Get the output file path based on the input file path and a suffix string to be added before the file extension.

        Args:
            input_file_path (str): The path to the input file.
            suffix (str): The suffix to be added to the file name.

        Returns:
            str: The path to the output file.
        """
        base, file_extension = os.path.splitext(input_file_path)

        if not file_extension:
            print("Error: The input file must have a valid extension.")
            return None
        elif file_extension not in ['.txt', '.csv']:
            print(f"Unsupported file extension: {file_extension}")
            return None

        return f"{base}_{suffix}{file_extension}"
