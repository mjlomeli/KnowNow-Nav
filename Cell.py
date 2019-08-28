# !/usr/bin/env python

"""Cell

If the description is long, the first line should be a short summary of Cell.py
that makes sense on its own, separated from the rest by a newline.
"""

from neo4j import GraphDatabase, basic_auth
from TestCases import TestCase
from pathlib import Path


__author__ = "Mauricio Lomeli"
__date__ = "8/17/2019"
__license__ = "MIT"
__version__ = "0.0.0.1"
__maintainer__ = "Mauricio Lomeli"
__email__ = "mjlomeli@uci.edu"
__status__ = "Prototype"

_TESTING = True
_RUNNING_NEO4J = False
_STRING_LIMIT = 15
_ROW_LENGTH = 28
_PICKLE = Path().cwd() / Path('data') / Path('index.pickle')
_DRIVER = GraphDatabase.driver('bolt://localhost:7687', auth=basic_auth('neo4j', 'knownow'))
_SESSION = _DRIVER.session()

_NORM_NODE_HEAD = {'id': 'ID', 'topic': 'Topic', 'date': 'Date', 'query_tag': 'Query Tag', 'query': 'Query',
                'profile': 'Profile', 'cohort': 'Cohort', 'tumor': 'T', 'tumor_count': 'T Count', 'node': 'N',
                'metastasis': 'M', 'grade': 'Grade', 'recurrence': 'Recurr', 'category': 'Category',
                'intervention': 'Intervention', 'side_effects': 'Side Effect', 'int_side_effects': 'Int. Side Eff.',
                'insights': 'Insights', 'volunteers': 'Volunt.', 'url': 'URL', 'HER2': 'HER2', 'HER': 'HER',
                'BRCA': 'BRCA', 'ER': 'ER', 'HR': 'HR', 'PR': 'PR', 'RP': 'RP', 'RO': 'RO'}


