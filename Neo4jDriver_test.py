# Anne Wang
# !/usr/bin/env python

"""Neo4jdriver
If the description is long, the first line should be a short summary of Neo4jDriver.py
that makes sense on its own, separated from the rest by a newline.
"""

from pathlib import Path
from neo4j import GraphDatabase, basic_auth

PATH = Path.cwd()

__author__ = "Mauricio Lomeli"
__date__ = "8/17/2019"
__license__ = "MIT"
__version__ = "0.0.0.1"
__maintainer__ = "Mauricio Lomeli"
__email__ = "mjlomeli@uci.edu"
__status__ = "Prototype"

def openDatabase(uri: str, username: str, password: str):
    try:
        driver = GraphDatabase.driver(
                uri, auth=basic_auth(username, password))
        session = driver.session()

        return (session, driver)

    except:
        pass

def closeDatabase(session):
    try:
        session.close()

    except:
        pass

def getSession(session):
    return session

def getDriver(driver):
    return driver

def insertNode(session, label: str, label_property: str, specific_text: str):
    '''Insert a single node given a label, property, and property string'''
    try:
        insert_cq = ''' 
        CREATE (n:`''' + label + "`{`" + label_property + "`:\"" +  specific_text + '''\"}) 
        RETURN n'''

        session.run(insert_cq)
    except:
        pass


def removeNode(session, label: str, label_property: str, specific_text: str):
    '''Provide a specific label, its specific text + property. Finds it and deletes it from graph.'''
    try:
        cypher_query = '''
        MATCH (n:`''' + label + "`{`" + label_property + "`:\"" +  specific_text + '''\"})
        DELETE n'''

        session.run(cypher_query)

    except: 
        pass

def createNewRelation(session, label_from: str, label_from_prop: str, label_from_text: str, label_to: str, label_to_prop: str, label_to_text: str, new_relation: str, rel_prop: str, relation_text: str):
    '''creates a new relation from one specified node to another specified node with respective label and text'''
    try:
        cypher_query = "MATCH " + "(label_from: `" + label_from + "`{`" + label_from_prop + "`:\"" + label_from_text + "\"})" + \
                        "MATCH (label_to" +  ":`" + label_to + "` {`" + label_to_prop + "`:\"" +  label_to_text + "\"})" + \
                        "MERGE (label_from)-[rel:`" + new_relation + "`{`" + rel_prop + "`:\"" +  relation_text + "\"}]->(label_to)"

        session.run(cypher_query)
    except:
        pass

def deleteRelation(session, label: str, prop: str, prop_text: str, relation: str):
    '''deletes a specified relation that is related to a specified node'''
    try:
        cypher_query = "MATCH (n: `" + label + "`{`" + prop + "`:\"" + prop_text + "\"})-[r:`" + relation + '''`]->()
                        DELETE r''' 
                       
        session.run(cypher_query)
    except:
        pass
