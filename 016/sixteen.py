# -*- coding: utf-8 -*-

"""
Please see 014 for comments
"""
import os
import xlwt
import json


class WriteToXls(object):

    def __init__(self, work_sheet="numbers"):
        self._data = []
        self._workbook = xlwt.Workbook(encoding="utf-8")
        self._work_sheet = self._workbook.add_sheet(work_sheet)

    def read_from_file(self, file_path="numbers.txt"):
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                try:
                    self._data = json.loads(f.read())
                except:
                    pass

    def write_to_xls(self, xls_file="numbers.xls"):
        for i in range(len(self._data)):
            for j in range(len(self._data[i])):
                self._work_sheet.write(i, j, self._data[i][j])
        self._workbook.save(xls_file)

if __name__ == "__main__":
    write_to_xls = WriteToXls()
    write_to_xls.read_from_file()
    write_to_xls.write_to_xls()
