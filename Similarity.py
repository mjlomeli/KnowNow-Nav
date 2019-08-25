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
__corp_size = len(__sheet)
__tokenizer = Tokenizer()
__index = {}

__IDF_WEIGHING = False


def __file():
    if not __data.exists():
        return {}
    else:
        with open(__data, 'rb') as f:
            return pickle.load(f)


def __write(pickle_data):
    with open(__data, 'wb') as w:
        pickle.dump(pickle_data, w)


def __prob_idf(term, index=__index):
    df_t = sum([1 for x in list(index[term].values()) if x > 0])
    diff = __corp_size - df_t
    return math.log10(diff / df_t) if diff > 0 else 0


def __score(query, row: int, index=__index):
    score = 0
    if isinstance(query, str) and query in index:
        tf = index[query][row] if row in index[query] else 0
        score += (1 + math.log10(tf)) if tf > 0 else 0
    elif isinstance(query, list):
        for word in query:
            if word in index and row in index[word]:
                tf = index[word][row]
                score += (1 + math.log10(tf)) if tf > 0 else 0
    return score


def __idf(term, index=__index):
    n = __corp_size
    df_t = sum([1 for x in list(index[term].values()) if x > 0])
    return math.log10(n / df_t) if df_t > 0 else 0


def __weighing(term, row, index=__index):
    return __score(term, row, index) * __idf(term, index)


def __length_norm(term, row, index=__index):
    if term in index and row in index[term]:
        d_term = __weighing(term, row) if __IDF_WEIGHING else __score(term, row)
        if __IDF_WEIGHING:
            d_norm = math.sqrt(sum([__weighing(words, row) ** 2 for words in list(index.keys())]))
        else:
            d_norm = math.sqrt(sum([__score(words, row)**2 for words in list(index.keys())]))
        if d_norm > 0:
            return d_term / d_norm
        else:
            return 0


def __cosine(row1, row2, index=__index):
    return sum([__length_norm(word, row1) * __length_norm(word, row2) for word in list(index.keys())])


def __cosine_score(query: list):
    scores = 0
    length = __corp_size
    for term in query:
        __weighing(term, )


def __weight_query(term, query, index=__index):
    q__index = {}
    __tokenizer.open(query)
    q_tf = __tokenizer.tf

    tokens = __tokenizer.tokens
    for tok in tokens:
        if tok in q__index:
            q__index[tok][0] = q_tf[tok]
        else:
            q__index[tok] = {0: q_tf[tok]}

    return __weighing(term, 0, q__index)


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
    a = ['antony', 'brutus', 'caesar', 'calpurnia', 'cleopatra', 'mercy', 'worser']
    ant_and_cleo = [157, 4, 232, 0, 57, 2, 2]
    ju_cea = [73, 157, 227, 10, 0, 0, 0]
    tempest = [0, 0, 0, 0, 0, 3, 1]
    ham = [0, 1, 2, 0, 0, 5, 1]
    othe = [0, 0, 1, 0, 0, 5, 1]
    mac = [0, 0, 1, 0, 0, 1, 0]
    index = {}
    for i in range(len(a)):
        index[a[i]] = {0: ant_and_cleo[i]}
        index[a[i]][1] = ju_cea[i]
        index[a[i]][2] = tempest[i]
        index[a[i]][3] = ham[i]
        index[a[i]][4] = othe[i]
        index[a[i]][5] = mac[i]

    __index = index  # must place this and all above outside of main to work.
                     # and must change n in the idf function to 37

    print('Antony:\t\t' + str(__score('antony', 0) * __idf('antony')))
    print('Brutus:\t\t' + str(__weighing(['brutus'], 0)))
    print('caesar:\t\t' + str(__weighing(['caesar'], 0)))
    print('Brutus, Caesar:\t\t' + str(__weighing(['brutus', 'caesar'], 0)))


    """
    Cosine Similarity
    For Vector Space Similarity slide Sec 6.3

    def __length_norm(term, row):
        if term in __index and row in __index[term]:
            d_term = __score(term, row)
            d_norm = math.sqrt(sum([__score(words, row) ** 2 for words in list(__index.keys())]))
            return d_term / d_norm
    """

if __name__ == '__main__':
    main()