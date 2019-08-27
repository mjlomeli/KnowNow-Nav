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
                OR = associates['OR']
                AND = associates['AND']
                for link, next_cells_header in _need_linking[header]:
                    if isinstance(self.__row[header], Cell):
                        cell = self.__row[header]
                        self.__row[header].setNext(self.__row[next_cells_header], link)


    def __eval_logic_and_link(self, header):
        if isinstance(self.__row[header], Cell):
            cell = self.__row[header]
            if cell.content is not None and cell.content is not '':
                AND = []
                OR = []
                logic_split = _splitting(cell.content)
                if len(logic_split) > 1 and '' in logic_split:
                    raise SyntaxError('There is an OR and AND without a matching operand.')
                length = len(logic_split)
                i = 2
                while i < length - 1:
                    if 'AND' in logic_split[:i] and 'OR' in logic_split[:i]:
                        raise SyntaxError('Cant have two logical operators side by side.')
                    elif logic_split[:i] == ['AND', 'AND']:
                        raise SyntaxError('Cant have two logical operators side by side.')
                    elif logic_split[:i] == ['OR', 'OR']:
                        raise SyntaxError('Cant have two logical operators side by side.')
                    elif 'AND' in logic_split[:i]:
                        AND.append(logic_split[i-2])
                    elif 'OR' in logic_split[:i]:
                        OR.append(logic_split[i-2])
                    i += 2
                    if i == length - 1:
                        if 'AND' in logic_split[i-1:i+1]:
                            AND.append(logic_split[i])
                        elif 'OR' in logic_split[i-1:i+1]:
                            OR.append(logic_split[i])
            return {'AND': AND, 'OR': OR}

    def __evaluate(self, cell: Cell):
        operators = _splitting(cell.content)
        if '' in operators and len(operators) > 1:
            raise AssertionError('An AND or an OR must be followed by another variable')
        elif '' not in operators:
            if 'NOT' in operators:
                return [' '.join(operators)]
            elif 'OR' in operators:
                return [x for x in operators if x != 'OR']
            elif 'AND' in operators:
                return [' '.join(operators).replace('AND', 'and')]

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


def _splitting(string: str):
    or_pos = None
    and_pos = None
    if 'OR' in string:
        or_pos = string.find('OR')
    if 'AND' in string:
        and_pos = string.find('AND')
    if not or_pos and not and_pos:
        return [string]
    if or_pos is not None:
        if and_pos is not None:
            if and_pos < or_pos:
                left = and_pos
                return [string[:left].strip()] + ['AND'] + _splitting(string[left + 3:].strip())
            else:
                left = or_pos
                return [string[:left].strip()] + ['OR'] + _splitting(string[left + 2:].strip())
        else:
            left = or_pos
            return [string[:left].strip()] + ['OR'] + _splitting(string[left + 2:].strip())
    else:
        if and_pos is not None:
            left = and_pos
            return [string[:left].strip()] + ['AND'] + _splitting(string[left + 3:].strip())
        else:
            raise NotImplementedError('You are not suppose to enter this whatsoever')


def _store(index, key, id=None):
    pass


def main():
    pass


def test():
    pass


if __name__ == '__main__':
    test()
