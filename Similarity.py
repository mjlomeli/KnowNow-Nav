# !/usr/bin/env python

"""Similarity

If the description is long, the first line should be a short summary of Similarity.py
that makes sense on its own, separated from the rest by a newline.
"""

from pathlib import Path
from Spreadsheet import Spreadsheet
from Tokenizer import Tokenizer
import pickle
from math import log10, sqrt
from heapq import nlargest

__author__ = "Mauricio Lomeli"
__date__ = "8/22/2019"
__license__ = "MIT"
__version__ = "0.0.0.1"
__maintainer__ = "Mauricio Lomeli"
__email__ = "mjlomeli@uci.edu"
__status__ = "Prototype"

__data = Path.cwd() / Path('data') / Path('scores.pickle')
__sheet = Spreadsheet()
__corp_size = 37
__tokenizer = Tokenizer()
__index = {}
__max_postings_size = 15
__IDF_WEIGHING = True


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
    return log10(diff / df_t) if diff > 0 else 0


def __score(term, row, index=__index):
    if isinstance(term, str) and term in index:
        tf = index[term][row] if row in index[term] else 0
        return (1 + log10(tf)) if tf > 0 else 0
    elif isinstance(term, list):
        return __weighing(term, row, index)


"""
def __score(term, row, index=__index):
    if isinstance(term, str) and term in index:
        tf = index[term][row] if row in index[term] else 0
        return (1 + log10(tf)) if tf > 0 else 0
    elif isinstance(term, list):
        score = 0
        for word in term:
            score += __score(word, row, index)
        return score
"""


def __idf(term, index=__index):
    if isinstance(term, str):
        if term in index:
            n = __corp_size
            df_t = sum([1 for x in list(index[term].values()) if x > 0])
            return log10(n / df_t) if df_t > 0 else 0
        else:
            return 0
    else:
        raise TypeError('term in __idf function must be a string.')


def __weighing(term, row, index=__index):
    if isinstance(term, str):
        if __IDF_WEIGHING:
            return __score(term, row, index) * __idf(term, index)
        else:
            return __score(term, row, index)
    elif isinstance(term, list):
        score = 0
        for word in term:
            if __IDF_WEIGHING:
                score += __score(word, row, index) * __idf(word, index)
            else:
                score += __score(word, row, index)
        return score
    else:
        raise TypeError('term in function __weighing must be a string or list of strings.')


def __length_norm(term, row, index=__index):
    if term in index and row in index[term]:
        d_term = __weighing(term, row, index) if __IDF_WEIGHING else __score(term, row, index)
        if __IDF_WEIGHING:
            d_norm = sqrt(sum([__weighing(words, row, index) ** 2 for words in index.keys()]))
        else:
            d_norm = sqrt(sum([__score(words, row, index)**2 for words in index.keys()]))
        if d_norm > 0:
            return d_term / d_norm
        else:
            return 0


def __cosine(row1, row2, index=__index):
    return sum([__length_norm(word, row1) * __length_norm(word, row2) for word in list(index.keys())])


def __cosine_score(query, index=__index):
    """
    Optimized cosines efficiently with unweighted query terms
    :param query: a list of the query
    :param index: a custom index if the default isn't wanted
    :return: the Nth largest scores, where N = __max_postings_size = 15
    """
    if isinstance(query, list):
        query = [query]
    scores = [0] * __corp_size
    length = len(index[list(index.keys())[0]])
    doc_word_count = [sum([index[item][i] for item in index.keys() if index[item][i] > 0]) for i in range(length)]
    for term in query:
        w_q = __weight_query(term, query, index)
        for i in range(length):
            scores[i] += __weighing(term, i, index) * w_q
    for i in range(length):
        scores[i] = scores[i] / doc_word_count[i]
    return nlargest(__max_postings_size, list(zip(scores, [i for i in range(length)])))


def __weight_query(term, query, index=__index):
    if isinstance(query, str):
        query = [query]
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
    testing()


def testing():
    """
    When testing, must change N to 37 by making the variable __corp_size = 37
    :return:
    """
    index = {'antony': {0: 157, 1: 73, 2: 0, 3: 0, 4: 0, 5: 0},
             'brutus': {0: 4, 1: 157, 2: 0, 3: 1, 4: 0, 5: 0},
             'caesar': {0: 232, 1: 227, 2: 0, 3: 2, 4: 1, 5: 1},
             'calpurnia': {0: 0, 1: 10, 2: 0, 3: 0, 4: 0, 5: 0},
             'cleopatra': {0: 57, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
             'mercy': {0: 2, 1: 0, 2: 3, 3: 5, 4: 5, 5: 1},
             'worser': {0: 2, 1: 0, 2: 1, 3: 1, 4: 1, 5: 0}}

    print('Antony:\t\t' + str(__weighing('antony', 0, index)))
    print('Brutus:\t\t' + str(__weighing('brutus', 0, index)))
    print('caesar:\t\t' + str(__weighing('caesar', 0, index)))
    # different functions displaying displaying the same results, in case
    # someone doesn't know the difference between __score(queries) and __weighing(queries)
    print('Brutus, Caesar:\t\t' + str(__score(['brutus', 'caesar'], 0, index)))
    print('Brutus, Caesar:\t\t' + str(__weighing(['brutus', 'caesar'], 0, index)))

    index = {
        'affection': {0: 115, 1: 58, 2: 20},
        'jealous': {0: 10, 1: 7, 2: 11},
        'gossip': {0: 2, 1: 0, 2: 6},
        'wuthering': {0: 0, 1: 0, 2: 38}}

    print('affection:\t\t' + str(__length_norm('affection', 0, index)))
    print('jealous:\t\t' + str(__length_norm('jealous', 0, index)))
    print('gossip:\t\t' + str(__length_norm('gossip', 0, index)))
    print('wuthering\t\t' + str(__weighing('wuthering', 0, index)))


if __name__ == '__main__':
    main()
