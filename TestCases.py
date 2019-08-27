# !/usr/bin/env python

"""Testcases

If the description is long, the first line should be a short summary of TestCases.py
that makes sense on its own, separated from the rest by a newline.
"""

from pathlib import Path
from Cell import testCell
from FlaskDriver import testFlaskDriver
from Tokenizer import testTokenizer
from Spreadsheet import testSpreadsheet
from Similarity import testSimilarity
from Row import testRow
from Document import testDocument

PATH = Path.cwd()

__author__ = "Mauricio Lomeli"
__date__ = "8/27/2019"
__copyright__ = "Copyright 2019, KnowNow-Nav"
__license__ = "0.0.0.1"
__maintainer__ = "Mauricio Lomeli"
__email__ = "mjlomeli@uci.edu"
__status__ = "Prototype"


def TestCase(*args, **kwargs):
    if isinstance(args, str):
        print(args)
        if '_RUN_NEO4J' == args:
            _RUN_NEO4J()
        elif 'createNewRelation' == args:
            _createNewRelation()
        elif 'closeDatabase' == args:
            _closeDatabase(args)

    if isinstance(args, tuple):
        if len(args) == 2:
            argum, var = args
            if '_RUN_NEO4J' == argum:
                _RUN_NEO4J(var)

        if len(args) == 5:
            _removeNode(args)
        if len(args) == 7:
            if args[0] == 'createNewRelation':
                _createNewRelation(args)


def _RUN_NEO4J(var=None):
    print('\033[31m' + 'You tried to run the Neo4j innapropriately:' + '\033[0m')
    if var is not None:
        if var is False:
            print('\033[93m' + 'You need to set _RUN_NEO4J=True' + '\033[0m')
        else:
            print('\033[93m' + 'Neo4j is crashing. Ask Anne and Jennifer about it.' + '\033[0m')


def _createNewRelation(*args):
    print('\033[31m' + 'You tried to use Neo4j to link one node to another and it failed:' + '\033[0m')
    if len(args) == 7:
        print('\033[93m' + 'Here are some variables that were used.' + '\033[0m')
        print('\033[93m' + str(args) + '\033[0m')


def _closeDatabase(*args):
    print('\033[31m' + 'Failed to close the database:' + '\033[0m')
    print('\033[93m' + 'These are the params (session, cell_count)' + '\033[0m')
    print('\033[93m' + str(args) + '\033[0m')


def _removeNode(*args):
    print('\033[31m' + 'Error removing a node from Neo4j:' + '\033[0m')
    print('\033[93m' + 'These are the params(session, id, header, content)' + '\033[0m')
    print('\033[93m' + str(args) + '\033[0m')


def _openDatabase(*args):
    print('\033[31m' + 'Error opening the database from Neo4j:' + '\033[0m')
    print('\033[93m' + 'These are the params(uri, username, password)' + '\033[0m')
    print('\033[93m' + str(args) + '\033[0m')


def testAll():
    print('\033[34m' + "_____Testing All Test Cases_____" + '\033[0m')
    testSpreadsheet()
    testCell()
    testRow()
    testFlaskDriver()
    testTokenizer()
    testSimilarity()
    testDocument()
