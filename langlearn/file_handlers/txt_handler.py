import os
import random


class TXTHandler:
    """
    A utility class for handling TXT file operations.
    """

    @staticmethod
    def _is_valid_word(word):
        """
        Check if the word contains only valid characters.

        Args:
            word (str): The word to validate.

        Returns:
            bool: True if the word is valid, False otherwise.
        """
        return all(w.isalpha() or w in ";./'|-" or w.isspace() for w in word)

    @staticmethod
    def read_words(file_path, required_columns=1):
        """
        Read words from a TXT file.

        Args:
            file_path (str): The path to the TXT file.
            required_columns (int, optional): The number of required columns.

        Returns:
            list: A list of word pairs or words.
        """
        words = []
        with open(file_path, 'r', encoding='utf-8') as txtfile:
            for line in txtfile:
                if not line.strip():
                    continue

                parts = line.strip().split(':')
                if len(parts) != required_columns:
                    print(f"TXT format error: Expected {required_columns} elements but found {len(parts)} "
                          f"in line {line.strip()}")
                    return

                word = parts[0]
                translations = parts[1] if required_columns == 2 else ''

                if not TXTHandler._is_valid_word(word) or (required_columns == 2 and
                                                           not TXTHandler._is_valid_word(
                                                               translations.replace(';', ''))):
                    print(f"TXT format error: Invalid characters in line {line.strip()}")
                    return

                words.append((word, translations) if required_columns == 2 else word)

        return words

    @staticmethod
    def write_words(translations, output_file_path):
        """
        Write translations to a TXT file.

        Args:
            translations (dict): A dictionary of translations.
            output_file_path (str): The path to the output TXT file.
        """
        with open(output_file_path, 'w', encoding='utf-8') as txtfile:
            for word, translation in translations.items():
                txtfile.write(f"{word}: {translation}\n")
                txtfile.flush()

    @staticmethod
    def swap_order_txt(input_filename, output_filename, delimiter=':'):
        """
        Swap the order of columns in a TXT file.

        Args:
            input_filename (str): The path to the input TXT file.
            output_filename (str): The path to the output TXT file.
            delimiter (str, optional): The delimiter separating the columns in the TXT file.
        """
        if not os.path.exists(input_filename):
            print(f"Error: Input file '{input_filename}' does not exist.")
            return

        if os.path.getsize(input_filename) == 0:
            print(f"Error: The file '{input_filename}' is empty.")
            return

        all_rows_valid = True
        temp_output = []

        try:
            with open(input_filename, 'r', encoding='utf-8') as infile:
                for line in infile:
                    line = line.strip()
                    if line:
                        parts = line.split(delimiter)
                        if len(parts) == 2:
                            temp_output.append(f'{parts[1].strip()}: {parts[0].strip()}')
                        else:
                            print(f"Error: Expected 2 columns but found {len(parts)} in line: {line}")
                            return

            if all_rows_valid:
                with open(output_filename, 'w', encoding='utf-8') as outfile:
                    for line in temp_output:
                        outfile.write(line + '\n')
                        outfile.flush()

            print(f"File '{input_filename}' has been reversed and saved as '{output_filename}'")

        except Exception as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def shuffle_file_txt(input_file_path, output_file_path):
        """
        Shuffle the lines of a TXT file and save the result to a new file.

        Args:
            input_file_path (str): The path to the input TXT file.
            output_file_path (str): The path to the output TXT file.
        """
        try:
            with open(input_file_path, 'r', encoding='utf-8') as infile:
                lines = infile.readlines()

            if not lines:
                print(f"Error: The file '{input_file_path}' is empty.")
                return

            if not lines[-1].endswith('\n'):
                lines[-1] += '\n'

            random.shuffle(lines)

            with open(output_file_path, 'w', encoding='utf-8') as outfile:
                outfile.writelines(lines)
                outfile.flush()

            print(f'File {input_file_path} has been shuffled and saved as {output_file_path}')

        except Exception as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def format_file_txt(input_file_path, output_file_path):
        """
        Format a TXT file by adding a space after each ':' and ';' in each line,
        and remove duplicate lines after formatting.

        Args:
            input_file_path (str): The path to the input TXT file.
            output_file_path (str): The path to the output TXT file.
        """
        try:
            with open(input_file_path, 'r', encoding='utf-8') as infile:
                lines = infile.readlines()
                if not lines:
                    print(f"Error: The file '{input_file_path}' is empty.")
                    return

            formatted_lines = set()

            for line in lines:
                formatted_line = ': '.join([segment.strip() for segment in line.split(':')])
                formatted_line = '; '.join([segment.strip() for segment in formatted_line.split(';')])

                if formatted_line.strip():
                    formatted_lines.add(formatted_line)

            with open(output_file_path, 'w', encoding='utf-8') as outfile:
                for formatted_line in formatted_lines:
                    outfile.write(formatted_line + '\n')
                    outfile.flush()

            print(f"File '{input_file_path}' has been formatted and saved as '{output_file_path}'")

        except Exception as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def add_delimiter_and_space_extension_txt(input_file_path, output_file_path):
        """
        Format a TXT file by adding a ':' at the end of each line.

        Args:
            input_file_path (str): The path to the input TXT file.
            output_file_path (str): The path to the output TXT file.
        """
        try:
            with open(input_file_path, 'r', encoding='utf-8') as infile:
                lines = infile.readlines()
                if not lines:
                    print(f"Error: The file '{input_file_path}' is empty.")
                    return

            with open(output_file_path, 'w', encoding='utf-8') as outfile:
                for line in lines:
                    trimmed_line = line.strip()
                    if trimmed_line:
                        new_line = f"{trimmed_line}: \n"
                        outfile.write(new_line)
                        outfile.flush()

            print(f"File '{input_file_path}' has been processed and saved as '{output_file_path}'")

        except Exception as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def sort_file_txt(input_file_path, output_file_path):
        """
        Sort the lines of a TXT file by the first character of each line.

        Args:
            input_file_path (str): The path to the input TXT file.
            output_file_path (str): The path to the output TXT file.
        """
        try:
            with open(input_file_path, 'r', encoding='utf-8') as infile:
                lines = infile.readlines()

            lines = [line.strip() for line in lines if line.strip()]

            if not lines:
                print(f"Error: The file '{input_file_path}' is empty.")
                return

            lines.sort(key=lambda line: line.strip().lower())

            with open(output_file_path, 'w', encoding='utf-8') as outfile:
                for line in lines:
                    outfile.write(line + '\n')
                    outfile.flush()

            print(f"File '{input_file_path}' has been sorted and saved as '{output_file_path}'")

        except Exception as e:
            print(f"An error occurred: {e}")
