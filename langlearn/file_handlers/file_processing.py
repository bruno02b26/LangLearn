import os

from .txt_handler import TXTHandler
from .csv_handler import CSVHandler


def check_repeated_columns(directory):
    """
    Check for repeated values in the first column of .txt files in the given directory.

    Args:
        directory (str): The directory to check for duplicates.

    Returns:
        tuple: (has_repeats, occurrences)
    """
    if not os.path.isdir(directory):
        print(f"Error: The path '{directory}' is not a directory.")
        return False, {}

    occurrences = {}
    has_repeats = False

    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith('.txt')]

    if not files:
        print("No .txt files found in the specified directory.")
        return has_repeats, occurrences

    for file in files:
        file_path = os.path.join(directory, file)

        print(f"Processing file: {file}")

        with open(file_path, 'r') as f:
            lines = f.readlines()
            for line_num, line in enumerate(lines):
                if '|' in line:
                    parts = line.strip().split('|')
                elif ':' in line:
                    parts = line.strip().split(':')
                else:
                    parts = [line.strip()]

                if len(parts) == 0 or parts[0] == '':
                    continue

                first_column = parts[0].strip()
                if first_column in occurrences:
                    occurrences[first_column].append((file, line_num + 1))
                    has_repeats = True
                else:
                    occurrences[first_column] = [(file, line_num + 1)]

    if has_repeats:
        print("Duplicates found:")
        for column, files_lines in occurrences.items():
            if len(files_lines) > 1:
                print(f"Value '{column}' appears in:")
                for file, line in files_lines:
                    print(f"  File: {file}, Line: {line}")
    else:
        print("OK - No duplicates found in the first columns.")

    return has_repeats, occurrences


def remove_duplicates(directory, occurrences):
    """
    Remove duplicates from files.

    Args:
        directory (str): The directory containing the files.
        occurrences (dict): The occurrences of duplicates.
    """
    if not occurrences:
        print("No duplicates found.")
        return

    confirm_and_update_occurrences(directory, occurrences)


def confirm_and_update_occurrences(directory, occurrences):
    """
    Prompts the user to confirm the removal of duplicate words in all files in the specified directory.

    Args:
        directory (str): The directory containing the files.
        occurrences (dict): A dictionary with words as keys and lists of file-line tuples as values.
    """
    while True:
        confirm = input(
            f"Are you sure you want to remove duplicate words in all files located in '{directory}'? "
            f"This action will keep only the first occurrence of each word in each file. "
            f"Type 'y' to proceed or 'n' to cancel: ").strip().lower()

        if confirm in ['y', 'yes']:
            update_occurrences(directory, occurrences)
            print("Operation done. Returning to menu.")
            return
        elif confirm in ['n', 'no']:
            print("Operation cancelled. Returning to menu.")
            return
        else:
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")


def update_occurrences(directory, occurrences):
    """
    Updates occurrences by keeping only the first instance of each word per file and removing duplicates.

    Args:
        directory (str): The directory containing the files.
        occurrences (dict): A dictionary with words as keys and lists of file-line tuples as values.

    Returns: dict or None: Returns an updated dictionary with occurrences if duplicates remain, or None if all
    duplicates are resolved.
    """
    updated_occurrences = {}

    for word, files in occurrences.items():
        file_line_map = {}

        for file_name, line_num in files:
            if file_name not in file_line_map:
                file_line_map[file_name] = line_num
            else:
                continue

        updated_files = []
        for file_name, line_num in file_line_map.items():
            updated_files.append((file_name, line_num))

        updated_occurrences[word] = updated_files

    line_dict = create_line_dict_from_occurrences(updated_occurrences)
    remove_unwanted_lines(directory, line_dict)
    remove_new_lines(directory, line_dict)

    has_repeats, occurrences = check_repeated_columns(directory)
    if has_repeats:
        return occurrences
    else:
        print("No duplicates found.")
        return None


