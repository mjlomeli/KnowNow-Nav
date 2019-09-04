# !/usr/bin/env python

"""Neo4jdriver
Executes Neo4j Cypher statements through python. Some common functionality include opening the database and closing it.
"""

from Activity.Neo4j.CellExample import Cell
from neo4j import GraphDatabase, basic_auth

__authors__ = ["Anne Wang", "Jennifer Kwon", "Mauricio Lomeli"]
__credits__ = ["here you add anyone who contributed without code"]
__date__ = "9/2/2019"
__license__ = "MIT"
__version__ = "0.0.0.2"
__maintainer__ = ["Anne Wang", "Jennifer Kwon"]
__email__ = ["annew3@uci.edu", "Jennifer enter your professional emails"]
__status__ = "Prototype"


def run(session, query: str):
    # Todo: Run a query statement and return the result of running the query.
    # ex: run(session, "create (Anne)-[:friends_with]->(Jennifer)")
    # note, cant test for cypher queries really other than if it has been executed.
    # return the query result: return session.run(query)
    pass


def insertStr(session, data: str):
    # Todo: insert data into neo4j, if it is successful, return True, else False
    # the string is just a value.
    # ex: insertStr("Jennifer")
    # by default the label is called name (n: node {name: "Jennifer"})
    # Don't allow duplicates, instead update them.
    # Return True if the insertion is successful, else False if no insertion is done.
    pass


def insertCell(session, data: Cell):
    # Todo: insert data into neo4j, if it is successful, return True, else False
    # the Cell is an object with the string attributes: Cell.content, Cell.header and an integer Cell.ID
    # create a node with the label as the content and the properties being the header, content, and ID
    # ex. data.content = 'tylenol'   data.header = 'medication'   data.ID = 12
    # hint: create (n: cell {name: 'tylenol', ID: 12, header: 'medication', content: 'tylenol'})
    # note: ID is the row number in the spreadsheet if you can override ID in creating the node,
    # great, else just add it as a property. We want only to allow unique nodes, else update the node.
    # result node: (tylenol)
    # Don't allow duplicates, instead update them.
    # Return True if the insertion is successful, else False if no insertion is done.
    pass


def insertDict(session, data: dict):
    # Todo: insert data into neo4j, if it is sucessful, return True, else False
    # the dictionary is a relationship template. We need neo4j to insert these example values
    # ex: {'ID': 1, 'topic': '', 'date': 'July 2015', 'query_tag': 'Treatment', 'query': 'Patient had …', …, 'RO': ''}
    # for this dictionary, make the name = query_tag
    # ex: create (n: row {name: 'Treatment', ID: 1, topic: '', date: 'July 2015', query_tag: 'Treatment', ...})
    # Don't allow duplicates, instead update them.
    # Return True if the insertion is successful, else False if no insertion is done.
    pass


def linkStr(strA, link_message, strB):
    # Todo: link existing cells from the database. Both CallA and cellB must have been in the database.
    # the string strA and strB is a value of two nodes in the database
    # Link existing nodes with strA and strB values: strA_node--link_message-->strB_node
    # Return True if the linking is successful, else False if no linking is done.
    pass


def linkCells(cellA, link_message, cellB):
    # Todo: link existing cells from the database. Both CallA and cellB must have been in the database.
    # the Cell is an object with the string attributes: Cell.content, Cell.header and an integer Cell.ID
    # Link existing nodes cellA--link_message-->cellB
    # Return True if the linking is successful, else False if no linking is done.
    pass


def linkDict(session, dictA, link_message, dictB):
    # Todo: link existing data from neo4j, if it is successful, return True, else False if no linking was done.
    # the dictionary is a relationship template. We need neo4j to find all nodes with these example values
    # ex: {'Tylenol': [('causes', 'headaches'), ('causes', 'fatigue'), ('relieves', 'pain')]}
    # Neo4j: Cell('tylenol', 'medicine', 12), Cell('headaches', 'side effects', 12),
    # Cell('fatigue', 'side effects', 12), Cell('pain', 'intervention', 12)
    # note: id 12 means they are all in row 12. So must match/link all nodes within the same row.
    # Neo4j:
    #                          (fatigue)
    #                              ^
    #                              |
    #                 (tylenol)-causes->(headaches)
    #                 (tylenol)-relieves->(pain)
    pass


def closeDatabase(session):
    try:
        session.close()
    except:
        print("Could not close database.")


