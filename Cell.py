# !/usr/bin/env python

"""Cell

If the description is long, the first line should be a short summary of Cell.py
that makes sense on its own, separated from the rest by a newline.
"""

from Neo4jDriver import *
from getpass import getpass
from TestCases import TestCase
from Spreadsheet import Spreadsheet

PATH = Path.cwd()

__author__ = "Mauricio Lomeli"
__date__ = "8/17/2019"
__license__ = "MIT"
__version__ = "0.0.0.1"
__maintainer__ = "Mauricio Lomeli"
__email__ = "mjlomeli@uci.edu"
__status__ = "Prototype"

_TESTING = False
_RUN_NEO4J = True
_STRING_LIMIT = 15
_PICKLE = Path().cwd() / Path('data') / Path('index.pickle')


_NORM_NODE_HEAD = {'id': 'ID', 'topic': 'Topic', 'date': 'Date', 'query_tag': 'Query Tag', 'query': 'Query',
                'profile': 'Profile', 'cohort': 'Cohort', 'tumor': 'T', 'tumor_count': 'T Count', 'node': 'N',
                'metastasis': 'M', 'grade': 'Grade', 'recurrence': 'Recurr', 'category': 'Category',
                'intervention': 'Intervention', 'side_effects': 'Side Effect', 'int_side_effects': 'Int. Side Eff.',
                'insights': 'Insights', 'volunteers': 'Volunt.', 'url': 'URL', 'HER2': 'HER2', 'HER': 'HER',
                'BRCA': 'BRCA', 'ER': 'ER', 'HR': 'HR', 'PR': 'PR', 'RP': 'RP', 'RO': 'RO'}

_LOCAL_HOST = 'bolt://localhost:7687'


