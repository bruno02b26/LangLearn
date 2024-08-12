import os
import random

from termcolor import colored

from langlearn.utils.file_utils import read_words_from_file, write_translations_to_file, is_file_valid


class LearningMode:
    """
    The LearningMode class handles the learning mode of the translation application,
    where users can learn translations from a given file.
    """

    @staticmethod
    def run(input_file_path):
        """
        Runs the learning mode, checking if the input file exists and contains words.

        Args:
            input_file_path (str): The path to the input file containing word pairs.
        """

        if not is_file_valid(input_file_path):
            return

        LearningMode.learn_words(input_file_path)

    @staticmethod
    def learn_words(input_file_path):
        """
        Facilitates the learning process, prompting the user to translate words.

        Args:
            input_file_path (str): The path to the input file containing word pairs.
        """
        known_words = set()
        no_know_words = 0
        last_word_pair = None
        words = LearningMode.read_words(input_file_path)
        if not words:
            return
        no_all_words = len(words)

        while True:
            if not words:
                words = LearningMode.read_words(input_file_path)
                if not words:
                    return

            if no_all_words == no_know_words:
                if not LearningMode.reload_words():
                    break
                else:
                    words = LearningMode.read_words(input_file_path)
                    if not words:
                        print('There are no words left.')
                        return
                known_words.clear()
                no_all_words = len(words)
                no_know_words = 0
                last_word_pair = None
                continue

            word_pair = LearningMode.select_word_pair(words, known_words, last_word_pair)
            last_word_pair = word_pair

            if LearningMode.handle_translation(word_pair, known_words, input_file_path):
                no_know_words += 1

    @staticmethod
    def read_words(input_file_path):
        """
        Reads word pairs from the input file and trims spaces around the words.

        Args:
            input_file_path (str): The path to the input file.

        Returns:
            list: A list of word pairs.
        """
        try:
            words = read_words_from_file(input_file_path, 2)
            if not words:
                return
            return [[w.strip() for w in pair] for pair in words]
        except Exception as e:
            print(f"Error reading file: {e}")
            return []

    @staticmethod
    def reload_words():
        """
        Prompts the user to reload words from the file and continue learning.

        Returns:
            bool: True if the user chooses to reload the words, False otherwise.
        """
        print("All words have been translated correctly.")
        response = input(
            "Would you like to reload the words from the file and continue? (y/Y for yes): ").strip().lower()
        if response == 'y':
            return True
        return False

    @staticmethod
    def select_word_pair(words, known_words, last_word_pair):
        """
        Selects a word pair from the list of words that hasn't been learned yet.

        Args:
            words (list): The list of word pairs.
            known_words (set): The set of known word pairs.
            last_word_pair (list): The last word pair that was presented.

        Returns:
            list: The selected word pair.
        """
        remaining_words = [tuple(word_pair) for word_pair in words if tuple(word_pair) not in known_words]

        if len(remaining_words) == 1:
            return remaining_words[0]

        word_pair = random.choice(words)
        while tuple(word_pair) in known_words or word_pair == last_word_pair:
            word_pair = random.choice(words)
        return word_pair

    @staticmethod
    def handle_translation(word_pair, known_words, input_file_path):
        """
        Handles the translation process, checking if the user's translation is correct.

        Args:
            word_pair (list): The word pair to be translated.
            known_words (set): The set of known word pairs.
            input_file_path (str): The path to the input file containing word pairs.

        Returns:
            bool: True if the translation is correct, False otherwise.
        """
        original_word, correct_translations = word_pair[0], word_pair[1].split(';')
        correct_translations = [t.strip() for t in correct_translations]

        user_translation = input(f"Translate '{original_word}': ").strip().lower()
        os.system('color')

        if user_translation in correct_translations:
            print(colored("Correct!", 'green'))
            additional_translations = [t for t in correct_translations if t != user_translation]
            if additional_translations:
                print(f"Other correct translations: {', '.join(additional_translations)}")
            if LearningMode.prompt_remove_word(word_pair, input_file_path):
                print(f"'{original_word}' removed from file.")
            known_words.add(tuple(word_pair))
            return True
        else:
            print(f"{colored('Incorrect.', 'red')} Correct translations: {', '.join(correct_translations)}")
            return False

    @staticmethod
    def prompt_remove_word(word_pair, input_file_path):
        """
        Prompts the user to remove a word pair from the file if it has been correctly translated.

        Args:
            word_pair (list): The word pair to be removed.
            input_file_path (str): The path to the input file containing word pairs.

        Returns:
            bool: True if the word pair is removed, False otherwise.
        """
        response = input("Remove this word from the file? (y/Y for yes): ").strip().lower()
        if response == 'y':
            try:
                file_words = LearningMode.read_words(input_file_path)
                if not file_words:
                    return
                file_words = [[w.strip() for w in pair] for pair in file_words]
                word_pair_list = [w.strip() for w in word_pair]
                if word_pair_list in file_words:
                    file_words.remove(word_pair_list)
                    write_translations_to_file(dict(file_words), input_file_path)
                    return True
                else:
                    print(f"Word pair '{word_pair}' not found in file.")
            except Exception as e:
                print(f"Error writing to file: {e}")
        return False