class Cell(object):
    """
    Holds each individual data. Has higher level of control. Each cell makes up a node.
    """
    __cell_total = 0

    def __init__(self, content=None, header_name=None, id=None):
        Cell.__cell_total += 1
        self.content = content
        self.header = header_name
        self.id = id
        self.__next = {}
        self.__index = 0

    def setNext(self, next_cell, link_name=None):
        """
        Linked list behavior. Sets the linkage to the next node.
        :param next_cell: the next cell
        :param link_name: the name of the link
        """
        if isinstance(next_cell, Cell):
            if link_name not in self.__next:
                self.__next[link_name] = [next_cell]
                self.insert_N4j(link_name, next_cell)
            else:
                if link_name in self.__next and next_cell not in self.__next[link_name]:
                    self.__next[link_name].append(next_cell)
                    self.insert_N4j(link_name, next_cell)
        elif isinstance(next_cell, list):
            for item in next_cell:
                self.setNext(item, link_name)
                self.insert_N4j(self, link_name, next_cell)
        else:
            raise TypeError('Can only set next to a Cell or list of Cells')

    def insert_N4j(self, link_name, next_cell):
        if _RUNNING_NEO4J:
            link = 'EMPTY_STRING' if link_name is None else link_name
            content = 'EMPTY_STRING' if next_cell.content is None else next_cell.content
            query = "CREATE ({})-[:{}]->({})".format(self.content.replace(' ', '_'),
                                                     link.replace(' ', '_'), next_cell.content.replace(' ', '_'))

    def hasNext(self, cell):
        return cell in self.__list_values()

    def getNext(self):
        """
        A cell can point to multiple cells. The next may be
        multiple cells.
        :return: list of cells
        """
        return self.__list_values()

    def getLast(self):
        """
        Returns the end of every path if it exists.
        :return: a list of all cells the have a None as their next
        """
        if self.__next is None or len(self.__next) == 0:
            return [self]
        else:
            Cell.__cell_global = []
            temp = self.__getLastHelper(self.__list_values())
            Cell.__cell_global = []
            return temp

    def __getLastHelper(self, current):
        """
        Helper function for getLast() function.
        :param current: the current node
        :return: List of ended nodes.
        """
        if current is None or len(current) == 0:
            return []
        else:
            result = []
            for cell in current:
                if cell not in Cell.__cell_global:
                    Cell.__cell_global.append(cell)
                    if len(cell.getNext()) == 0:
                        result += [self]
                    else:
                        result += self.__getLastHelper(cell)
            return result

    def __add__(self, other):
        """
        Concatenates a string and a cell's text
        :param other: the other param
        :return: string concatenation
        """
        header = ''
        if isinstance(other, str):
            content = '' if other is None else other
        elif isinstance(other, Cell):
            content = '' if other.content is None else other.content
            header = '' if other.header is None else other.header
        else:
            raise TypeError('Can only add TF among Writing, Cell, and str.')

        return Cell(self.content + content, self.header + header)

    def __contains__(self, item):
        """
        Checks to see if a string is in the content of a cell
        or checks if the cells are the same.
        :param item: the item getting compared
        :return: boolean
        """
        if isinstance(item, str):
            return item in self.content
        elif isinstance(item, Cell):
            return self == item or self.id == item.id

    def __str__(self):
        """
        prints the node relationships.
        :return: string
        """
        result = ''
        for link, cells in self.__next.items():
            for next_cell in cells:
                link = '' if link is None else link
                result += '\033[95m(' + str(self.content)[:_STRING_LIMIT] + ')\033[0m'
                result += '\033[93m-' + link + '->\033[0m'
                result += '\033[95m(' + str(next_cell.content)[:_STRING_LIMIT] + ')\033[0m'
                result += '\n'
        return result

    def keys(self):
        """
        Gets the headers of what the current cell points to.
        :return: list of headers
        """
        return self.__next.keys()

    def values(self):
        """
        Gets all the cells the current cell points to as a list
        :return: list of cells
        """
        return self.__list_values()

    def __iter__(self):
        """
        Begins the iteration
        :return: self
        """
        self.__index = 0
        return self

    def __next__(self):
        """
        Gets the next iteration index
        :return: the next item
        """
        if self.__index >= len(self):
            raise StopIteration
        temp = list(self.__list_values())[self.__index]
        self.__index += 1
        return temp

    def __len__(self):
        """
        Returns the length of the links, including the current cell.
        Like a linked list length.
        :return: int
        """
        return len(self.__list_values()) + 1

    def __getitem__(self, item):
        """
        Gets an item in the cell that matches the item
        :param item: int, str, or Cell
        :return: the matching pair
        """
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
        """
        Sets the current cell's next to value. If the
        cell already exists, then it overrides it.
        :param key: the header
        :param value: the cell
        """
        self.setNext(value, key)

    def __get__(self, obj, objtype):
        if _TESTING:
            test_msg = '\033[94m' + 'Retrieving: ' + self.content
            test_msg += ' from Cell({}{}{})'.format(self.content, self.header, self.id) + '\033[0m'
            print(test_msg)
        return self.content

    def __set__(self, obj, val):
        if _TESTING:
            test_msg = '\033[94m' + 'Updating: {}'.format(self.id)
            test_msg += ' from Cell({}{}{})'.format(self.content, self.header, self.id) + '\033[0m'
            print(test_msg)
        self.content = val

    def __eq__(self, other):
        if isinstance(other, str):
            return self.content == other or self.header == other or str(self.id) == other
        elif isinstance(other, Cell):
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
        if self.__next is not None:
            return [item for sublist in self.__next.values() for item in sublist]
        else:
            return []

    def __del__(self):
        """
        De-allocates variables and storage values.
        :return:
        """
        Cell.__cell_total -= 1
        if Cell.__cell_total < 1 and _RUNNING_NEO4J:
            _SESSION.close()
        else:
            if _RUNNING_NEO4J:
                query = "MATCH (n:{} {{}: {}})".format(self.header.replace('', "EMPTY STRING"),
                                                       self.content.replace('', "EMPTY STRING"))
                _SESSION.run(query)


def main():
    pass


def TestCell():
    header = ['calpurnia', 'sunny', 'egypt', 'capital']
    content = ['something', 'goes', 'in', 'here']

    # test auto id
    for head, cont in zip(header, content):
        temp = Cell(head, cont)
        print(temp.id)

    # test add
    a = Cell("hello", "where")
    b = Cell("there", "is")
    c = a + b
    print('c.content: ' + c.content)
    print('c.header: ' + c.header)

    # test linking
    c.setNext(a)
    a.setNext(b)
    print(c.values())
    d = c.getNext()
    for item in d:
        print(item.id)
        print(item.content)
        print(item.header)

    # test tokenizer
    tokens = a.getTokens()
    tf = b.getTF()

    # keys
    print(c.keys())

    # logical
    print(a == b)
    print(c == (a + b))
    print(a != b)

    c['new_link'] = Cell('new link')
    for item in c['new_link']:
        print(item.content)


if __name__ == '__main__':
    main()
