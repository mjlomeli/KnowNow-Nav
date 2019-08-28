# !/usr/bin/env python

"""Row

If the description is long, the first line should be a short summary of Row.py
that makes sense on its own, separated from the rest by a newline.
"""

from pathlib import Path
from Cell import Cell
from prettytable import PrettyTable
from Spreadsheet import Spreadsheet
from datetime import date
import lxml as html

__author__ = "Mauricio Lomeli"
__date__ = "8/17/2019"
__license__ = "MIT"
__version__ = "0.0.0.1"
__maintainer__ = "Mauricio Lomeli"
__email__ = "mjlomeli@uci.edu"
__status__ = "Prototype"

_STRING_LIMIT = 15
_TESTING = False
_NEO4J_RUNNING = False
_NORMALIZE_HEADERS = True
_NORMALIZE_NODE_HEADERS = True
_DEFAULT_SPREADSHEET = Path.cwd() / Path("data") / Path("insights.csv")
_DEFAULT_TEXT_LENGTH = 30
_PICKLE = Path().cwd() / Path('data') / Path('index.pickle')

_need_logic_linking = {
    'Associated Side effect': [('mitigated by', 'Intervention mitigating side effect')],
    'Intervention': [('causes', 'Associated Side effect')],
    'Intervention mitigating side effect': []
}
_need_linking = {
    'Intervention': [('causes', 'Associated Side effect'), ('fight against', 'Patient Cohort (Definition)')],
    'Associated Side effect': [('mitigated by', 'Intervention mitigating side effect')]
    # 'Associated Side effect': [('lasted for', 'Duration')],
    # 'Associated Side effect': [('occurred after intervention', 'Duration')]}
}

_TAGS = [int, str, date, list, str, str, list, list, int, list, list, list, list, str,
         str, str, str, str, str, html, list, list, list, list, list, list, list, list]

_NORM_HEADERS = {'id': 'id', 'Topic': 'topic', 'Date Discussion (Month/Year)': 'date', 'Query Tag': 'query_tag',
                 'Patient Query/inquiry': 'query', 'Specific Patient Profile': 'profile',
                 'Patient Cohort (Definition)': 'cohort', 'Tumor (T)': 'tumor', 'Tumor Count': 'tumor_count',
                 'Node (N)': 'node', 'Metastasis (M)': 'metastasis', 'Grade': 'grade', 'Recurrence': 'recurrence',
                 'Category Tag': 'category', 'Intervention': 'intervention', 'Associated Side effect': 'side_effects',
                 'Intervention mitigating side effect': 'int_side_effects', 'Patient Insight': 'insights',
                 'Volunteers': 'volunteers', 'Discussion URL': 'url', 'HER2': 'HER2', 'HER': 'HER', 'BRCA': 'BRCA',
                 'ER': 'ER', 'HR': 'HR', 'PR': 'PR', 'RP': 'RP', 'RO': 'RO'}
_REGULAR_HEADERS = ['id', 'Topic', 'Date Discussion (Month/Year)', 'Query Tag', 'Patient Query/inquiry',
                    'Specific Patient Profile', 'Patient Cohort (Definition)', 'Tumor (T)', 'Tumor Count', 'Node (N)',
                    'Metastasis (M)', 'Grade', 'Recurrence', 'Category Tag', 'Intervention', 'Associated Side effect',
                    'Intervention mitigating side effect', 'Patient Insight', 'Volunteers', 'Discussion URL', 'HER2',
                    'HER', 'BRCA', 'ER', 'HR', 'PR', 'RP', 'RO']


