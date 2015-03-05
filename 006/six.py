# -*- coding: utf-8 -*-

"""
你有一个目录，放了你一个月的日记，都是 txt，为了避免分词的问题，假设内容都是英文，请统计出你认为每篇日记最重要的词。
count the most important word in a diary file(txt file) from a directory. suppose that all the content are English words.
"""

import os
import string
from collections import Counter

CHECK_FILE_TYPE = ['*.txt']

class diaryChecker(object):

    """
    initialize parameters
    @param path:the directory of diaries
    """
    def __init__(self, path=None):
        self._path = path
        self._exclude = string.punctuation + string.digits
        self._diary_dict = {}

    """
    invoke checking all the diaries function according to the method
    @param method: which method is used to check diary
    @param path: the directory of diaries
    """
    def check_all_diaries(self, method="glob", path=os.getcwd()):
        result = getattr(self, "_check_all_diaries_by_"+method, None)
        if result is not None:
            result(path)

    """
    checking all the diaries by using glob
    @param path: the direcory of diaries
    """
    def _check_all_diaries_by_glob(self, path):
        if os.path.exists(path):
            import glob
            self._path = path
            files_list = [files for file_type in CHECK_FILE_TYPE for files in glob.glob(os.path.abspath(os.path.join(self._path, file_type)))]
            for one_file in files_list:
                most_word, diary_name = self.check_diary(one_file)
                self._diary_dict[diary_name] = most_word

    """
    check one diary file
    @param diary_file: the path and name of the diary file
    @param case_sensitive: True is case sensitive while reading data from file, otherwise False
    @return: (the_most_important_word, diary_name)
    """
    def check_diary(self, diary_file="/diary.txt", case_sensitive=False):
        long_text = ""
        diary_name = diary_file.rsplit("/", 1)[1]
        with open(diary_file, "r") as f:
            for line in f:
                long_text += line if case_sensitive else line.lower()
        return self.counter_word(long_text), diary_name

    """
    count the most important word in the content
    @param counter_text: the whole content from one diary files
    @return: the most important word
    """
    def counter_word(self, counter_text):
        word_list = ''.join([c for c in counter_text if c not in self._exclude]).split()
        return Counter(word_list).most_common()[0][0]

    """
    get the result of all the diaries
    @return: a dict that contains key:diary name, value: the most important word in the diary
    """
    def get_result(self):
        return self._diary_dict


if __name__ == "__main__":
    diary_checker = diaryChecker()
    diary_checker.check_all_diaries()
    print diary_checker.get_result()


