# -*- coding: utf-8 -*-


class FilteredWordStar(object):

    def __init__(self):
        self._words = None

    """
    read filtered words from file
    @param word_file: the file that contains filtered words
    """
    def read_words_from_file(self, word_file="filtered_words.txt"):
        with open(word_file, "r") as f:
            self._words = [line.strip() for line in f]

    def filter_word(self, text=""):
        if self._words is None:
            self.read_words_from_file()

        filter_words = [word for word in self._words if word in text]
        for word in filter_words:
            stars = "*" * len(word.decode("utf-8"))
            text = text.replace(word, stars)

        return text


if __name__ == "__main__":
    inputs = str(raw_input("Please enter something here!"))
    filter_word_star = FilteredWordStar()
    print filter_word_star.filter_word(inputs)
