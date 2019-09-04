# !/usr/bin/env python
"""Testing of Neo4jDriver.

If the description is long, the first line should be a short summary 
that makes sense on its own, separated from the rest by a newline.
"""

import unittest
import getpass
from nltk.corpus import words
import random
from Activity.Neo4j.Neo4jDriver import run, insertDict, insertCell, insertStr, insertList, insert, openDatabase, closeDatabase

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
        self.session = None
        try:
            self.session = openDatabase(self.uri, self.username, self.password)[0]
        except Exception as e:
            self.fail("Failed to open the database: neo4jDriver = openDatabase(uri, username, password)")
        try:
            delete_all_relationships(self.session)
            delete_all_nodes(self.session)
        except Exception as e:
            self.fail("Failed to clear the database: ask {} for help.".format(str(__maintainer__)))

    def test_run(self):
        query = 'match (n) return n;'
        result = run(self.session, query)
        statement = result.summary().statement
        self.assertEqual(query, statement)
        test_list = [None, '', '\n', '\r', '0', '0.0001', '0x1234', '0e-12']
        for item in test_list:
            try:
                run(self.session, item)
            except Exception as e:
                message = "Failed executing run(session, '{}'). Your function must ignore these "
                message += "without crashing. Possibly not even including them."
                self.fail(message.format(str(item)))

    def test_escapeChar(self):
        test_list = [None, '', '\n', '\r', '0', '0.0001', '0x1234', '0e-12']
        title = "Testing Escape Characters"
        print(title)

        start = 0
        correct = 0
        end = len(test_list) * 2
        printProgressBar(start, end, title, "{}/{}".format(start, end))

        for item in test_list:
            try:
                start += 1
                printProgressBar(start, end, title, "{}/{}".format(start, end))
                insertStr(item)
                correct += 1
            except Exception as e:
                message = "Failed inserting into insertStr('{}'). Your function must ignore these "
                message += "without crashing. Possibly not even include them."
                self.fail(message.format(str(item)))
        for item in test_list:
            try:
                start += 1
                printProgressBar(start, end, title, "{}/{}".format(start, end))
                insertCell(Cell(item, item))
                correct += 1
            except Exception as e:
                message = "Failed inserting into insertCell('{}','{}'). Your function must ignore these "
                message += "without crashing. Possibly not even include them."
                self.fail(message.format(str(item), str(item)))

    def test_insertStr(self):
        clear(self.session)
        start = 0
        correct = 0
        end = 2000
        word_list = words.words()

        printProgressBar(start, end, "Testing insertStr", "{}/{}".format(start, end))
        for count in range(end):
            try:
                start += 1
                from_word_list = random.choice(word_list)
                insertStr(from_word_list)
                values = getValues(self.session)
                exists = ['name' in val and val['name'] == from_word_list for val in values]
                if any(exists):
                    if exists.count(True) > 1:
                        self.fail("Found multiple instances of the same node. The node must be unique.")
                    else:
                        correct += 1
                else:
                    self.fail("Couldn't find {name: '{}'} as a node in Neo4j.".format(from_word_list))
                printProgressBar(start, end, "Testing insertStr", "{}/{}".format(start, end))
            except Exception as e:
                self.fail("Failed inserting into insertStr('" + str(from_word_list) + "')")
                printProgressBar(start, end, "Testing insertStr", "{}/{}".format(start, end))
        print()
        print("Testing insertStr: {} errors found".format(end-correct))

    def test_insertCell(self):
        clear(self.session)
        start = 0
        correct = 0
        end = 2000
        word_list = words.words()
        printProgressBar(start, end, "Testing insertCell", "{}/{}".format(start, end))
        for count in range(end):
            try:
                start += 1
                header = random.choice(word_list)
                content = random.choice(word_list)
                cell = Cell(content, header)
                insertCell(cell)
                values = getValues(self.session)
                exists = ['name' in val and val['name'] == from_word_list for val in values]
                if any(exists):
                    if exists.count(True) > 1:
                        self.fail("Found multiple {name: '{}'} nodes, must be unique.".format(from_word_list))
                    else:
                        correct += 1
                else:
                    self.fail("Couldn't find {name: '{}'} as a node.".format(from_word_list))
                printProgressBar(start, end, "Testing insertStr", "{}/{}".format(start, end))
            except Exception as e:
                self.fail("Failed inserting into insertCell('{}','{}')".format(content, header))
                printProgressBar(start, end, "Testing insertCell", "{}/{}".format(start, end))
        print()
        print("Testing insertCell: {} errors found".format(end-correct))

    def test_insertDict(self):
        clear(self.session)
        start = 0
        correct = 0
        end = 2000
        word_list = words.words()
        printProgressBar(start, end, "Testing insertDict", "{}/{}".format(start, end))
        for count in range(end):
            try:
                start += 1
                name = random.choice(word_list)
                field1 = random.choice(word_list)
                field2 = random.choice(word_list)
                field3 = random.choice(word_list)
                field4 = random.choice(word_list)
                dictionary = {'name': name, 'field1': field1, 'field2': field2, 'field3': field3, 'field4': field4}
                insertDict(dictionary)
                values = getValues(self.session)
                exists = ['name' in val and val['name'] == from_word_list for val in values]
                if any(exists):
                    if exists.count(True) > 1:
                        self.fail("Found multiple {name: '{}'} nodes, must be unique.".format(from_word_list))
                    else:
                        index = exists.index(True)
                        node = values[index]
                        if node['name'] == name and node['field1'] == field1 and node['field2'] == field2 and \
                                node['field3'] == field3 and node['field4'] == field4:
                            correct += 1
                else:
                    self.fail("Couldn't find {name: '{}'} as a node.".format(from_word_list))
                printProgressBar(start, end, "Testing insertDict", "{}/{}".format(start, end))
            except Exception as e:
                self.fail("Failed inserting into insertCell('{}','{}')".format(content, header))
                printProgressBar(start, end, "Testing insertDict", "{}/{}".format(start, end))
        print()
        print("Testing insertDict: {} errors found".format(end-correct))

    def tearDown(self):
        try:
            closeDatabase(self.neo4jdriver[0])
        except Exception as e:
            self.fail("Failed to close the database: closeDatabase(neo4jDriver[0])")