class Row:
    total_rows = 0
    __auto_id = 0

    def __init__(self, cells=None, headers=_REGULAR_HEADERS, tags=_TAGS):
        # TODO: need to change id structure to row:column, 0:0, 0:1
        self.headers = headers
        self.norm_headers = None
        self.length = 0
        self.id = None
        self.tags = tags
        self.__row = None
        self.__index = 0
        self.__assemble(cells, headers)

    def __assemble(self, cells, headers=None):
        if cells is None:
            self.__row = None
        elif isinstance(cells, str):
            row = {0: Cell(cells)}
        elif isinstance(cells, Cell):
            headers = [cells.header]
            row = {cells.header: cells}
        elif isinstance(cells, list) and len(cells) > 0:
            if isinstance(cells[0], Cell):
                headers = [cell.header for cell in cells]
                row = {cell.header: cell for cell in cells}
            elif isinstance(cells[0], str):
                if self.headers is None:
                    row = {i: Cell(cell[i]) for i, cell in enumerate(cells)}
                else:
                    row = {self.headers[i]: Cell(cell) for i, cell in enumerate(cells)}
                headers = list(row.keys())
        elif isinstance(cells, Row):
            headers = list(cells.__row.keys())
            row = cells.__row
        else:
            raise TypeError('The constructor accepts only type Row, Cell, and list of Cells')
        if isinstance(headers, list) and isinstance(cells, list):
            assert (len(headers) == len(cells))
            self.headers = headers
            self.id = Row.__auto_id
            self.__row = row
            self.__length = 0 if row is None else len(row)
            self.norm_headers = _NORM_HEADERS if _NORMALIZE_HEADERS else None
            Row.__auto_id += 1
            self.__set_associations()

    def __set_associations(self):
        for header in self.headers:
            associates = {}
            if header in _need_logic_linking:
                associates = self.__eval_logic_and_link(header)
            if header in _need_linking:
                self.__link_associations(header, associates)



    def __link_associations(self, header, associates=None):
        if isinstance(_need_linking, dict):
            if header in _need_linking and associates is not None:
                if isinstance(self.__row[header], Cell):
                    for link, next_cells_header in _need_linking[header]:
                        for assoc in associates:
                            cell = self.__row[header]
                            cell.setNext(Cell(assoc, next_cells_header), link)
                            # TODO: finish this part where we link more

    def __eval_logic_and_link(self, header):
        if isinstance(self.__row[header], Cell):
            cell = self.__row[header]
            if cell.content is not None and cell.content is not '':
                if 'OR' in cell.content:
                    ANDS = [ands.strip() for ands in cell.content.split('OR')]
                    return ANDS
                else:
                    return [cell.content]
            else:
                return None

    def __iter__(self):
        self.__index = 0
        return self

    def __next__(self):
        if self.__index >= len(self.__list_values()):
            raise StopIteration
        temp = self.__list_values()[self.__index]
        self.__index += 1
        return temp

    def __len__(self):
        return len(self.__list_values())

    def __contains__(self, item):
        return item in self.__row.keys() or item in self.__list_values()

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.__list_values()[item]
        elif isinstance(item, str):
            if _NORMALIZE_HEADERS:
                if item in _NORM_HEADERS:
                    return self.__row[_NORM_HEADERS[item]]
                elif item in self.headers:
                    return self.__row[item]
                else:
                    return None
            return self.__row[item]
        elif isinstance(item, Cell):
            return self.__row[item.id]
        elif isinstance(item, int) or isinstance(item, slice):
            print(self.__row)
            return list(self.__row.values())[item]

    def keys(self):
        return self.__row.keys()

    def values(self):
        return self.__list_values()

    def __str__(self):
        if self.__row is not None:
            keys = list(self.__row.keys())
            table = PrettyTable(keys)
            for head in keys:
                table.align[head] = 'c'
            table.add_row([value.content[:_STRING_LIMIT] for value in self.__row.values()])
            return str(table)
        else:
            return ''

    def __and__(self, other):
        return False

    def __or__(self, other):
        return False

    def __xor__(self, other):
        return False

    def __eq__(self, other):
        return False

    def __ne__(self, other):
        return True

    def __gt__(self, other):
        return False

    def __lt__(self, other):
        return False

    def __list_values(self):
        return list(self.__row.values())

    def __del__(self):
        Row.total_rows -= 1


def _store(index, key, id=None):
    pass


def main():
    sheet = Spreadsheet()
    practice = [Row(sheet[i], sheet.headers) for i in range(25)]
    print(practice[0])


def testRow():
    pass


def testRow():
    try:
        sheet = Spreadsheet()
        message = "Initializing with arguments: Row(sheet[0], sheet.headers)"
        row = Row(sheet[0], sheet.headers)
        print('\033[1m' + '\033[92m' + "PASS: " + message + '\033[0m')

        message = "Initializing default constructor: Row()"
        r = Row()
        print('\033[1m' + '\033[92m' + "PASS: " + message + '\033[0m')

        message = "Iterating through first 3 rows in Spreadsheet"
        assert len(row[:3]) == 3
        for cell in row[:3]:
            pass
        print('\033[1m' + '\033[92m' + "PASS: " + message + '\033[0m')

        message = "Find row with 'Associated Side effect'"
        assert len(row['Associated Side effect']) > 0
        print('\t' + str(row['Associated Side effect']))
        print('\033[1m' + '\033[92m' + "PASS: " + message + '\033[0m')

        message = "Find something that doesn't exist"
        assert row['it shouldnt exist'] is None
        print('\033[1m' + '\033[92m' + "PASS: " + message + '\033[0m')

        message = "First cell in the Row"
        if isinstance(row[0], Cell) and len(row[0]) > 0:
            print('\033[1m' + '\033[92m' + "PASS: " + message + '\033[0m')

        message = "Printing the table"
        response = input("Would you like to print the table?")
        if 'y' in response.lower():
            print(row)

    except Exception:
        print('\033[1m' + '\033[31m' + "FAIL:" + message + '\033[0m')


if __name__ == '__main__':
    main()
