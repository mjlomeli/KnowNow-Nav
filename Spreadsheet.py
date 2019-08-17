# !/usr/bin/env python

"""Spreadsheet

Opens a CSV spreadsheet for reading and searching operations.

Ideas: pickle handling with __call__ && __init__, print formatting,
"""
from prettytable import PrettyTable
from pathlib import Path
import csv

# default required values
PATH = Path.cwd()
DEFAULT_SPREADSHEET = "Patient Insights - Insights.csv"
DEFAULT_TEXT_LENGTH = 30
NORM_HEADERS = {
    'Topic': 'topic',
    'Date discussion (month/ year)':'date',
    'Patient Query/ Inquiry':'query',
    'Specific patient profile':'profile',
    'Patient cohort (definition)':'cohort',
    'Category tag':'category',
    'Secondary tags':'secondary',
    'Patient insight':'insights',
    'Volunteers':'volunteers',
    'Discussion URL':'url',
    'Notes/ comments/ questions':'comments',
    "Smruti Vidwans comments/ Topics": 'professor_comments'}


# program's author information and licenses
__author__ = "Mauricio Lomeli"
__date__ = "8/15/2019"
__license__ = "MIT"
__version__ = "0.0.0.1"
__maintainer__ = "Mauricio Lomeli"
__email__ = "mjlomeli@uci.edu"
__status__ = "Prototype"


class Spreadsheet:
    """
    If DEFAULT_SPREADSHEET and NORM_HEADERS are kept, 'Patient Insights - Insights.csv' will
    be the CSV that it will be reading. Else, replace with a file in the same directory or specified path.
    NORM_HEADERS truncates the fieldnames to a single word without spaces, this is important if integrating
    with flask (can't use the . function on variables with white space).

    Ex:
        from Spreadsheet import Spreadsheet
        sheet = Spreadsheet()
        sheet = Spreadsheet('Patient Insights - Insights.csv')
        sheet = Spreadsheet('Patient Insights - Insights.csv', NORM_HEADERS) # assume NORM_HEADERS is defined


    """
    def __init__(self, spreadsheet=DEFAULT_SPREADSHEET, headers=NORM_HEADERS):
        self.title = spreadsheet
        self.real_headers = None
        self.norm_headers = headers
        self.headers = None
        self.book = None
        self.spreadsheet = []
        self.__index = 0
        if spreadsheet is not None:
            self.assemble(spreadsheet)
        if self.norm_headers is not None:
            self.normalize(headers)
        else:
            self.headers = self.real_headers

    def assemble(self, spreadsheet):
        with open(Path(spreadsheet), 'r', newline="", encoding="utf-8") as f:
            content = csv.DictReader(f)
            self.real_headers = content.fieldnames
            self.book = {header: index for index, header in enumerate(self.real_headers)}
            self.spreadsheet = [list(element.values()) for element in content]

    def getColumn(self, fieldname):
        return [item[self.book[fieldname]] for item in self.spreadsheet]

    def find(self, value):
        return [row for row in self.spreadsheet if value in row]

    def convertToDict(self, item):
        if isinstance(item, list) and len(item) > 0:
            if isinstance(item[0], list) and len(item[0]) > 0:
                return [dict(zip(self.headers, value)) for value in item]
            elif not isinstance(item[0], list):
                return dict(zip(self.headers, item))
        return None

    def textLength(self, text, length=DEFAULT_TEXT_LENGTH):
        if isinstance(text, list):
            return [value[:length] + '...' if len(value) > length else value for value in text]
        elif isinstance(text, str):
            if len(text) > length:
                return text[:length] + '...'
            else:
                return text
        else:
            return ''

    def normalize(self, headers):
        self.headers = list(headers.values())
        self.book = {header: index for index, header in enumerate(self.headers)}

    def __contains__(self, item):
        if item in self.real_headers:
            return True
        else:
            for row in self.spreadsheet:
                if item in row:
                    return True
        return False

    def __getitem__(self, item):
        if isinstance(item, str):
            if self.headers is not None and item in self.headers:
                return self.getColumn(item)
            elif item in self.real_headers:
                return self.getColumn(self.norm_headers[item])
            else:
                return self.find(item)
        elif isinstance(item, tuple):
            pos1, pos2 = item
            if isinstance(pos1, str) and isinstance(pos2, str):
                return [element.values() for element in self.spreadsheet if element[pos1] == pos2]
            elif isinstance(pos1, int) and isinstance(pos2, str):
                return self.spreadsheet[pos1 - 1][pos2]
        elif isinstance(item, int) or isinstance(item, slice):
            return self.spreadsheet[item]

    def __len__(self):
        return len(self.spreadsheet)

    def __iter__(self):
        self.__index = 0
        return self

    def __next__(self):
        if self.__index >= len(self.spreadsheet):
            raise StopIteration
        item = self.spreadsheet[self.__index]
        self.__index += 1
        return item

    def __call__(self, spreadsheet=DEFAULT_SPREADSHEET):
        with open(Path(spreadsheet), 'r', newline="", encoding="utf-8") as f:
            content = csv.DictReader(f)
            for element in content:
                temp = list(element.values())
                if temp not in self.spreadsheet:
                    self.spreadsheet.append(temp)

    def __format__(self, format_spec):
        #TODO: "Sheet has at columns topic: {a}".format('column')"
        pass

    def __str__(self):
        table = PrettyTable(self.real_headers)
        for head in self.real_headers:
            table.align[head] = 'l'
        for content in self.spreadsheet:
            table.add_row(self.textLength(content))
        return str(table)


if __name__ == '__main__':
    print("Initializing with arguments: Spreadsheet(DEFAULT_SPREADSHEET, NORM_HEADERS)")
    sheet = Spreadsheet(DEFAULT_SPREADSHEET, NORM_HEADERS)
    sheet = Spreadsheet(DEFAULT_SPREADSHEET, NORM_HEADERS)
    print("Initializing default constructor: Spreadsheet()")
    sheet = Spreadsheet()

    print("Iterating through Spreadsheet")
    for row in sheet[:3]:
        print(row)
