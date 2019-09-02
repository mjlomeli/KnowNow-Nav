# !/usr/bin/env python
"""Testing of Neo4jDriver.

If the description is long, the first line should be a short summary 
that makes sense on its own, separated from the rest by a newline.
"""

import unittest
import getpass
from nltk.corpus import words
import random
from Activity.Neo4j.Neo4jDriver import insertDict, insertCell, insertStr, insertList, insert, openDatabase, closeDatabase

__author__ = "Mauricio Lomeli"
__date__ = "8/30/2019"
__maintainer__ = "Mauricio Lomeli"
__email__ = "mjlomeli@uci.edu"
__status__ = "Prototype"
__version__ = "0.0.0.2"


class Cell:
    def __init__(self, content=None, header=None, id=1):
        self.content = content
        self.header = header
        self.id = id


def testNeo4j():
    print("Testing Neo4jDriver")
    unittest.main()


class TestNeo4jDriver(unittest.TestCase):

    def setUp(self):
        self.uri = input("Enter your Neo4j URI: ")
        self.username = input("Enter your username: ")
        self.password = getpass.getpass("Enter your Neo4j password: ")
        printProgressBar(0, 1, "Opening Database")
        self.neo4jdriver = openDatabase(self.uri, self.username, self.password)
        printProgressBar(1, 1, "Opening Database")

    def test_insertStr(self):
        start = 0
        end = 2000
        word_list = words.words()
        for count in range(end):
            try:
                from_word_list = random.choice(word_list)
                insertStr(from_word_list)
                start += 1
            except Exception as e:
                self.fail("Failed with inserting into insertStr: " + from_word_list)



    def test_insertCell(self):
        start = 0
        end = 2000
        word_list = words.words()
        for count in range(end):
            try:
                header = random.choice(word_list)
                content = random.choice(word_list)
                insertStr(from_word_list)
                start += 1
            except Exception as e:
                self.fail("Failed with inserting into insertStr: " + from_word_list)



    def tearDown(self):
        printProgressBar(0, 1, "Closing Database")
        closeDatabase(self.neo4jdriver[0])
        printProgressBar(1, 1, "Closing Database")


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█'):
    """ 
    Displays a progress bar for each iteration. I've added my own personal twist to make it more functional.
    Title: Progress Bar
    Author: Benjamin Cordier
    Date: 6/10/2019
    Availability: https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    """
    if int(iteration % (total / 100)) == 0 or iteration == total or prefix is not '' or suffix is not '':
        # calculated percentage of completeness
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        # modifies the bar
        bar = fill * filledLength + '-' * (length - filledLength)
        # Creates the bar
        print('\r\t\t{} |{}| {}% {}'.format(prefix, bar, percent, suffix), end='\r')
        # Print New Line on Complete
        if iteration == total:
            print()


def main():
    testNeo4j()


if __name__ == "__main__":
    main()
