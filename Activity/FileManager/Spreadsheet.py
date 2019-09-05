# !/usr/bin/env python

"""Spreadsheet
Opens a CSV spreadsheet for reading and searching operations.
Ideas: pickle handling with __call__ && __init__, print formatting,
"""
from prettytable import PrettyTable
from pathlib import Path
import csv

__author__ = "Mauricio Lomeli"
__date__ = "8/22/2019"
__credits__ = ["Rebecca Zhuo, Smruti Vidwans"]
__license__ = "MIT"
__version__ = "0.0.0.2"
__maintainer__ = "Mauricio Lomeli"
__email__ = "mjlomeli@uci.edu"
__status__ = "Prototype"

# default required values
_DEFAULT_SPREADSHEET = Path.cwd() / Path('data') / Path('insights.csv')
_DEFAULT_TEXT_LENGTH = 30

_NORM_HEADERS = {'id': 'id', 'Topic': 'topic', 'Date Discussion (Month/Year)': 'date', 'Query Tag': 'query_tag',
                 'Patient Query/inquiry': 'query', 'Specific Patient Profile': 'profile',
                 'Patient Cohort (Definition)': 'cohort', 'Tumor (T)': 'tumor', 'Tumor Count': 'tumor_count',
                 'Node (N)': 'node', 'Metastasis (M)': 'metastasis', 'Grade': 'grade', 'Recurrence': 'recurrence',
                 'Category Tag': 'category', 'Intervention': 'intervention', 'Associated Side effect': 'side_effects',
                 'Intervention mitigating side effect': 'int_side_effects', 'Patient Insight': 'insights',
                 'Volunteers': 'volunteers', 'Discussion URL': 'url', 'HER2': 'HER2', 'HER': 'HER', 'BRCA': 'BRCA',
                 'ER': 'ER', 'HR': 'HR', 'PR': 'PR', 'RP': 'RP', 'RO': 'RO'}


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
        sheet['topic'] = ['About to start Radiation ... Need advice on what to expect', 'Afinitor T...
        sheet[0] = ['About to start Radiation ... Need advice on what to expect', 'Dec 2016...
        [row for row in sheet] -> [['About to start Radiation ... Need advice on what to expect', 'Dec 2016', 'what...
        'topic' in sheet
        'August 2018' in sheet
        print(sheet)
    """

    def __init__(self, file=_DEFAULT_SPREADSHEET, norm_headers=_NORM_HEADERS):
        self.name = Path(file).name
        self.headers = []
        self.norm_headers = []
        self.__norm_to_real = {}  # converts norm_headers into headers
        self.__spreadsheet = []  # rows of csv file
        self.__index = 0
        self.__assemble(file, norm_headers)

    def __assemble(self, file, norm_headers):
        if file is not None and Path(file).exists():
            with open(file, 'r', newline="", encoding="utf-8") as f:
                content = csv.DictReader(f)
                self.headers = content.fieldnames
                self.__spreadsheet = [list(element.values()) for element in content]

        message = "Norm headers do not match with the orgininal headers"
        if isinstance(norm_headers, dict):
            if all([real in self.headers for real in list(norm_headers.keys())]):
                self.norm_headers = list(norm_headers.values())
                self.__norm_to_real = {norm: real for real, norm in norm_headers.items()}
            elif all([real in self.headers for real in list(norm_headers.values())]):
                self.norm_headers = list(norm_headers.keys())
                self.__norm_to_real = norm_headers
            else:
                assert False, message
        elif isinstance(norm_headers, list):
            self.norm_headers = norm_headers
            assert len(norm_headers) == len(self.headers), message
            self.__norm_to_real = dict(zip(norm_headers, self.headers))

    def keys(self):
        return self.headers

    def exists(self, item=None):
        if item is None:
            return self.__spreadsheet is not None
        else:
            return self.has(item)

    def has(self, item):
        if isinstance(item, str):
            if item in self.norm_headers or item in self.headers:
                return True
            else:
                for rows in self.__spreadsheet:
                    if item in rows:
                        return True
                return False
        elif isinstance(item, list):
            if len(item) == 0:
                return False
            elif isinstance(item[0], str):
                items_non_headers = [e for e in item if e not in self.headers and e not in self.norm_headers]
                result = dict(zip(items_non_headers, [False] * len(items_non_headers)))
                for rows in self.__spreadsheet:
                    for element in items_non_headers:
                        if element in rows:
                            result[element] = True
                    if all(result.values()):
                        return True
                return False
            else:
                return self.__has_all(item)
        elif isinstance(item, dict):
            if len(item) == 0:
                return False
            has_all = True
            for keys in item.values():
                if keys not in self.headers or keys not in self.norm_headers:
                    return False
                else:
                    if isinstance(item[keys], list):
                        for rows in item[keys]:
                            if rows not in self[keys]:
                                return False
                    elif isinstance(item[keys], str):
                        if not item[keys] in self[keys]:
                            return False
            return has_all
        else:
            return False

    def at(self, item):
        if isinstance(item, list):
            if len(item) == len(self.headers) and item in self.__spreadsheet:
                return self.__spreadsheet.index(item)
        elif isinstance(item, str):
            if item in self.headers:
                return self.headers.index(item)
            elif item in self.norm_headers:
                return self.norm_headers.index(item)
            else:
                for i, row in enumerate(self.__spreadsheet):
                    if item in row:
                        return i, row.index(item)
        return None

    def getColumn(self, fieldname):
        if fieldname in self.norm_headers:
            index = self.norm_headers.index(fieldname)
            return [item[index] for item in self.__spreadsheet]
        elif fieldname in self.headers:
            index = self.headers.index(fieldname)
            return [item[index] for item in self.__spreadsheet]

    def find(self, value):
        return [rows for rows in self.__spreadsheet if value in rows]

    def convertToDict(self, item=None, norm=True):
        headers = self.norm_headers if norm else self.headers
        if item is None:
            columns = [self[col] for col in headers]
            return dict(zip(headers, columns))
        elif isinstance(item, list) and len(item) > 0:
            message = "Some items do not match the same length as the headers."
            if isinstance(item[0], list) and len(item[0]) == len(headers):
                if all([len(headers) == len(content) for content in item]):
                    return [dict(zip(headers, value)) for value in item]
                else:
                    assert False, message
            elif not isinstance(item[0], list) and len(item) == len(headers):
                return dict(zip(headers, item))
            else:
                assert False, message
        return None

    def trunc_text(self, text, length=_DEFAULT_TEXT_LENGTH):
        if isinstance(text, list):
            return [value[:length] + '...' if len(value) > length else value for value in text]
        elif isinstance(text, str):
            if len(text) > length:
                return text[:length] + '...'
            else:
                return text
        else:
            return ''

    def most_common(self, num_results=4):
        items = set([x for element in self.__spreadsheet for x in element])
        dict_items = {}
        for element in items:
            if element != '' and element != None:
                length = len(self.find(element))
                if length not in dict_items:
                    dict_items[length] = [element]
                else:
                    dict_items[length].append(element)
        count_list = list(dict_items.keys())
        count_list.sort()
        maximums_list = count_list[::-1][:num_results]
        results = [res for count in maximums_list for res in dict_items[count]]
        return results[:num_results]

    def __like(self, string, compare):
        if len(string) > len(compare):
            added_len = abs(len(string) - len(compare))
            shortest = string if len(string) < len(compare) else compare
            compare = string if len(string) > len(compare) else compare
            string = list(shortest) + ([None] * added_len)
        combined = list(zip(compare, string))
        len_combined = len(combined)
        equality = sum([1 if elem[0] == elem[1] else 0 for elem in combined])
        return equality / len_combined

    def __contains_like(self, string, compare):
        equality = sum([1 if letter in compare else 0 for letter in string])
        return equality / len(string)

    def __intersection(self, raw, required, exact=False):
        result = []
        req = [elem.lower() for elem in required]
        raw = [elem.split(';') for elem in raw]
        for item in raw:
            adding = []
            for words in item:
                if len(words) > 0:
                    if words.lower() in req:
                        adding.append(words)
                    elif not exact:
                        words = words.lower().strip().replace('/', ' ').replace('\n', ' ')
                        for capital in req:
                            tag = capital.lower()
                            if tag not in adding:
                                if words in tag:
                                    adding.append(tag)
                                elif self.__like(words, tag) > 0.85:
                                    adding.append(tag)
                                elif self.__contains_like(words, tag) > 0.85:
                                    div = 1.5
                                    end = int(len(words) // div)
                                    start = 0
                                    while end < len(words) and start < len(words):
                                        if words[start:end] in tag and tag not in adding:
                                            adding.append(tag)
                                        end += 1
                                        start += 1
            result.append(adding)
        return result

    def __has_all(self, item):
        has_all = True
        for index in item:
            if not self.has(index):
                return False
        return has_all

    def __replace(self, arr, list_of_values):
        for i in range(len(arr)):
            for item in list_of_values:
                arr[i] = arr[i].lower().replace(*item)
        return arr

    def __contains__(self, item):
        return self.has(item)

    def __getitem__(self, item):
        if isinstance(item, str):
            if self.headers is not None and item in self.headers:
                return self.getColumn(item)
            elif item in self.norm_headers:
                return self.getColumn(self.__norm_to_real[item])
            else:
                return self.find(item)
        elif isinstance(item, tuple):
            pos1, pos2 = item
            if isinstance(pos1, str) and isinstance(pos2, str):
                return [element.values() for element in self.__spreadsheet if element[pos1] == pos2]
            elif isinstance(pos1, int) and isinstance(pos2, str):
                return self.__spreadsheet[pos1 - 1][pos2]
        elif isinstance(item, int) or isinstance(item, slice):
            return self.__spreadsheet[item]

    def __len__(self):
        return len(self.__spreadsheet)

    def __iter__(self):
        self.__index = 0
        return self

    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            self.__spreadsheet[key[0]][key[1]] = value

    def __next__(self):
        if self.__index >= len(self.__spreadsheet):
            raise StopIteration
        item = self.__spreadsheet[self.__index]
        self.__index += 1
        return item

    def __call__(self, spreadsheet=_DEFAULT_SPREADSHEET):
        with open(Path(spreadsheet), 'r', newline="", encoding="utf-8") as f:
            content = csv.DictReader(f)
            for element in content:
                temp = list(element.values())
                if temp not in self.__spreadsheet:
                    self.__spreadsheet.append(temp)

    def __format__(self, format_spec):
        # TODO: "Sheet has at columns topic: {a}".format('column')"
        pass

    def __str__(self):
        table = PrettyTable(self.headers)
        for head in self.headers:
            table.align[head] = 'l'
        for content in self.__spreadsheet:
            table.add_row(self.trunc_text(content))
        return str(table)


def testSpreadsheet():
    try:
        message = "Initializing with arguments: Spreadsheet(DEFAULT_SPREADSHEET, NORM_HEADERS)"
        sheet = Spreadsheet(_DEFAULT_SPREADSHEET, _NORM_HEADERS)
        print('\033[1m' + '\033[92m' + "PASS: " + message + '\033[0m')

        message = "Initializing default constructor: Spreadsheet()"
        sheet = Spreadsheet()
        print('\033[1m' + '\033[92m' + "PASS: " + message + '\033[0m')

        message = "Iterating through first 3 rows in Spreadsheet"
        assert len(sheet[:3]) == 3
        for row in sheet[:3]:
            pass
        print('\033[1m' + '\033[92m' + "PASS: " + message + '\033[0m')

        message = "Find row with 'Specific Therapy Inquries'"
        assert len(sheet['Specific Therapy Inquries']) > 0
        print('\t' + str(sheet['Specific Therapy Inquries']))
        print('\033[1m' + '\033[92m' + "PASS: " + message + '\033[0m')

        message = "Find something that doesn't exist"
        assert len(sheet['it shouldnt exist']) == 0
        print('\033[1m' + '\033[92m' + "PASS: " + message + '\033[0m')

        message = "First item in the Spreadsheet"
        print('\t' + str(sheet[0]))
        print('\033[1m' + '\033[92m' + "PASS: " + message + '\033[0m')

        message = "Printing the table"
        response = input("Would you like to print the table?")
        if 'y' in response.lower():
            print(sheet)

    except Exception:
        print('\033[1m' + '\033[31m' + "FAIL:" + message + '\033[0m')


if __name__ == '__main__':
    testSpreadsheet()