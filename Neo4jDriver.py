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

