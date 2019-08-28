# !/usr/bin/env python

"""Writing

If the description is long, the first line should be a short summary of Writing.py
that makes sense on its own, separated from the rest by a newline.
"""

from pathlib import Path
from Cell import Cell
from Tokenizer import Tokenizer

PATH = Path.cwd()

__author__ = "Mauricio Lomeli"
__date__ = "8/27/2019"
__copyright__ = "Copyright 2019, KnowNow-Nav"
__license__ = "0.0.0.1"
__maintainer__ = "Mauricio Lomeli"
__email__ = "mjlomeli@uci.edu"
__status__ = "Prototype"


_TOKENIZER = Tokenizer()
_NEED_LEMMA = ['insights', 'topic', 'query', 'profile', ]


class Writing(Cell):
    def __init__(self, text=None, title=None, id=None):
        super().__init__(self, text, title, id)
        self.header = title
        self.content = text
        self.__tokens = None
        self.__tf = None
        self.count = 0
        self.length = None
        self.__assemble()

    def __assemble(self):
        # Tokenizes the cell if it is in a certain column
        try:
            if self.header in _NEED_LEMMA:
                if self.content is not None:
                    if isinstance(self.content, str):
                        self.__tokenize(self.content)
            self.length = len(self.content)
            self.count = len(self.content.split(' '))
        except Exception as e:
            print(e)

    def __tokenize(self, text):
        """
        Cleans a cell's text and brings it to the root meaning.
        Then stores the result in the member variables.
        :param content: the cell's text
        """
        _TOKENIZER.open(text)
        self.__tf = _TOKENIZER.tf
        self.__tokens = list(self.__tf.keys())

    def getTokens(self):
        """
        Gets the cleaned text from the cell.
        :return: text
        """
        if self.__tokens is None:
            self.__tokenize(self.content)
        return self.__tokens

    def getTF(self):
        """
        Gets a dictionary of every word in the cell
        and their count.
        :return: dictionary: Term Frequency
        """
        if self.__tf is None:
            self.__tokenize(self.content)
        return self.__tf

    def __add__(self, other):
        """
        Concatenates a string and a cell's text
        :param other: the other param
        :return: string concatenation
        """
        if self.__tf is None:
            self.__tokenize(self.content)

        header = ''

        if isinstance(other, str):
            content = '' if other is None else other
        elif isinstance(other, Cell) or isinstance(other, Writing):
            content = '' if other.content is None else other.content
            header = '' if other.header is None else other.content
        else:
            raise TypeError('Can only add TF among Writing, Cell, and str.')

        return Writing(self.content + content, self.header + header)

    def __iadd__(self, other):
        if self.__tf is None:
            self.__tokenize(self.content)

        if isinstance(other, str):
            self.content = '' if other is None else other
        elif isinstance(other, Cell) or isinstance(other, Writing):
            self.content = '' if other.content is None else other.content
            self.header = '' if other.header is None else other.content
        else:
            raise TypeError('Can only add TF among Writing, Cell, and str.')

    def __str__(self):
        """
        prints the node relationships.
        :return: string
        """
        result = ''
        if self.header is not None:
            result = '\033[1m\033[92m' + 'Title: {}'.format(self.header) + '\033[0m\n'
            result += '\033[1m\033[92m' + 'Text: {}'.format(self.content) + '\033[0m\n'
        return result

    def print_relationships(self):
        print(super())

    def __gt__(self, other):
        if self.__tf is None and self.content is not None:
            self.__tokenize(self.content)
        tf = {} if other.getTF() is None else other.getTF()
        if isinstance(other, Writing):
            pass

        return _merge_indexes(self.__tf, other.getTF())


    def __and__(self, other):
        if isinstance(other, Writing):
            tf = self.__add_tf(other)
            #cosine(0, 1)

    def __or__(self, other):
        pass

    def __xor__(self, other):
        pass

    def __lt__(self, other):
        pass

    def __le__(self, other):
        pass

    def __ge__(self, other):
        pass

    def __mod__(self, other):
        pass

    def __imod__(self, other):
        pass


def _increment_index(index, val):
    i = {}
    for key, values in index.items():
        for key1, val2 in values.items():
            if key not in i:
                i[key] = {key1 + val: val2}
            else:
                i[key][key1 + val] = val2
    return i


def _reconstruct_index(new_start, index, keys):
    new_index = {}
    length = 0
    if len(index) > 0:
        k = list(index.values())[0]
        if k is not None:
            length = len(k)
    if length > 0:
        for key in keys:
            if key in index:
                for i, value in enumerate(index[key].values()):
                    if key not in new_index:
                        new_index[key] = {new_start + i: value}
                    else:
                        new_index[key][new_start + i] = value
            else:
                for i in range(length):
                    if key not in new_index:
                        new_index[key] = {new_start + i: 0}
                    else:
                        new_index[key][new_start + i] = 0
    else:
        return {key: {i: 0} for i, key in enumerate(keys)}
    return new_index


def _convert_index(tf):
    if tf is None or len(tf) == 0:
        return {}
    if len(tf.values()) > 1 and isinstance(list(tf.values())[0], dict):
        return tf
    else:
        return {key: {0: value} for key, value in tf.items()}


def _merge_indexes(index1, index2):
    index1 = _convert_index(index1)
    index2 = _convert_index(index2)
    start = min(list(index1.values())[0]) if len(index1) > 0 else 0
    end = max(list(index1.values())[0]) + 1 if len(index1) > 0 else 0
    if index1.keys() != index2.keys() or end == 0 and len(index2) == 0:
        keys = set(index1.keys()).union(index2.keys())
        index1 = _reconstruct_index(start, index1, keys)
        index2 = _reconstruct_index(end, index2, keys)
    for key in index1.keys():
        index1[key].update(index2[key])
    return index1


def testWriting():
    pass