def delete_all_relationships(session):
    query = "MATCH (n) DETACH DELETE n;"
    session.run(query)


def delete_all_nodes(session):
    query = "MATCH (n) DELETE n;"
    session.run(query)


def clear(session):
    """
    Removes all nodes and relationships.
    :param session: the Neo4j session
    """
    delete_all_relationships(session)
    delete_all_nodes(session)


def create_node_frm_lists(session, node_type, headers: list, contents: list):
    query = "create(n: {} {".format(node_type)
    for header, content in zip(headers, contents):
        query += "{}: '{}',".format(header, content)
    query = query[:-1] + "})"
    session.run(query)


def create_node_frm_dict(session, node_type, dictionary: dict):
    query = "create(n: {} {".format(node_type)
    for header, content in dictionary.items():
        query += "{}: '{}',".format(header, content)
    query = query[:-1] + "})"
    session.run(query)


def getValues(session):
    query = 'match (n) return n;'
    results = session.run(query)
    return [dict(values) for val in results.values() for values in val]


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
    print("Testing Neo4j")
    import subprocess as sub
    import os
    if os.name == 'nt':
        sub.run(['python', '-m', 'unittest', 'Activity/Test/testNeo4j/testNeo4jDriver.py'])
    elif os.name == 'posix':
        sub.run(['python3', '-m', 'unittest', 'Activity/Test/testNeo4j/testSpreadsheet.py'])
    elif os.name == 'darwin':
        sub.run(['python3', '-m', 'unittest', 'Activity/Test/testNeo4j/testSpreadsheet.py'])
    else:
        message = "Tell " + str(__maintainer__) + " the test functions can't find your OS system type"
        raise (NotImplementedError, message)


if __name__ == "__main__":
    main()
