# -*- coding: utf-8 -*-

"""
有个目录，里面是你自己写过的程序，统计一下你写过多少行代码。包括空行和注释，但是要分别列出来.
calculate how many code(lines) do you write in a program, including whitespace and comments, list them respectively
"""
import os
from collections import defaultdict

ONE_LINE_COMMENT_TYPE = ('#', )
MULTIPLE_LINE_COMMENT_TYPE = ('"""', )
FILE_TYPE = ["*.py"]

#in order to ignore the first line
IGNORE_LINES = 1

class CodeChecker(object):

    def __init__(self):
        self._dict = {}

    def read_file(self, file_path):
        result_dict = defaultdict(int)
        file_name = file_path.rsplit("/", 1)[1]

        with open(file_path, "r") as f:
            # remove lines on the top
            for _ in range(IGNORE_LINES):
                next(f)

            #TODO: the logic here should be improved later
            counter = 0
            for number, line in enumerate(f, 1):
                if counter != 0:
                    if line.startswith(MULTIPLE_LINE_COMMENT_TYPE):
                        result_dict["comments"] += number - counter
                        counter = 0
                    continue
                line = line.strip()
                len_line = len(line)
                if len_line == 0:
                    result_dict["whitespace"] += 1
                elif line.startswith(ONE_LINE_COMMENT_TYPE):
                        result_dict["comments"] += 1
                elif line.startswith(MULTIPLE_LINE_COMMENT_TYPE):
                        result_dict["comments"] += 1
                        counter = number
                else:
                    result_dict["code"] += 1

        self._dict[file_name] = dict(result_dict)

    def _read_all_files_by_glob(self, dir_path):
        import glob
        all_files = [files for file_type in FILE_TYPE for files in glob.glob(os.path.abspath(os.path.join(dir_path, file_type)))]
        for one_file in all_files:
            self.read_file(one_file)

    def _read_all_files_by_oswalk(self, dir_path):
        import fnmatch
        all_files = [os.path.abspath(os.path.join(root, files)).replace('\\', '/') for root, subdir, filenames in os.walk(dir_path)
                                                                                for file_type in FILE_TYPE
                                                                                for files in fnmatch.filter(filenames, file_type)]
        for one_file in all_files:
            self.read_file(one_file)

    def read_all_files(self, method="glob", dir_path=os.getcwd()):
        result = getattr(self, "_read_all_files_by_"+method, None)
        if result:
            result(dir_path=dir_path)

    def get_result(self):
        return self._dict


if __name__ == "__main__":
    code_checker = CodeChecker()
    code_checker.read_all_files()
    print code_checker.get_result()

