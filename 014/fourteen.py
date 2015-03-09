# -*- coding: utf-8 -*-

import json
import xlwt
from collections import OrderedDict


class WriteToXLS(object):

    """
    initialize parameters
    @param work_sheet: the name of work sheet, default is student
    """
    def __init__(self, work_sheet="student"):
        self._data = None
        self._workbook = xlwt.Workbook(encoding="utf-8")
        self._work_sheet = self._workbook.add_sheet(work_sheet)

    """
    read data from file
    @param file_path: the file path
    """
    def read_from_file(self, file_path="student.txt"):
        with open(file_path, "r") as f:
            try:
                self._data = json.loads(f.read(), object_pairs_hook=OrderedDict)
            except:
                self._data = OrderedDict()

    """
    write data into xls file
    @param xls_file: the output xls file
    """
    def write_to_xls(self, xls_file="student.xls"):
        result = ()
        for index, list_value in self._data.items():
            current_result = (index,) + tuple([d for d in list_value])
            result = result + (current_result,)

        for i, row in enumerate(result):
            for j, col in enumerate(row):
                self._work_sheet.write(i, j, col)

        self._workbook.save(xls_file)


if __name__ == "__main__":
    write_to_xls = WriteToXLS()
    write_to_xls.read_from_file()
    print write_to_xls.write_to_xls()
