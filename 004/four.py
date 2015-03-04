# -*- coding: utf-8 -*-

"""
任一个英文的纯文本文件，统计其中的单词出现的个数。
calculate word occurrence from any file
"""
import string
from collections import Counter, defaultdict, OrderedDict
from operator import itemgetter

class CheckWord(object):

    """
    initialize parameters
    @param _long_test: text read from file
    @param _word_list: contains all the word after removing punctuation and digits
    @param _exclude: contains punctuation and digits
    """
    def __init__(self):
        self._long_test = ""
        self._word_list = []
        self._exclude = string.punctuation + string.digits

    """
    read text from external file
    @param org_file: the path of the file
    @param returned: True: return the text read from the file, otherwise don't
    @param case_sensitive: True: word is case sensitive, False: case insensitive and lowercase is used
    """
    def read_word_from_file(self, org_file="word.txt", returned=False, case_sensitive=False):
        with open(org_file, "r") as f:
            for line in f:
                self._long_test += line if case_sensitive else line.lower()
        if returned:
            return self._long_test

    """
    parse(remove punctuation and digits) the text read from external file
    and add all the word into list
    @param
    """
    def parse_words(self):
        parsed_words = ''.join([c for c in self._long_test if c not in self._exclude])
        self._word_list = parsed_words.split()

    """
    calculate the occurrence of word with Counter
    @return: list of tuple which display the word and occurrence in desc
    """
    def calculate_word_occurrence_with_counter(self):
        return Counter(self._word_list).most_common()

    """
    calculate the occurrence of word with defaultdict, just a different way to implement
    @return: list of tuple which display the word and occurrence in desc
    """
    def calculate_word_occurrence(self):
        a_dict = defaultdict(int)
        for word in self._word_list:
            a_dict[word] += 1
        return sorted(a_dict.items(), key=itemgetter(1), reverse=True)


if __name__ == "__main__":
    import os
    os.system("clear")

    check_word = CheckWord()
    check_word.read_word_from_file()
    check_word.parse_words()
    print check_word.calculate_word_number_with_counter()
