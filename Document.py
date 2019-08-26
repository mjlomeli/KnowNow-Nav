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
    """A data descriptor that sets and returns values
       normally and prints a message logging their access.
    """

    def __init__(self, cell=None, header_name=None, row_number=None, logic=False):
        self.val = cell
        self.header = header_name
        self.id = row_number
        self.__tokens = None
        self.__tf = None
        self.__next = None
        self.__prev = None
        if header_name in _needing_lemma and cell is not None and isinstance(cell, str):
            self.__tokenize(cell)
        if header_name in _header_w_logic and cell is not None and isinstance(cell, str):
            self.__logic(cell)

    def __tokenize(self, cell):
        _TOKENIZER.open(cell)
        self.__tf = _TOKENIZER.tf
        self.__tokens = list(self.__tf.keys())

    def getTokens(self):
        return self.__tokens

    def getTF(self):
        return self.__tf

    def setNext(self, next):
        self.__next = next
        #TODO: add Jennifer and Anne's code here

    def setPrev(self, prev):
        self.__prev = prev
        #TODO: add Jennifer and Anne's code here

    def getNext(self):
        return self.__next
        #TODO: add Jennifer and Anne's code here

    def getPrev(self):
        return self.__prev
        #TODO: add Jennifer and Anne's code here

    def __add__(self, other):
        if isinstance(other, str):
            return self.val + other
        elif isinstance(other, Cell):
            return str(self) + str(other)
        #Todo: add Jennifer and Anne's code here
        #Todo: to be able to link one node to another

    def __logic(self, string):
        operation = _splitting(string)
        _evaluate(operation)
        #Todo: make additional nodes to point to intervention mitigating side effect

    def __eq__(self, other):
        return self.val == other

    def __ne__(self, other):
        return self.val != other

    def __contains__(self, item):
        return item in self.val

    def __str__(self):
        trunc = self.header[:10]
        next = self.__next if self.__next is not None else 'None'
        result = '(' + trunc + ')-->' + next
        return result

    def __get__(self, obj, objtype):
        if _TESTING:
            print('Retrieving ' + str(self.header) + ':' + str(self.row))
        return self.val

    def __set__(self, obj, val):
        if _TESTING:
            print('Updating ' + str(self.header) + ':' + str(self.row))
        self.val = val


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

    def __tokenize(self):
        # TODO: here we will combine similarities among documents
        self.__tokenized = True
        self.__cell_cf = {}
        for cell in self.__row.values():
            if cell is not None:
                pass

        _TOKENIZER.open(self.val)
        self.__tf = _TOKENIZER.tf

    def __and__(self, other):
        if self.__tokenized is None:
            self.__tokenize()
        return False

    def __or__(self, other):
        if self.__tokenized is None:
            self.__tokenize()
        return False

    def __xor__(self, other):
        if self.__tokenized is None:
            self.__tokenize()
        return False

    def __eq__(self, other):
        if self.__tokenized is None:
            self.__tokenize()
        return False

    def __ne__(self, other):
        if self.__tokenized is None:
            self.__tokenize()
        return False

    def __gt__(self, other):
        if self.__tokenized is None:
            self.__tokenize()
        return False

    def __lt__(self, other):
        if self.__tokenized is None:
            self.__tokenize()
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
