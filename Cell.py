# !/usr/bin/env python

"""Cell

If the description is long, the first line should be a short summary of Cell.py
that makes sense on its own, separated from the rest by a newline.
"""

from Tokenizer import Tokenizer
from Neo4jDriver import *
from getpass import getpass
from TestCases import TestCase

PATH = Path.cwd()

__author__ = "Mauricio Lomeli"
__date__ = "8/17/2019"
__license__ = "MIT"
__version__ = "0.0.0.1"
__maintainer__ = "Mauricio Lomeli"
__email__ = "mjlomeli@uci.edu"
__status__ = "Prototype"

_TESTING = True
_RUN_NEO4J = False
_STRING_LIMIT = 15
_PICKLE = Path().cwd() / Path('data') / Path('index.pickle')


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
    __cell_global = []
    __ids = []
    __session = None
    __neo4j_running = False

    def __init__(self, content=None, header_name=None):
        self.content = content
        self.header = header_name
        self.id = Cell.__cell_total
        self.__next = {}
        self.__index = 0
        self.__assemble()

    def __assemble(self):
        """
        Executes the necessary functions for the cell to exist.
        """
        # Keeps track that all ids are unique, else auto-generates
        if self.id is None:
            self.id = Cell.__cell_total
            Cell.__ids.append(self.id)
        elif self.id in Cell.__ids:
            raise AssertionError('id must be unique. ' + str(self.id) + ' exists.')
        else:
            Cell.__ids.append(self.id)
        # Opens the database
        if Cell.__cell_total == 0 and _RUN_NEO4J:
            Cell.__session = self.__openDB()
            Cell.__neo4j_running = True
        # Adds the node in the database if it is running
        if Cell.__neo4j_running:
            try:
                insertNode(Cell.__session, self.id, self.header, self.content)
            except ConnectionRefusedError:
                TestCase('_RUN_NEO4J', _RUN_NEO4J)
        # Static variable holding the count of all existing cells
        Cell.__cell_total += 1

    def __openDB(self):
        """
        Opens the database. It will prompt you for your
        username and password. As well as the URI to
        establis hteh connection.
        :return: session
        """
        uri = input('Enter URI connection: ')
        username = input('Enter your username: ')
        password = getpass('Enter your password: ')
        try:
            return openDatabase(uri, username, password)
        except Exception as e:
            TestCase('openDatabase', uri, username, password)

    def setNext(self, next_cell, link_name=None):
        """
        Linked list behavior. Sets the linkage to the next node.
        :param next_cell: the next cell
        :param link_name: the name of the link
        """
        if isinstance(next_cell, Cell):
            if link_name not in self.__next:
                self.__next[link_name] = [next_cell]
            else:
                self.__next[link_name].append(next_cell)
            if Cell.__neo4j_running:
                link = '' if link_name is None else link_name
                try:
                    createNewRelation(
                        Cell.__session, self.id, self.content, next_cell.id, next_cell.content, link, link)
                except Exception as e:
                    print(e)
                    TestCase('createNewRelation', self.id, self.content, next_cell.id, next_cell.content,
                             link, link)

        elif isinstance(next_cell, list):
            for item in next_cell:
                self.setNext(item, link_name)
        else:
            raise TypeError('Can only set next to a Cell or list of Cells')

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
                result += '\033[95m(' + self.content[:_STRING_LIMIT] + ')\033[0m'
                result += '\033[93m-' + link + '->\033[0m'
                result += '\033[95m(' + next_cell.content[:_STRING_LIMIT] + ')\033[0m'
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
        Cell.__ids.remove(self.id)
        if Cell.__cell_total == 0:
            if Cell.__neo4j_running:
                try:
                    closeDatabase(Cell.__session)
                except Exception as e:
                    print(e)
                    TestCase('closeDatabase', Cell.__session, Cell.__cell_total)

                Cell.__neo4j_running = False
        else:
            if Cell.__neo4j_running:
                try:
                    removeNode(Cell.__session, self.id, self.content, self.content)
                except Exception as e:
                    print(e)
                    TestCase('removeNode', Cell.__session, self.id, self.content, self.content)


def main():
    pass


def test():
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
    test()
