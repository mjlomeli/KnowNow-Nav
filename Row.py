# !/usr/bin/env python

"""Row

If the description is long, the first line should be a short summary of Row.py
that makes sense on its own, separated from the rest by a newline.
"""

from Tokenizer import Tokenizer
from Neo4jDriver import *
from getpass import getpass
PATH = Path.cwd()

__author__ = "Mauricio Lomeli"
__date__ = "8/17/2019"
__license__ = "MIT"
__version__ = "0.0.0.1"
__maintainer__ = "Mauricio Lomeli"
__email__ = "mjlomeli@uci.edu"
__status__ = "Prototype"



_TESTING = False
_STRING_LIMIT = 15
_NEO4J_RUNNING = False
_SESSION = openDatabase(input('URI: '), input('Username'), getpass('Password: ')) if _NEO4J_RUNNING else None
_PICKLE = Path().cwd() / Path('data') / Path('index.pickle')
_TOKENIZER = Tokenizer()


_needing_logic = ['intervention', 'side_effects', 'int_side_effects']
_linking_headers = {
    'intervention': [('causes', 'side_effects'), ('against', 'cohort')],
    'side_effects': [('could be mitigated by', 'int_side_effects')]
    # 'side_effects': ('lasted for', 'duration'),
    # 'side_effects': ('occurred after intervention', 'duration')
}

_NORM_HEADERS = {'id': 'id', 'Topic': 'topic', 'Date Discussion (Month/Year)': 'date', 'Query Tag': 'query_tag',
                'Patient Query/inquiry': 'query', 'Specific Patient Profile': 'profile',
                'Patient Cohort (Definition)': 'cohort', 'Tumor (T)': 'tumor', 'Tumor Count': 'tumor_count',
                'Node (N)': 'node', 'Metastasis (M)': 'metastasis', 'Grade': 'grade', 'Recurrence': 'recurrence',
                'Category Tag': 'category', 'Intervention': 'intervention', 'Associated Side effect': 'side_effects',
                'Intervention mitigating side effect': 'int_side_effects', 'Patient Insight': 'insights',
                'Volunteers': 'volunteers', 'Discussion URL': 'url', 'HER2': 'HER2', 'HER': 'HER', 'BRCA': 'BRCA',
                'ER': 'ER', 'HR': 'HR', 'PR': 'PR', 'RP': 'RP', 'RO': 'RO'}
_NODE_HEADER = {'id': 'ID', 'topic': 'Topic', 'date': 'Date', 'query_tag': 'Query Tag', 'query': 'Query',
                'profile': 'Profile', 'cohort': 'Cohort', 'tumor': 'T', 'tumor_count': 'T Count', 'node': 'N',
                'metastasis': 'M', 'grade': 'Grade', 'recurrence': 'Recurr', 'category': 'Category',
                'intervention': 'Intervention', 'side_effects': 'Side Effect', 'int_side_effects': 'Int. Side Eff.',
                'insights': 'Insights', 'volunteers': 'Volunt.', 'url': 'URL', 'HER2': 'HER2', 'HER': 'HER',
                'BRCA': 'BRCA', 'ER': 'ER', 'HR': 'HR', 'PR': 'PR', 'RP': 'RP', 'RO': 'RO'}


class Row:
    total_rows = 0

    def __init__(self, headers=None, cells=None, length=10):
        # TODO: need to change id structure to row:column, 0:0, 0:1
        # TODO: SUM of TF in 0:1, where 0 is the row
        # TODO: UPDATE(TF: empty TF w/ words) -> updated TF
        __total_rows = 0
        self.__row = {}
        self.__length = length
        self.__pos = Row.total_rows + 1
        Row.total_rows += 1
        self.__tf = None
        self.__index = 0
        self.__assemble(headers, cells, length)

    def __assemble(self, headers=None, cells=None, length=10):
        if headers is None:
            headers = [i for i in range(length)]
        if cells is None:
            cells = [Cell(None, None, None)] * length
        else:
            cells = [Cell(txt, head, self.__pos) for txt, head in zip(cells, headers)]
        assert(len(headers) == len(cells))
        self.__row = dict(zip(headers, cells))
        self.__length == len(self.__row)
        self.__set_associations()

    def __set_associations(self):
        for header in self.__row.keys():
            self.__linking_headers(self.__row[header])

    def __linking_headers(self, cell: Cell):
        """
        'intervention': [('causes', 'side_effects'), ('against', 'cohort')]
        """
        if cell.header in _linking_headers:
            for link in _linking_headers[cell.header]:
                if link[1] in self.__row:
                    cell.setNext(self.__row[link[1]], link[0])
                else:
                    cell.setNext(Cell(link[0], link[1] + '_new', 0), link[0])

    def __linking_logic(self, cell: Cell):
        """
        _needing_logic = ['intervention', 'side_effects', 'int_side_effects']
        _linking_headers = {
                    intervention': [('causes', 'side_effects'), ('against', 'cohort')]
        """
        if cell.header in self.__row:
            if cell.content is not None and cell.content is not '':
                operation = self.__evaluate(cell)
                if cell.header not in _linking_headers:
                    for link in operation:
                        cell.setNext(Cell(link, link + '_new', 0))
                else:
                    for items in operation:
                        for linkage in _linking_headers[cell.header]:
                            link_name, to_header = linkage
                            self.__linking_headers(cell, items)
                            #cell.setNext(new_cell, link_name)

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




def _store(index, key, id=None):
    pass


def main():
    pass


def test():
    pass


if __name__ == '__main__':
    test()
