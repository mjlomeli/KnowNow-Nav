# !/usr/bin/env python

"""Document

If the description is long, the first line should be a short summary of Document.py
that makes sense on its own, separated from the rest by a newline.
"""

from prettytable import PrettyTable
from pathlib import Path
from Tokenizer import Tokenizer

# Programs author information
__author__ = "Mauricio Lomeli"
__date__ = "8/22/2019"
__credits__ = ["Rebecca Zhuo, Smruti Vidwans"]
__license__ = "MIT"
__version__ = "0.0.0.1"
__maintainer__ = "Mauricio Lomeli"
__email__ = "mjlomeli@uci.edu"
__status__ = "Prototype"

_TESTING = False
_STRING_LIMIT = 15
_PICKLE = Path().cwd() / Path('data') / Path('index.pickle')
_TOKENIZER = Tokenizer()
_needing_lemma = ['insights', 'topic', 'query', 'profile', ]
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



class Cell(object):
    """
    Holds each individual data. Has higher level of control. Each cell makes up a node.
    """
    cell_total = 0
    cell_global_print = True
    cell_global = []

    def __init__(self, content=None, header_name=None, row_number=None):
        Cell.cell_total += 1
        self.content = content
        self.header = header_name
        self.id = row_number
        self.__tokens = None
        self.__tf = None
        self.__next = {}
        self.__link_name = header_name + ': ' + content if content is not None and header_name is not None else None
        self.__index = 0
        if header_name in _needing_lemma and content is not None and isinstance(content, str):
            self.__tokenize(content)

    def __tokenize(self, content):
        _TOKENIZER.open(content)
        self.__tf = _TOKENIZER.tf
        self.__tokens = list(self.__tf.keys())

    def getTokens(self):
        if self.__tokens is None:
            self.__tokenize(self.content)
        return self.__tokens

    def getTF(self):
        if self.__tf is None:
            self.__tokenize(self.content)
        return self.__tf

    def setNext(self, next_cell, link_name=None):
        if isinstance(next_cell, Cell):
            if next_cell is not None:
                if isinstance(link_name, str):
                    self.__link_name = link_name
                if next_cell.header not in self.__next:
                    self.__next[next_cell.header] = [next_cell]
                else:
                    self.__next[next_cell.header].append(next_cell)
        #TODO: add Jennifer and Anne's code here

    def getNext(self):
        return self.__list_values()
        #TODO: add Jennifer and Anne's code here

    def getLast(self):
        """
        Returns the end of every path if it exists.
        :return: a list of all paths the have a None type
        """
        if self.__next is None or len(self.__next) == 0:
            return [self]
        else:
            Cell.cell_global = []
            temp = self.__getLastHelper(self.__list_values())
            Cell.cell_global = []
            return temp

    def __getLastHelper(self, current):
        if current is None or len(current) == 0:
            return []
        else:
            result = []
            for cell in current:
                if cell not in Cell.cell_global:
                    Cell.cell_global.append(cell)
                    if len(cell.getNext()) == 0:
                        result += [self]
                    else:
                        result += self.__getLastHelper(cell)
            return result

    def __add__(self, other):
        if isinstance(other, str):
            return self.content + other
        elif isinstance(other, Cell):
            self.setNext(other)
        #Todo: add Jennifer and Anne's code here
        #Todo: to be able to link one node to another

    def __contains__(self, item):
        if isinstance(item, str):
            return item in self.content
        elif isinstance(item, Cell):
            return self == item

    def __str__(self):
        Cell.cell_global = []
        result = self.__print()
        Cell.cell_global = []
        return result

    def __print(self):
        content = self.content if len(self.content) < _STRING_LIMIT else self.content[:_STRING_LIMIT-3] + '...'
        next_cell = self.getNext()
        if next_cell is None or len(next_cell) == 0:
            if self.content is not None and self.content is not '':
                return '(' + content + ')-->None\n'
            return 'None\n'
        else:
            result = ''
            for cell in next_cell:
                if cell.header is not '' and cell.header is not None:
                    result += '(' + content + ')-' + self.__link_name + '->'
                    if cell not in Cell.cell_global:
                        Cell.cell_global.append(cell)
                        result += cell.__print()
                    else:
                        cell_content = cell.content if len(cell.content) < _STRING_LIMIT else cell.content[:_STRING_LIMIT-3] + '...'
                        result = result + '(' + cell_content + ')' + '\n'
            return result

    def keys(self):
        return self.__next.keys()

    def values(self):
        return self.__next.values()

    def __iter__(self):
        self.__index = 0
        return self

    def __next__(self):
        if self.__index >= len(self):
            raise StopIteration
        temp = list(self.__list_values())[self.__index]
        self.__index += 1
        return temp

    def __len__(self):
        return len(self.__list_values())

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.__list_values()[item]
        elif isinstance(item, str):
            if item in self.__next:
                return self.__next[item]
        elif isinstance(item, Cell):
            for cell in self.__list_values():
                if item == cell:
                    return cell

    def __setitem__(self, key, value):
        if isinstance(key, str) and key in self.__next:
            if isinstance(value, list):
                for item in value:
                    self.setNext(item)
            elif isinstance(value, Cell):
                self.setNext(value)

    def __get__(self, obj, objtype):
        if _TESTING:
            print('Retrieving ' + str(self.header) + ':' + str(self.row))
        return self.content

    def __set__(self, obj, val):
        if _TESTING:
            print('Updating ' + str(self.header) + ':' + str(self.row))
        self.content = val

    def __eq__(self, other):
        if isinstance(other, str):
            return self.content == other
        elif isinstance(other, Cell):
            result = True
            if other.content != self.content:
                return False
            if other.header != self.header:
                return False
            if other.id != self.id:
                return False
            return True
        else:
            return False

    def __ne__(self, other):
        if isinstance(other, str):
            return other != self.content
        elif isinstance(other, Cell):
            if other.content != self.content:
                return True
            if other.header != self.header:
                return True
            if other.id != self.id:
                return True
            return False
        else:
            return True

    def __list_values(self):
        return [item for sublist in list(self.values()) for item in sublist]

    def store(self):
        if self.id is not None and self.header is not None:
            return {self.id: {
                        'tf': self.__tf,
                        'tokens': self.__tokens,
                        'content': self.content,
                        'header': self.header,
                        'id': self.id,
                        'next': self.__next
                    }}

    def __del__(self):
        Cell.cell_total -= 1


