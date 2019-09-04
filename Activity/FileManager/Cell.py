# !/usr/bin/env python

"""Cell

If the description is long, the first line should be a short summary of Cell.py
that makes sense on its own, separated from the rest by a newline.
"""

__author__ = "Mauricio Lomeli"
__date__ = "8/17/2019"
__license__ = "MIT"
__version__ = "0.0.0.1"
__maintainer__ = "Mauricio Lomeli"
__email__ = "mjlomeli@uci.edu"
__status__ = "Prototype"


class Cell(object):
    """
    Holds each individual data. Has higher level of control. Each cell makes up a node.
    """
    __cell_total = 0

    def __init__(self, content=None, header=None, id=None):
        Cell.__cell_total += 1
        self.content = None if content is None else str(content)
        self.header = None if header is None else str(header)
        self.id = None if id is None else id
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
                #self.insert_N4j(link_name, next_cell)
            else:
                if link_name in self.__next and next_cell not in self.__next[link_name]:
                    self.__next[link_name].append(next_cell)
                    #self.insert_N4j(link_name, next_cell)
        elif isinstance(next_cell, list):
            for item in next_cell:
                self.setNext(item, link_name)
                #self.insert_N4j(self, link_name, next_cell)
        else:
            raise TypeError('Can only set next to a Cell or list of Cells')

    def hasNext(self, cell=None):
        if cell is None:
            return len(self.__list_values()) > 0
        elif isinstance(cell, Cell):
            return cell in self.__list_values()
        elif isinstance(cell, dict):
            return all([val in self for val in cell.values()])
        elif isinstance(cell, list):
            return all([val in self for val in cell])

    def getNext(self):
        """
        A cell can point to multiple cells. The next may be
        multiple cells.
        :return: list of cells
        """
        return self.__list_values()

    def remove(self, cell):
        if isinstance(cell, Cell):
            if self.hasNext(cell):
                empties = []
                for key, value in self.__next.items():
                    if cell in value:
                        self.__next[key].remove(cell)
                        if len(self.__next[key]) == 0:
                            empties.append(key)
                for key in empties:
                    self.__next.pop(key)
        elif isinstance(cell, dict):
            if 'content' in cell and 'header' in cell and 'id' in cell:
                self.remove(Cell(cell['content'], cell['header'], cell['id']))
        elif isinstance(cell, list):
            if len(cell) == 3:
                return self.remove(Cell(cell[0], cell[1], cell[2]))

    def __contains__(self, item):
        """
        Checks to see if a string is in the content of a cell
        or checks if the cells are the same.
        :param item: the item getting compared
        :return: boolean
        """
        if isinstance(item, str):
            return item in self.content
        elif isinstance(item, dict):
            if item['content'] != self.content:
                return False
            if item['header'] != self.header:
                return False
            if item['id'] != self.id:
                return False
            return True
        elif isinstance(item, list):
            if self.content not in item:
                return False
            if self.header not in item:
                return False
            if self.id not in item:
                return False
            return True
        elif isinstance(item, Cell):
            return self.content == item.content and self.header == item.header and self.id == item.id

    def __str__(self):
        """
        prints the node relationships.
        :return: string
        """
        result = ''
        if len(self.__next) == 0:
            result += '\033[95m(' + str(self.content)[:10] + ')\033[0m'
        else:
            for link, cells in self.__next.items():
                for next_cell in cells:
                    link = '' if link is None else link
                    result += '\033[95m(' + str(self.content)[:10] + ')\033[0m'
                    result += '\033[93m-' + link + '->\033[0m'
                    result += '\033[95m(' + str(next_cell.content)[:10] + ')\033[0m'
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
        return self.content

    def __set__(self, obj, val):
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


def testCell():
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

    print('print(c)')
    print(c)
    print('print(a)')
    print(a)


if __name__ == '__main__':
    pass