def remove_unwanted_lines(directory, line_dict):
    """
    Removes lines from files specified in line_dict based on line numbers to remove duplicates.

    Args:
        directory (str): The directory containing the files.
        line_dict (dict): Dictionary with file names as keys and lists of line numbers to keep as values.
    """
    for file_name, line_nums in line_dict.items():
        file_path = os.path.join(directory, file_name)

        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                lines = file.readlines()

            updated_lines = []
            deleted_lines = []

            for i in range(1, len(lines) + 1):
                if i in line_nums:
                    updated_lines.append(lines[i - 1])
                else:
                    if lines[i - 1].strip():
                        deleted_lines.append(lines[i - 1].strip())
                    updated_lines.append('\n')

            with open(file_path, 'w') as file:
                file.writelines(updated_lines)

            if deleted_lines:
                print(f"Deleted duplicates from {file_name}: {', '.join(deleted_lines)}")
        else:
            print(f"File {file_name} doesn't exist in {directory} directory.")


def create_line_dict_from_occurrences(occurrences):
    """
    Creates a dictionary mapping file names to lists of unique line numbers from occurrences.

    Args:
        occurrences (dict): Dictionary with words as keys and lists of file-line tuples as values.

    Returns:
        dict: A dictionary with file names as keys and sorted lists of line numbers as values.
    """
    line_dict = {}

    for word, files in occurrences.items():
        for file_name, line_num in files:
            if file_name not in line_dict:
                line_dict[file_name] = []
            if line_num not in line_dict[file_name]:
                line_dict[file_name].append(line_num)

    for file_name in line_dict:
        line_dict[file_name].sort()

    return line_dict


def remove_new_lines(directory, line_dict):
    """
    Removes new lines from files specified in line_dict, ensuring lines to keep are preserved.

    Args:
        directory (str): The directory containing the files.
        line_dict (dict): Dictionary with file names as keys and lists of line numbers to keep as values.
    """
    for file_name, line_nums in line_dict.items():
        file_path = os.path.join(directory, file_name)

        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                lines = file.readlines()

            updated_lines = []
            for i in range(1, len(lines) + 1):
                if i in line_nums:
                    updated_lines.append(lines[i - 1])
                else:
                    updated_lines.append('\n')

            if len(updated_lines) > 0 and updated_lines[-1] == '\n':
                updated_lines = [line for line in updated_lines if line != '\n'] + ['\n']
            else:
                updated_lines = [line for line in updated_lines if line != '\n']

            with open(file_path, 'w') as file:
                file.writelines(updated_lines)

        else:
            print(f"File {file_name} doesn't exist in {directory} directory.")


def process_file_extension(input_file_path, output_file_path, operation):
    """
    Process a file based on its extension and the specified operation.

    Args:
        input_file_path (str): The path to the input file.
        output_file_path (str): The path to the output file.
        operation (str): The operation to perform ('swap_order', 'shuffle', 'format', 'add_delimiter', 'sort').
    """
    file_extension = os.path.splitext(input_file_path)[1].lower()

    handlers = {
        '.txt': {
            'swap_order': TXTHandler.swap_order_txt,
            'shuffle': TXTHandler.shuffle_file_txt,
            'format': TXTHandler.format_file_txt,
            'add_delimiter': TXTHandler.add_delimiter_and_space_extension_txt,
            'sort': TXTHandler.sort_file_txt
        },
        '.csv': {
            'swap_order': CSVHandler.swap_order_csv,
            'shuffle': CSVHandler.shuffle_file_csv,
            'format': CSVHandler.format_file_csv,
            'add_delimiter': CSVHandler.add_delimiter_and_space_extension_csv,
            'sort': CSVHandler.sort_file_csv
        }
    }

    if file_extension in handlers and operation in handlers[file_extension]:
        handlers[file_extension][operation](input_file_path, output_file_path)
    else:
        print("Unsupported file type or operation. Only '.txt' and '.csv' files with valid operations are supported.")


def swap_order_extension(input_file_path, output_file_path):
    """Swap the order of columns in a file based on its extension."""
    process_file_extension(input_file_path, output_file_path, 'swap_order')


def shuffle_file_extension(input_file_path, output_file_path):
    """Shuffle the contents of a file based on its extension."""
    process_file_extension(input_file_path, output_file_path, 'shuffle')


def format_file_extension(input_file_path, output_file_path):
    """Format a file based on its extension by adding ':' and space."""
    process_file_extension(input_file_path, output_file_path, 'format')


def add_delimiter_and_space_extension(input_file_path, output_file_path):
    """Add delimiter and space to a file based on its extension."""
    process_file_extension(input_file_path, output_file_path, 'add_delimiter')


def sort_file_extension(input_file_path, output_file_path):
    """Sort a file based on its first column."""
    process_file_extension(input_file_path, output_file_path, 'sort')
