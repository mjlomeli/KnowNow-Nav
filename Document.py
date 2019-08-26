# !/usr/bin/env python

"""Document

If the description is long, the first line should be a short summary of Document.py
that makes sense on its own, separated from the rest by a newline.
"""

from prettytable import PrettyTable
from collections import namedtuple
from Tokenizer import Tokenizer
from Similarity import cosine_score

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
_TOKENIZER = Tokenizer()
_needing_lemma = ['insights', 'topic']
_linking_headers = {
    'intervention': ('causes', 'side_effects'),
    'intervention': ('against', 'cohort'),
    'side_effects': ('could be mitigated by', 'int_side_effects')
    # 'side_effects': ('lasted for', 'duration'),
    # 'side_effects': ('occurred after intervention', 'duration')
}
_header_w_logic = ['intervention', 'side_effects', 'int_side_effects']
_NORM_HEADERS = {'id': 'id', 'Topic': 'topic', 'Date Discussion (Month/Year)': 'date', 'Query Tag': 'query_tag',
                'Patient Query/inquiry': 'query', 'Specific Patient Profile': 'profile',
                'Patient Cohort (Definition)': 'cohort', 'Tumor (T)': 'tumor', 'Tumor Count': 'tumor_count',
                'Node (N)': 'node', 'Metastasis (M)': 'metastasis', 'Grade': 'grade', 'Recurrence': 'recurrence',
                'Category Tag': 'category', 'Intervention': 'intervention', 'Associated Side effect': 'side_effects',
                'Intervention mitigating side effect': 'int_side_effects', 'Patient Insight': 'insights',
                'Volunteers': 'volunteers', 'Discussion URL': 'url', 'HER2': 'HER2', 'HER': 'HER', 'BRCA': 'BRCA',
                'ER': 'ER', 'HR': 'HR', 'PR': 'PR', 'RP': 'RP', 'RO': 'RO'}


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
        self.__prev = {}
        self.__index = 0
        if header_name in _needing_lemma and content is not None and isinstance(content, str):
            self.__tokenize(content)
        if header_name in _header_w_logic and content is not None and isinstance(content, str):
            self.__logic(content)

    def __print(self):
        trunc = self.header[:10]
        next_cell = self.__next
        if next_cell is None or len(next_cell) == 0:
            return '(' + trunc + ')-->None\n'
        else:
            result = ''
            next_cell = self.__list_values()
            for cell in next_cell:
                result += '(' + trunc + ')-->'
                if cell not in Cell.cell_global:
                    Cell.cell_global.append(cell)
                    result += cell.__print()
                else:
                    result = result + '(' + cell.header + ')' + '\n'
            return result

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

    def setNext(self, next_cell):
        if isinstance(next_cell, Cell):
            if next_cell is not None:
                if next_cell.header not in self.__next:
                    self.__next[next_cell.header] = [next_cell]
                else:
                    self.__next[next_cell.header].append(next_cell)
                next_cell.__prev = self
        elif isinstance(next_cell, tuple):
            if None not in next_cell and len(next_cell) > 1:
                if next_cell[0] not in self.__next:
                    self.__next[next_cell[0]] = [next_cell[1]]
                else:
                    self.__next[next_cell[0]].append(next_cell[1])
                next_cell[1].__prev = self
        #TODO: add Jennifer and Anne's code here

    def getNext(self):
        return self.__list_values()
        #TODO: add Jennifer and Anne's code here

    def getPrev(self):
        return self.__prev
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

    def __logic(self, string):
        operation = _splitting(string)
        _evaluate(operation)
        #Todo: make additional nodes to point to intervention mitigating side effect

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
            if other.val != self.content:
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
            if other.val != self.content:
                return True
            if other.header != self.header:
                return True
            if other.id != self.id:
                return True
            return False
        else:
            return True

    def __list_values(self):
        return [item for sublist in list(self.contentues()) for item in sublist]

    def __del__(self):
        Cell.cell_total -= 1


class Row:
    def __init__(self, headers=None, cells=None, length=10):
        __total_rows = 0
        self.__row = {}
        self.__length = length
        self.__pos = Row.__total_rows + 1
        Row.__total_rows += 1
        self.__tf = None
        self.__index = 0
        self.__assemble(headers, cells, length)

    def __assemble(self, headers=None, cells=None, length=10):
        if headers is None:
            headers = [i for i in range(length)]
        if cells is None:
            cells = [Cell(None, None, None)] * length
        else:
            cells = [Cell(txt, head, self.__pos) for txt, head in zip(headers, cells)]
        assert(len(headers) == len(cells))
        self.__row = dict(zip(headers, cells))
        self.__length == len(self.__row)
        self.__set_associations()

    def __set_associations(self):
        for node, link in _linking_headers:
            if node in self.__row and link in self.__row:
                self.__row[node].setNext(self.__row[link])
                #Todo: Test if the plus sign works here too
                # self.__row[node] + self.__row[link]

    def __iter__(self):
        self.__index = 0
        return self

    def __next__(self):
        if self.__index > len(self):
            raise StopIteration
        temp = self.__cells[self.__index]
        self.__index += 1
        return temp

    def __len__(self):
        self.__length

    def __contains__(self, item):
        return item in self.__row.values()

    def __getitem__(self, item):
        return self.__row[item]

    def keys(self):
        return self.__row.keys()

    def __str__(self):
        keys = list(self.__row.keys())
        table = PrettyTable(keys)
        for head in keys:
            table.align[head] = 'c'
        table.add_row(self.__row.values())
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

    def __del__(self):
        Row.__total_rows -= 1


def _evaluate(items: list):
    if '' in items:
        raise AssertionError('An AND or an OR must be followed by another variable')
    # TODO: find a cell or row associated with each string variable
    # TODO: then apply a logical operation to it


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
