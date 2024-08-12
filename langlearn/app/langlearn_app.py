import sys

from langlearn.file_handlers.file_handler import FileHandler
from langlearn.modes.interactive_mode import InteractiveMode
from langlearn.modes.learning_mode import LearningMode


class LanglearnApp:
    """
    The LanglearnApp class serves as the main application for language translation tasks.
    """

    def run(self):
        """
        Runs the application based on the command-line arguments provided.
        """

        print("Welcome to LangLearn!")
        argument_count = len(sys.argv)

        if argument_count == 1:
            self.handle_no_args()
        elif argument_count == 2:
            self.handle_two_args(sys.argv[1])
        elif argument_count == 3:
            self.handle_three_args(sys.argv[1], sys.argv[2])
        else:
            self.print_usage_error()

    def handle_no_args(self):
        """
        Handles command-line arguments when no arguments are provided.
        Provides an interactive menu for the user to select an option.
        """
        menu_options = {
            '1': self.handle_check_duplicates,
            '2': self.handle_remove_duplicates,
            '3': self.handle_learning_mode,
            '4': self.handle_interactive_mode,
            '5': self.handle_shuffle_file,
            '6': self.handle_reverse_file,
            '7': self.handle_format_file,
            '8': self.handle_add_separator,
            '9': self.handle_sort_file,
            '0': self.handle_exit
        }

        while True:
            print("\nPlease select an option:")
            for key, value in menu_options.items():
                print(f"  {key}. {value.__doc__}")

            choice = input("Enter your choice (0-9): ").strip()
            action = menu_options.get(choice)
            if action:
                action()
            else:
                print("Invalid choice. Please enter a number between 0 and 8.")

    @staticmethod
    def handle_two_args(flag):
        """
        Handles command-line arguments when two arguments are provided.

        Args:
            flag (str): The command-line flag indicating the operation to be performed.
        """
        if flag == '-c':
            directory = '.'
            FileHandler.check_and_report_duplicates(directory)
        elif flag == '-d':
            directory = '.'
            FileHandler.check_and_report_duplicates(directory, True)
        else:
            LanglearnApp.handle_flag_with_error(flag)

    @staticmethod
    def handle_three_args(flag, path):
        """
        Handles command-line arguments when three arguments are provided.

        Args:
            flag (str): The command-line flag indicating the operation to be performed.
            path (str): The path to the file or directory for the operation.
        """
        handlers = {
            '-c': lambda: FileHandler.check_and_report_duplicates(path),
            '-d': lambda: FileHandler.check_and_report_duplicates(path, True),
            '-l': lambda: LearningMode().run(path),
            '-i': lambda: InteractiveMode().run(path),
            '-sh': lambda: FileHandler.shuffle_file(path),
            '-r': lambda: FileHandler.swap_order(path),
            '-f': lambda: FileHandler.format_file(path),
            '-as': lambda: FileHandler.add_delimiter_and_space(path),
            '-so': lambda: FileHandler.sort_file(path)
        }

        handler = handlers.get(flag)
        if handler:
            try:
                handler()
            except Exception as e:
                print(f"An error occurred: {e}")
                sys.exit(1)
        else:
            LanglearnApp.print_usage_error()

    @staticmethod
    def handle_check_duplicates():
        """Check for duplicates in a directory"""
        FileHandler.check_and_report_duplicates()

    @staticmethod
    def handle_remove_duplicates():
        """Remove duplicates in a directory"""
        FileHandler.check_and_report_duplicates(remove=True)

    @staticmethod
    def handle_learning_mode():
        """Run learning mode"""
        input_file_path = input("Enter the file path for learning mode: ").strip()
        LearningMode().run(input_file_path)

    @staticmethod
    def handle_interactive_mode():
        """Run interactive mode"""
        input_file_path = input("Enter the file path for interactive mode: ").strip()
        InteractiveMode().run(input_file_path)

    @staticmethod
    def handle_shuffle_file():
        """Shuffle file"""
        FileHandler.shuffle_file()

    @staticmethod
    def handle_reverse_file():
        """Reverse file"""
        FileHandler.swap_order()

    @staticmethod
    def handle_format_file():
        """Format file"""
        FileHandler.format_file()

    @staticmethod
    def handle_add_separator():
        """Add separator to file"""
        FileHandler.add_delimiter_and_space()

    @staticmethod
    def handle_sort_file():
        """Sort file"""
        FileHandler.sort_file()

    @staticmethod
    def handle_exit():
        """Exit the program"""
        print("Exiting the program.")
        sys.exit(0)

    @staticmethod
    def handle_flag_with_error(flag):
        """
        Handles error messages for flags that require a file path.

        Args:
            flag (str): The command-line flag indicating the operation to be performed.
        """
        error_messages = {
            '-l': "learning mode.",
            '-i': "interactive mode.",
            '-sh': "shuffling.",
            '-r': "reversing.",
            '-f': "formatting.",
            '-as': "adding separator.",
            '-so': "sorting."
        }

        error_str = "You must provide a file path for "

        if flag in error_messages:
            full_error_message = error_str + error_messages[flag]
            print(f"Error: {full_error_message}")
        else:
            print(f"Error: Unknown flag '{flag}'")

        LanglearnApp.print_usage_error()

    @staticmethod
    def print_usage_error():
        """
        Prints a usage error message when the provided command-line arguments are incorrect.
        """
        print("Incorrect arguments.\nUsage: python main.py\n"
              "or python main.py -l <path_to_input_file>\n"
              "or python main.py -i <path_to_input_file>\n"
              "or python main.py -sh <path_to_input_file>\n"
              "or python main.py -r <path_to_input_file>\n"
              "or python main.py -f <path_to_input_file>\n"
              "or python main.py -as <path_to_input_file>\n"
              "or python main.py -so <path_to_input_file>\n"
              "or python main.py -d [<directory_path>]\n")
