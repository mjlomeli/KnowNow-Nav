# !/usr/bin/env python

"""Cellexample

If the description is long, the first line should be a short summary of CellExample.py
that makes sense on its own, separated from the rest by a newline.
"""

__author__ = "Mauricio Lomeli"
__date__ = "8/31/2019"
__license__ = "0.0.0.2"
__maintainer__ = "Mauricio Lomeli"
__email__ = "mjlomeli@uci.edu"
__status__ = "Prototype"


class Cell:
    def __init__(self, content=None, header=None, ID=None):
        self.content = content
        self.header = header
        self.ID = ID
