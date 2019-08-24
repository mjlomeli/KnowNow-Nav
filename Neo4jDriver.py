# !/usr/bin/env python

"""Neo4jdriver

If the description is long, the first line should be a short summary of Neo4jDriver.py
that makes sense on its own, separated from the rest by a newline.
"""

from pathlib import Path
from neo4j import GraphDatabase, basic_auth

PATH = Path.cwd()

# program's author information and licenses
__authors__ = "Jennifer Kwon, Anne Wang, Mauricio Lomeli"
__credits__ = ["Smruti Vidwans"]
__date__ = "8/15/2019"
__license__ = "MIT"
__version__ = "0.0.0.1"
__maintainer__ = "Jennifer Kwon, Anne Wang"
__email__ = "mjlomeli@uci.edu"
__status__ = "Prototype"

driver = GraphDatabase.driver(
    "bolt://34.203.33.130:38790",
    auth=basic_auth("neo4j", "excuses-bush-reels"))
session = driver.session()

cypher_query = '''
MATCH (n)
RETURN id(n) AS id
LIMIT 10
'''

results = session.run(cypher_query,
  parameters={})

for record in results:
  print(record['id'])


class HelloWorldExample(object):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def print_greeting(self, message):
        with self._driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting, message)
            print(greeting)

    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        return result.single()[0]