class Cell(object):
    """
    Holds each individual data. Has higher level of control. Each cell makes up a node.
    """
    __cell_total = 0
    __cell_global = []
    __ids = []
    __session = None
    # __neo4j_running = True

    def __init__(self, session, content="_", header_name="_"):
        self.content = content
        self.header = header_name
        self.id = Cell.__cell_total
        self.__next = {}
        self.__index = 0
        self.__assemble()
        self.__relation = None
        self.__session = session

        if (str(self.header)) == "":
            self.header = "empty"
        if (str(self.id) == ""):
            self.id = "00"
        if (str(self.content) == ""):
            self.content = "no content"

        insertNode(self.__session, "label filler" , "prop filler", str(self.content))


    def __assemble(self):
        """
        Executes the necessary functions for the cell to exist.
        """
        # Keeps track that all ids are unique, else auto-generate

        # Opens the database
        # if Cell.__cell_total == 0 and _RUN_NEO4J:
        
        # print(Cell.__session)
        # print(database)
        Cell.__neo4j_running = True
        # Adds the node in the database if it is running
        # if Cell.__neo4j_running:
        # try:
        #     # TODO: Check with Anne and Jennifer that this works
        # except ConnectionRefusedError:
        #     TestCase('_RUN_NEO4J', _RUN_NEO4J)
        # Static variable holding the count of all existing cells

        self.id = Cell.__cell_total
        Cell.__ids.append(self.id)
        Cell.__cell_total += 1


    def __openDB(self):
        """
        Opens the database. It will prompt you for your
        username and password. As well as the URI to
        establis hteh connection.
        :return: session
        """
        username = input('Enter your username: ')
        password = getpass('Enter your password: ')
        try:
            # TODO: Check with Jennifer and Anne if the database opens well enough.
            return openDatabase(_LOCAL_HOST, username, password)
        except Exception as e:
            TestCase('openDatabase', _LOCAL_HOST, username, password)

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
                self.insert_N4j(link_name, next_cell)
        else:
            raise TypeError('Can only set next to a Cell or list of Cells')

    def insert_N4j(self, link_name, next_cell):
        # if Cell.__neo4j_running:
        link = '' if link_name is None else link_name
        try:

            if (str(self.header)) == "":
                self.header = "empty"
            if (str(self.id) == ""):
                self.id = "00"
            if (str(self.content) == ""):
                self.content = "no content"

            if (str(next_cell.header)) == "":
                next_cell.header = "empty"
            if (str(next_cell.id) == ""):
                next_cell.id = "00"
            if (str(next_cell.content) == ""):
                next_cell.content = "no content"

            # TODO: Check with Jennifer and Anne if our code checks out
            self.__relation = link_name
            # insertNode(self.__session, str(self.header), str(self.id), str(self.content))
            insertNode(self.__session, "label filler", "prop filler", str(self.content))

            # createNewRelation(self.__session,  str(self.header), str(self.id),str(self.content),
            #                    str(next_cell.header),str(next_cell.id), str(next_cell.content),
            #                   str(link_name), str(self.id), str(link_name))

            createNewRelation(self.__session,  "label filler", "prop filler",str(self.content),
                               "label filler" ,"prop filler", str(next_cell.content),
                              str(link_name), "rel prop filler", str(link_name))
        except Exception as e:
            print(e)
            TestCase('createNewRelation', str(self.id), self.content, next_cell.id, next_cell.content,
                     link, link)

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

    def find_link(self, id):
        values = list(self.__next.values())
        if id in values:
            return values[values.index(id)]

    def __del__(self):
        """
        De-allocates variables and storage values.
        :return:
        """
        Cell.__cell_total -= 1
        Cell.__ids.remove(self.id)
        # if Cell.__cell_total == 0:
        #     if Cell.__neo4j_running:
        # try:
            # TODO: Check with Jennifer and Anne about closing the DB
            
        # except Exception as e:
        #     print(e)
        #     TestCase('closeDatabase', Cell.__session, Cell.__cell_total)

            # Cell.__neo4j_running = False
        # else:
            # if Cell.__neo4j_running:
        try:
            # TODO: Check with Jennifer and Anne about removing a Node
            if (str(self.header)) == "":
                self.header = "empty"
            if (str(self.id) == ""):
                self.id = "00"
            if (str(self.content) == ""):
                self.content = "no content"

            deleteRelation(self.__session, "label filler", "prop filler", str(self.content),
                           str(self.__relation))
            removeNode(self.__session, "label filler", "prop filler", str(self.content))
        except Exception as e:
            print(e)
            TestCase('removeNode', self.__session, self.id, self.content, self.content)


def main():
    database = openDatabase(_LOCAL_HOST, "neo4j", "testing")
    session = database[0]

    # a = Cell(session, 'July 2015', 'Date')
    # b = Cell(session, 'Treatment', 'Query Tag')
    # c = Cell(session, 'Patient Query',
    #          r'Patient had to get her implants removed after her breast expanders got infected. Now she is on zoladex and tamoxifen and is worried about the swelling and pain in her feet.')
    # d = Cell(session, 'Category Tag', 'Side Effects')
    # e = Cell(session, 'Intervention', 'Tamoxifen')
    # f = Cell(session, 'Associated Side effect', 'Joint pain OR swelling OR pain in feet')
    # g = Cell(session, 'Intervention mitigating side effect', None)
    # h = Cell(session, 'Intervention', 'Taxmoxifen')

    insertNode(session, "employee", "name", "person1")
    insertNode(session, "employee", "name", "person2")
    createNewRelation(session, "employee", "name", "person1", "employee", "name", "person2", "Related", "how", "by law" )
    # createNewRelation(self.__session,  str(self.id), str(self.header),str(self.content),
    #                            str(next_cell.id),str(next_cell.header), str(next_cell.content),
    #                           str(link_name), str(self.id), str(link_name))

    # e.setNext(a)
    # a.setNext(b, "connecting")
    # b.setNext(c, "linking")


    # d.setNext(f, 'does verb')
    # f.setNext(g, 'got linked')
    # f.setNext(d, 'goes around')

    closeDatabase(session)




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
