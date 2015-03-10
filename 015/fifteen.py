# -*- coding: utf-8 -*-

"""
Please see 014 for comments.
"""
import os
import xlwt
import json
from collections import OrderedDict


class WriteToXls(object):

    def __init__(self, work_sheet="city"):
        self._data = OrderedDict()
        self._workbook = xlwt.Workbook(encoding="utf-8")
        self._work_sheet = self._workbook.add_sheet(work_sheet)

    def read_from_file(self, file_path="city.txt"):
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                try:
                    self._data = json.loads(f.read(), object_pairs_hook=OrderedDict)
                except:
                    pass

    def write_to_xls(self, xls_file="city.xls"):
        print self._data
        result = ()
        for key, value in self._data.items():
            result = result + ((key, value), )

        for i, row in enumerate(result):
            for j, col in enumerate(row):
                self._work_sheet.write(i, j, col)
        self._workbook.save(xls_file)

if __name__ == "__main__":
    write_to_xls = WriteToXls()
    write_to_xls.read_from_file()
    write_to_xls.write_to_xls()