class Row:
    total_rows = 0

    def __init__(self, headers=None, cells=None, length=10):
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


def _evaluate(items: list):
    if '' in items and len(items) > 1:
        raise AssertionError('An AND or an OR must be followed by another variable')
    elif '' not in items:
        pass
    # TODO: find a cell or row associated with each string variable
    # TODO: then apply a logical operation to it


def _splitting(string: str):
    or_pos = None
    and_pos = None
    if 'OR' in string:
        or_pos = string.find('OR')
    if 'AND' in string:
        and_pos = string.find('AND')
    if 'NOT' in string:
        not_pos = string.find('NOT')
        return ['NOT', string[not_pos + 3:].strip()]
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
    insight = 'The cause of the headaches might be from the medication, Zofran, ' + \
              'which suppresses nausea and vomiting. The body may need to adjust to the ' + \
              'medications given to the new patient. The FDA has also approved Rolapitant to ' +\
              'prevent chemotherapy-induced nausea and vomiting. Imitrex worked well for ' + \
              'the patient to alleviate the headaches.'
    topic = 'The patient is experiencing nausea associated with severe headaches and is' + \
            ' asking for solutions for these'

    c = Cell(insight, 'insights', 0)
    print(c)
    s = c
    print(c.getTokens())
    print(c.getTF())

    d = Cell(topic, 'topic', 0)
    print(d.getTokens())
    print(d.getTF())

    e = Cell('helloword', 'something', 0)
    print(e.getTokens())
    print(e.getTF())


if __name__ == '__main__':
    test()