def openDatabase(uri: str, username: str, password: str):
    try:
        driver = GraphDatabase.driver(
                uri, auth=basic_auth(username, password))
        session = driver.session()
        return (session, driver)
    except:
        print("Could not open database.")


def createNode(start, link, end):
    return "CREATE ({})-[:{}]->({})".format(start.replace(' ', '_'),link.replace(' ', '_'),end.replace(' ', '_'))


def insertNode(session, label: str, label_property: str, specific_text: str):
    '''Insert a single node given a label, property, and property string'''
    insert_cq = ''' 
    CREATE (n:''' + label + "{" + label_property + ":" +  specific_text + '''})
    RETURN n})'''

    session.run(insert_cq)


def removeNode(session, label: str, label_property: str, specific_text: str):
    '''Provide a specific label, its specific text + property. Finds it and deletes it from graph.'''

    cypher_query = '''
    MATCH (n:''' + label + "{" + label_property + ":" +  specific_text + '''})
    DELETE n'''

    session.run(cypher_query)


def createNewRelation(session, label_from: str, label_from_text: str, label_to: str, label_to_text: str, new_relation: str, relation_text: str):
    '''creates a new relation from one specified node to another specified node with respective label and text'''

    cypher_query = "MATCH " + "(label_from: " + label_from + "{" + label_from + ":" + label_from_text + "})" + \
                    "MATCH (label_to" +  ":" + label_to + " {" + label_to + ":" +  label_to_text + "})" + \
                    "MERGE (label_from)-[rel:" + new_relation + "{" + new_relation + ":" +  relation_text + "}]->(label_to)"

    session.run(cypher_query)


def deleteRelation(session, label: str, prop: str, prop_text: str, relation: str, relation_text: str):
    '''deletes a specified relation that is related to a specified node'''
    cypher_query = "MATCH (n: " + label + "{" + prop + ":" + prop_text + "})-[" + relation + ":" + relation_text + ''']->()
                    DELETE ''' + relation

    session.run(cypher_query)


# Do not delete or modify
def insertList(data: list):
    """
    Separates the listing items into their categories of processing.
    Example: all string inputs get processed by insertStr function, and all Cell type
    inputs get processed by insertCell function.
    :param data: a list
    :return: True if the insertion is completed without failures, else False
    """
    if all([strings for strings in data if type(strings) == str]):
        return all([insertStr(strings) for strings in data])
    elif all([cells for cells in data if cells == Cell]):
        return all([insertCell(cells) for cells in data])
    elif all([rel for rel in data if type(rel) == dict]):
        return all([insertDict(rel) for rel in data])
    return False


# Do not delete or modify
def insert(data):
    """
    Handles the input dynamically. It detects the user's input and creates
    nodes relevant to the data.
    :param data: str, list, dict, or Cell types
    :return: True if successful, False otherwise
    """
    if isinstance(data, str):
        return insertStr(data)
    elif isinstance(data, list):
        return insertList(data)
    elif isinstance(data, dict):
        return insertDict(data)
    elif isinstance(data, Cell):
        return insertCell(data)
    else:
        return False


def setNext(_SESSION, header1, start, link, header2, end):
    header1 = 'Number_' + str(header1) if isinstance(header1, int) else header1
    header2 = 'Number_' + str(header2) if isinstance(header2, int) else header2
    link = 'Number_' + str(link) if isinstance(link, int) else link
    start = 'Number_' + str(start) if isinstance(start, int) else start
    end = 'Number_' + str(end) if isinstance(end, int) else end

    header1 = 'Number_' + str(int(header1)) if isinstance(header1, float) else header1
    header2 = 'Number_' + str(int(header2)) if isinstance(header2, float) else header2
    link = 'Number_' + str(int(link)) if isinstance(link, float) else link
    start = 'Number_' + str(int(start)) if isinstance(start, float) else start
    end = 'Number_' + str(int(end)) if isinstance(end, float) else end

    header1 = None if header1 == '' else header1
    header2 = None if header2 == '' else header2
    link = None if link == '' else link
    start = None if start == '' else start
    end = None if end == '' else end
    _SESSION.run("CREATE (n:{0}".format(str(start)) + " { " + " {0}: '{1}'".format(str(header1), str(
        start)) + "})-[:" + "{0}]->(m:{1}".format(str(link), str(end)) + " {" + "{0}: '{1}'".format(str(header2),
                                                                           str(end)) + "})")


def main():
    from Activity.Test.testNeo4j.testNeo4jDriver import testNeo4j
    testNeo4j()


if __name__ == '__main__':
    main()
