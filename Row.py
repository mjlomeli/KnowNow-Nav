# !/usr/bin/env python

"""Row

If the description is long, the first line should be a short summary of Row.py
that makes sense on its own, separated from the rest by a newline.
"""

from pathlib import Path
from Cell import Cell
from prettytable import PrettyTable

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

_NORM_HEADERS = {'id': 'id', 'Topic': 'topic', 'Date Discussion (Month/Year)': 'date', 'Query Tag': 'query_tag',
                'Patient Query/inquiry': 'query', 'Specific Patient Profile': 'profile',
                'Patient Cohort (Definition)': 'cohort', 'Tumor (T)': 'tumor', 'Tumor Count': 'tumor_count',
                'Node (N)': 'node', 'Metastasis (M)': 'metastasis', 'Grade': 'grade', 'Recurrence': 'recurrence',
                'Category Tag': 'category', 'Intervention': 'intervention', 'Associated Side effect': 'side_effects',
                'Intervention mitigating side effect': 'int_side_effects', 'Patient Insight': 'insights',
                'Volunteers': 'volunteers', 'Discussion URL': 'url', 'HER2': 'HER2', 'HER': 'HER', 'BRCA': 'BRCA',
                'ER': 'ER', 'HR': 'HR', 'PR': 'PR', 'RP': 'RP', 'RO': 'RO'}


class Row:
    total_rows = 0
    __auto_id = 0

    def __init__(self, cells=None, headers=None):
        # TODO: need to change id structure to row:column, 0:0, 0:1
        self.headers = None
        self.norm_headers = None
        self.length = 0
        self.id = None
        self.__row = None
        self.__index = 0
        self.__assemble(cells)

    def __assemble(self, cells, headers=None):
        if cells is None:
            pass
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
                row = {i: Cell(cell[i], id=i) for i, cell in enumerate(cells)}
                headers = list(row.keys())
        elif isinstance(cells, Row):
            headers = list(cells.__row.keys())
            row = cells.__row
        else:
            raise TypeError('The constructor accepts only type Row, Cell, and list of Cells')

        assert(len(headers) == len(cells))
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
            else:
                #TODO: link them to nothing next
                pass

    def __link_associations(self, header, associates=None):
        if isinstance(_need_linking, dict):
            if header in _need_linking and associates is not None:
                if isinstance(self.__row[header], Cell):
                    for link, next_cells_header in _need_linking[header]:
                        for assoc in associates:
                            cell = self.__row[header]
                            cell.setNext(Cell(assoc),


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
            return self.__row[item]

    def keys(self):
        return self.__row.keys()

    def values(self):
        return self.__list_values()

    def __str__(self):
        keys = list(self.__row.keys())
        table = PrettyTable(keys)
        for head in keys:
            table.align[head] = 'c'
        table.add_row([value.content[:_STRING_LIMIT] for value in self.__row.values()])
        return str(table)

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
    pass


def test():
    pass


if __name__ == '__main__':
    test()
