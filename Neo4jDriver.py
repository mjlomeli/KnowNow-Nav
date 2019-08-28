# !/usr/bin/env python

"""Neo4jdriver
If the description is long, the first line should be a short summary of Neo4jDriver.py
that makes sense on its own, separated from the rest by a newline.
"""

from pathlib import Path


PATH = Path.cwd()

__author__ = "Mauricio Lomeli"
__date__ = "8/17/2019"
__license__ = "MIT"
__version__ = "0.0.0.1"
__maintainer__ = "Mauricio Lomeli"
__email__ = "mjlomeli@uci.edu"
__status__ = "Prototype"

def createNode(start, link, end):
    return "CREATE ({})-[:{}]->({})".format(start.replace(' ', '_'),link.replace(' ', '_'),end.replace(' ', '_'))


def create_database():
    from Spreadsheet import Spreadsheet
    sheet = Spreadsheet()
    query = "CREATE "
    for i, row in enumerate(sheet):
        query += '(' + str(i) + ':Discussion ' + str({head: content.replace(' ', '_').replace('', 'EMPTY_STRING') for
                                              head, content in zip(sheet.headers, sheet[i])}) + '),'
    return query




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

