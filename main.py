# !/usr/bin/env python

"""KnowNow

If the description is long, the first line should be a short summary of KnowNowNav.py
that makes sense on its own, separated from the rest by a newline.
"""

from pathlib import Path
import sys

__DATA = Path.cwd() / Path('Data')

__author__ = ["Mauricio Lomeli"]
__date__ = "8/22/2019"
__credits__ = ["Rebecca Zhuo, Smruti Vidwans"]
__license__ = "MIT"
__version__ = "0.0.0.1"
__maintainer__ = "Mauricio Lomeli"
__email__ = "mjlomeli@uci.edu"
__status__ = "Prototype"

# TODO: This is the main file to run everyone's code.
# TODO: This will combine everyone's material and should
# TODO: be the only file anyone should ever see.


def main():
    pass


def __reset():
    for file in __DATA.iterdir():
        if '.pickle' in file.name:
            file.unlink()


def __test(tests=None):
    if tests is not None and len(tests) > 0:
        for test_case in tests:
            if test_case == 'FileManager':
                #from Activity.Test.testFileManager import testRow, testSpreadsheet, testCell
                # Todo: Call test for FileManager
                print("Testing FileManager")
            elif test_case == 'Neo4j':
                #from Activity.Test.testNeo4j import testNeo4jDriver
                # Todo: Call test for Neo4j
                print("Testing Neo4j")
            elif test_case == 'Web':
                #from Activity.Test.testWeb import testFlaskDriver
                # Todo: Call test for Web
                print("Testing Web")
            elif test_case == 'NLP':
                #from Activity.Test.testNLP import *
                # Todo: Call test for NLP
                print("Testing NLP")
    else:
        #from Activity.Test.testFileManager import testRow, testSpreadsheet, testCell
        #from Activity.Test.testNeo4j import testNeo4jDriver
        #from Activity.Test.testWeb import testFlaskDriver
        #from Activity.Test.testNLP import *
        # Todo: Call test for everything
        print("Testing Everything")


if __name__ == '__main__':
    if '-r' in sys.argv:
        __reset()
    if '-t' in sys.argv:
        test = []
        if 'Neo4j' in sys.argv:
            test.append('Neo4j')
        if 'FileManager' in sys.argv:
            test.append('FileManager')
        if 'Web' in sys.argv:
            test.append('Web')
        if 'NLP' in sys.argv:
            test.append('NLP')
        __test(test)

    main()
