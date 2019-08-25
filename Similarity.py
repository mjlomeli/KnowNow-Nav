# !/usr/bin/env python

"""Similarity

If the description is long, the first line should be a short summary of Similarity.py
that makes sense on its own, separated from the rest by a newline.
"""

from pathlib import Path
from Spreadsheet import Spreadsheet
from tokenizer import Tokenizer
import pickle
import math

__author__ = "Mauricio Lomeli"
__date__ = "8/22/2019"
__license__ = "MIT"
__version__ = "0.0.0.1"
__maintainer__ = "Mauricio Lomeli"
__email__ = "mjlomeli@uci.edu"
__status__ = "Prototype"

__data = Path.cwd() / Path('data') / Path('scores.pickle')
__sheet = Spreadsheet()
__tokenizer = Tokenizer()
__index = {}

# TODO: write your code here


def __file():
    if not __data.exists():
        return {}
    else:
        with open(__data, 'rb') as f:
            return pickle.load(f)


def __write(pickle_data):
    with open(__data, 'wb') as w:
        pickle.dump(pickle_data, w)


def __score(query, row: int):
    score = 0
    if isinstance(query, str):
        tf = __index[query][row]
        score += (1 + math.log10(tf)) if tf > 0 else 0
    elif isinstance(query, list):
        for word in query:
            if word in __index and row in __index[word]:
                tf = __index[word][row]
                score += (1 + math.log10(tf)) if tf > 0 else 0
    elif isinstance(query, dict):
        __tokenizer.open(__sheet.convertToDict(query))
        tokens = __tokenizer.tokens
        for word in tokens:
            if word in __index and row in __index[word]:
                tf = __index[word][row]
                score += (1 + math.log10(tf)) if tf > 0 else 0
    return score


def __cosine():
    pass


def __process_index():
    for i, row in enumerate(__sheet):
        __tokenizer.open(__sheet.convertToDict(row))
        tokens = __tokenizer.tokens
        for tok in tokens:
            if tok in __index:
                __index[tok][i] = __tokenizer.tf[tok]
            else:
                __index[tok] = {i: __tokenizer.tf[tok]}
    return __index


def main():
    index = __process_index()
    print(index.keys())
    print(index.values())


if __name__ == '__main__':
    main()
