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
_header_needing_tokenized = ['insights', 'category', 'topic']
_header_w_logic = ['intervention', 'side_effects']



class Logic:
    def __init__(self, string):
        self.__string = string
        self.__split(string)
        self.root = None

    def __is_oper(self, string: str):
        return string in '()[]*/+-'

    def __internal(self, string: str, count):
        string = string.lower()
        if '(' in string:
            start = string.find('(') + 1

            end = string.rfind(')') if ')' in string else len(string)
            return string[start:end]
        elif '[' in string:
            start = string.find(']') + 1
            end = string.rfind(']') if ']' in string else len(string)
            return string[start:end]
        else:
            return None

    def __split(self, string: str):
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
                    return [string[:left].strip()] + ['AND'] + self.__split(string[left + 3:].strip())
                else:
                    left = or_pos
                    return [string[:left].strip()] + ['OR'] + self.__split(string[left + 2:].strip())
            else:
                left = or_pos
                return [string[:left].strip()] + ['OR'] + self.__split(string[left + 2:].strip())
        else:
            if and_pos is not None:
                left = and_pos
                return [string[:left].strip()] + ['AND'] + self.__split(string[left + 3:].strip())
            else:
                raise NotImplementedError('You are not suppose to enter this whatsoever')


    """
    def inOrder(self, v):
        if isInternal(v): # if is another node /if right and left are not values
            self.inOrder(v.left) [logic goes here] self.inOrder(v.right)
    """

class Cell(object):
    """A data descriptor that sets and returns values
       normally and prints a message logging their access.
    """

    def __init__(self, cell=None, header_name=None, row_number=None, tokenize=False, logic=False):
        self.val = cell
        self.header = header_name
        self.row = row_number
        self.__tokenized = tokenize
        self.__tokens = None
        self.__tf = None
        self.__next = None
        self.__prev = None
        if tokenize and cell is not None and isinstance(cell, str):
            self.__tokenize(cell)
        if logic and cell is not None and isinstance(cell, str):
            self.__logic(cell)

    def __tokenize(self, cell):
        _TOKENIZER.open(cell)
        self.__tf = _TOKENIZER.tf
        self.__tokens = list(self.__tf.keys())

    def __logic(self, cell):
        if _TESTING:
            print('\033[94m' + 'Still need to finish Cell::__logic() function.' + '\033[0m')
            # need an inorder traversal

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
            cells = []
            for cont, head in zip(headers, cells):
                if head in _header_needing_tokenized:
                    cells.append(Cell(cont, head, self.__pos, tokenize=True))
                cells.append(Cell(cont, head, self.__pos))
        assert(len(headers) == len(cells))
        self.__row = dict(zip(headers, cells))
        self.__length == len(self.__row)

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

    def __getitem__(self, item):
        return self.__row[item]

    def __str__(self):
        keys = list(self.__row.keys())
        table = PrettyTable(keys)
        for head in keys:
            table.align[head] = 'c'
        table.add_row(self.__row.values())
        return str(table)

    def __tokenize(self):
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



def passing():
    pass


def evaluate(items: list):
    if '' in items:
        raise AssertionError('An AND or an OR must be followed by another variable')
    # TODO: find a cell or row associated with each string variable
    # TODO: then apply a logical operation to it


def splitting(string: str):
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
                return [string[:left].strip()] + ['AND'] + splitting(string[left + 3:].strip())
            else:
                left = or_pos
                return [string[:left].strip()] + ['OR'] + splitting(string[left + 2:].strip())
        else:
            left = or_pos
            return [string[:left].strip()] + ['OR'] + splitting(string[left + 2:].strip())
    else:
        if and_pos is not None:
            left = and_pos
            return [string[:left].strip()] + ['AND'] + splitting(string[left + 3:].strip())
        else:
            raise NotImplementedError('You are not suppose to enter this whatsoever')


def main():
    pass


if __name__ == '__main__':
    exp = 'OR with more thingsOR am working hereAND something ORsomeAND where AND some OR something else AND'
    print(splitting(exp))
