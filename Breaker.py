# !/usr/bin/env python

"""Breaker

If the description is long, the first line should be a short summary of Breaker.py
that makes sense on its own, separated from the rest by a newline.
"""

from pathlib import Path
from Cell import Cell
from Row import Row
from Writing import Writing
from Spreadsheet import Spreadsheet
from Tokenizer import Tokenizer
import random


PATH = Path.cwd()

__author__ = "Mauricio Lomeli"
__date__ = "8/27/2019"
__maintainer__ = "Mauricio Lomeli"
__email__ = "mjlomeli@uci.edu"
__status__ = "Prototype"


class TestMaker:
    def __init__(self, data_type=None, variable=None):
        a = Cell('hello', 'header')
        b = Cell('some')
        c = Cell()
        d = Row()
        e = Tokenizer
        f = Writing('hello', 'header')
        g = Writing('hi')
        h = Writing()
        i = Spreadsheet()

        self.local = [a, b, c, d, e, f, g, h, i,]
        self.numbers = [-1000, -100010.10, 0, -1, 0.00000001, -0.00000001, 1000000000, 10e200, -10e200, 1e-20, 2e20]
        self.primitives = [None, 'hello', "hello", '', "", chr(12), [], [20], ['21'], [''], {}, {1}, {0}, {0, 1},
                           True, False]
        self.types = [str, int, list, dict, float, bool, tuple]
        self.classes = [Path, Cell, Row, Tokenizer, Writing, Spreadsheet]
        self.logic = ['*', '+', '%', '/', '-', '+=', '-=', 'and', 'or', 'in', '!=', '==',
                         'and', 'or', 'xor', '>', '<', '>=', '<=']

        self.__index = 0
        self.__type = self.local + self.numbers + self.primitives + self.types + self.classes + self.logic
        self.__var = self.local + self.numbers + self.primitives + self.types + self.classes + self.logic

        self.variables = self.__var

        self.test_creating()
        self.test_operations()
        self.test_getting_called()

    def __iter__(self):
        self.__index = 0
        return self

    def test_creating(self):
        for item in self.variables:
            for types in self.types:
                try:
                    types(item)
                    print('\033[92m' + 'Passed: ' + str(types)[13:-1] + '(' + str(type(item))[8:-2] + ')' + '\033[0m')
                except Exception as e:
                    print('\033[31m' + 'Failed: ' + str(types)[13:-1] + '(' + str(type(item))[8:-2] + ')' + '\033[0m')

    def test_operations(self):
        try:
            for item in self.logic:
                for var in self.variables:
                    eval('self.__type' + item + 'self.__type')
                    print('\033[92m' + 'Passed: ' + str(var)[13:-2] + ' ' + str(type(item)) + ' ' + str(var)[
                                                                                                      13:-2] + ' \033[0m')
        except Exception as e:
            print('\033[31m' + 'Failed: ' + str(var)[13:-2] + ' ' + str(type(item)) + ' ' + str(var)[13:-2] + ' \033[0m')


    def test_getting_called(self):
        for item in self.variables:
            for types in self.types:
                try:
                    item(types)
                    print('\033[92m' + 'Passed: ' + str(item)[13:-2] + '(' + str(type(types))[8:-2] + ')' + '\033[0m')
                except Exception as e:
                    print('\033[31m' + 'Failed: ' + str(item)[13:-2] + '(' + str(type(types))[8:-2] + ')' + '\033[0m')

    def __next__(self):
        if self.__index >= len(self.variables):
            raise StopIteration
        temp = self.variables[self.__index]
        self.__index += 1
        return temp


def main():
    TestMaker()


if __name__ == '__main__':
    main()
