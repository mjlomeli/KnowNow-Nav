# !/usr/bin/env python

"""SQLdriver

If the description is long, the first line should be a short summary of SQLdriver.py
that makes sense on its own, separated from the rest by a newline.
"""

from pathlib import Path
import mysql.connector


__author__ = "Mauricio Lomeli"
__date__ = "8/21/2019"
__license__ = "MIT"
__version__ = "0.0.0.1"
__maintainer__ = "Mauricio Lomeli"
__email__ = "mjlomeli@uci.edu"
__status__ = "Prototype"


# default required values
PATH = Path.cwd()
DEFAULT_DATA = str(PATH / Path('data') / Path("PatientInsights.sql"))
DEFAULT_TEXT_LENGTH = 30
NORM_HEADERS = {
    'Topic': 'topics',
    'Date discussion (month/ year)': 'dates',
    'Patient Query/ Inquiry': 'queries',
    'Specific patient profile': 'patient_profile',
    'Patient cohort (definition)': 'cohort',
    'Category tag': 'category',
    'Secondary tags': 'secondary_tags',
    'Patient insight': 'insights',
    'Volunteers': 'volunteers',
    'Discussion URL': 'url',
    'Notes/ comments/ questions': 'comments',
    "Smruti Vidwans comments/ Topics": 'professor_comment'}


class SQLDriver:
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

    def __init__(self, file=DEFAULT_DATA, headers=NORM_HEADERS):
        """
        Initializes the Spreadsheet.
        :param spreadsheet: the path of the csv file, else the default file is ued.
        :param headers: normalized headers (conversion of the csv headers to truncated names).
        """
        driver.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
        driver.setencoding(encoding='utf-8')
        self.__driver = sql.connect(r'Server=(localdb)\v11.0;Integrated Security=true;')
        self.title = spreadsheet
        self.real_headers = None
        self.__norm_headers = headers
        self.headers = None
        self.__book = None
        self.spreadsheet = []
        self.__index = 0
        if spreadsheet is not None:
            self.__assemble(spreadsheet)
        if self.__norm_headers is not None:
            self.__normalize(headers)
        else:
            self.headers = self.real_headers

    def __assemble(self, spreadsheet):
        """

        :param spreadsheet:
        :return:
        """
        with open(Path(spreadsheet), 'r', newline="", encoding="utf-8") as f:
            content = csv.DictReader(f)
            self.real_headers = content.fieldnames
            self.__book = {header: index for index, header in enumerate(self.real_headers)}
            self.spreadsheet = [list(element.values()) for element in content]

    def getColumn(self, fieldname):
        return [item[self.__book[fieldname]] for item in self.spreadsheet]

    def find(self, value):
        return [row for row in self.spreadsheet if value in row]

    def convertToDict(self, item):
        if isinstance(item, list) and len(item) > 0:
            if isinstance(item[0], list) and len(item[0]) > 0:
                print(item[0])
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

    def __normalize(self, headers):
        self.headers = list(headers.values())
        self.__book = {header: index for index, header in enumerate(self.headers)}

    def max_results(self, min_value=4):
        omit = list(set(self['volunteers'] + self['comments'] + self['professor_comments']))
        items = set([x for element in self.spreadsheet for x in element if x not in omit])
        dict_items = {}
        for element in items:
            length = len(sheet[element])
            if length > min_value:
                if length not in dict_items:
                    dict_items[length] = [element]
                else:
                    dict_items[length].append(element)
        return dict_items

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
                return self.getColumn(self.__norm_headers[item])
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
        # TODO: "Sheet has at columns topic: {a}".format('column')"
        pass

    def __str__(self):
        table = PrettyTable(self.real_headers)
        for head in self.real_headers:
            table.align[head] = 'l'
        for content in self.spreadsheet:
            table.add_row(self.textLength(content))
        return str(table)


if __name__ == '__main__':
    print('\033[92m' + "Initializing with arguments: Spreadsheet(DEFAULT_SPREADSHEET, NORM_HEADERS)" + '\033[0m')
    sheet = Spreadsheet(DEFAULT_SPREADSHEET, NORM_HEADERS)
    sheet = Spreadsheet(DEFAULT_SPREADSHEET, NORM_HEADERS)

    print('\033[92m' + "Initializing default constructor: Spreadsheet()" + '\033[0m')
    sheet = Spreadsheet()

    print('\033[92m' + "Iterating through first 3 rows in Spreadsheet" + '\033[0m')
    for row in sheet[:3]:
        print(row)

    print('\033[92m' + "Find row with 'Specific Therapy Inquries'" + '\033[0m')
    print(sheet['Specific Therapy Inquries'])

    print('\033[92m' + "Find something that doesn't exist" + '\033[0m')
    print(sheet['it shouldnt exist'])

    print('\033[92m' + "First item in the Spreadsheet" + '\033[0m')
    print(sheet[0])

    response = input('\033[31m' + "Would you like to print the table?" + '\033[0m')
    if 'y' in response.lower():
        print(sheet)
