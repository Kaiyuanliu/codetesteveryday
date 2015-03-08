# -*- coding: utf-8 -*-

ALLOWED_RESPONSE = "Human Rights"
BLOCKED_RESPONSE = "Freedom"

class FilteredWord(object):

    def __init__(self):
        self._words = None

    """
    read filtered words from file
    @param word_file: the file that contains filtered words
    """
    def read_words_from_file(self, word_file="filtered_words.txt"):
        with open(word_file, "r") as f:
            self._words = [line.strip() for line in f]

    """
    To check if one word is a filtered word
    @param word: the word that needs to be checked
    @return ALLOWED_RESPONSE if the word is not in filtered words list, otherwise return BLOCKED_RESPONSE
    """
    def filter_word(self, word=""):
        if self._words is None:
            self.read_words_from_file()

        if word in self._words:
            return BLOCKED_RESPONSE
        else:
            return ALLOWED_RESPONSE


if __name__ == "__main__":
    inputs = str(raw_input("Please enter something here!"))
    filtered_word = FilteredWord()
    filtered_word.read_words_from_file()
    print filtered_word.filter_word(inputs)