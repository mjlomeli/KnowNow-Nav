# !/usr/bin/env python

"""Similarity

If the description is long, the first line should be a short summary of Similarity.py
that makes sense on its own, separated from the rest by a newline.
"""

import sys
from pathlib import Path
from Spreadsheet import Spreadsheet
from Tokenizer import Tokenizer
import pickle
from math import log10, sqrt
from heapq import nlargest
from Document import Row

__author__ = "Mauricio Lomeli"
__credits__ = ['Prof. Mustafa Ibrahim']
__date__ = "8/22/2019"
__license__ = "MIT"
__version__ = "0.0.0.1"
__maintainer__ = "Mauricio Lomeli"
__email__ = "mjlomeli@uci.edu"
__status__ = "Prototype"

__data = Path.cwd() / Path('data') / Path('scores.pickle')
__IDF_WEIGHTING = True     # must set to True to run original program
__corpus = Spreadsheet()             # must add your file/items here like your corpus
__corp_size = len(__corpus)                 # must change value
__tokenizer = Tokenizer()
__index = {}
__max_postings_size = 15    # choose maximum number of results for cosine


def file():
    if not __data.exists():
        index = __process_index()
        with open(__data, 'wb') as w:
            pickle.dump(index, w)
            __index = index
    else:
        with open(__data, 'rb') as f:
            __index = pickle.load(f)


def __prob_idf(term, index=__index):
    df_t = sum([1 for x in list(index[term].values()) if x > 0])
    diff = __corp_size - df_t
    return log10(diff / df_t) if diff > 0 else 0


def __score(term, row, index=__index):
    if isinstance(term, str) and term in index:
        tf = index[term][row] if row in index[term] else 0
        return (1 + log10(tf)) if tf > 0 else 0
    elif isinstance(term, list):
        return __weighting(term, row, index)


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


def __weighting(term, row, index=__index):
    if isinstance(term, str):
        if __IDF_WEIGHTING:
            return __score(term, row, index) * __idf(term, index)
        else:
            return __score(term, row, index)
    elif isinstance(term, list):
        score = 0
        for word in term:
            if __IDF_WEIGHTING:
                score += __score(word, row, index) * __idf(word, index)
            else:
                score += __score(word, row, index)
        return score
    else:
        raise TypeError('term in function __weighting must be a string or list of strings.')


def __length_norm(term, row, index=__index):
    if term in index and row in index[term]:
        d_term = __weighting(term, row, index) if __IDF_WEIGHTING else __score(term, row, index)
        if __IDF_WEIGHTING:
            d_norm = sqrt(sum([__weighting(words, row, index) ** 2 for words in index.keys()]))
        else:
            d_norm = sqrt(sum([__score(words, row, index)**2 for words in index.keys()]))
        if d_norm > 0:
            return d_term / d_norm
        else:
            return 0


def __cosine(row1, row2, index=__index):
    return sum([__length_norm(word, row1, index) * __length_norm(word, row2, index) for word in index.keys()])


def cosine_score(query, index=__index):
    """
    Optimized cosines efficiently with unweighted query terms
    :param query: a list of the query
    :param index: a custom index if the default isn't wanted
    :return: the Nth largest scores, where N = __max_postings_size = 15
    """
    if isinstance(query, str):
        query = [query]
    scores = [0] * __corp_size
    length = len(index[list(index.keys())[0]])
    doc_word_count = [sum([index[item][i] for item in index.keys() if index[item][i] > 0]) for i in range(length)]
    for term in query:
        w_q = __weight_query(term, query, index)
        for i in range(length):
            scores[i] += __weighting(term, i, index) * w_q
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

    return __weighting(term, 0, q__index)


def combine_tf(tf: list):
    combined = {}
    for item in tf:
        for term, freq in item.items():
            if term in combined:
                combined[term] += freq
            else:
                combined[term] = freq
    return combined

def __process_index():
    """
    Your corpus must be iterable to use this function.
    Also, it should allow to convert itself into a dictionary.
    The keys will be the special tags which have additional weight.
    :return: dict, index holding term frequency
    """
    CATEGORIES = ["Comparing Therapies", "Side Effects", "Right treatment?", "Specific Therapy Inquiries",
                  "Others' experience", 'Symptoms diagnosis', 'Side effect management', 'Recurrence Queries',
                  'Specific Conditions', 'Data interpretation', 'Referral', 'Lifestyle', 'Positive Affirmations',
                  'Encouragement', 'Inter-Personal Patient Connections', 'Other/ Miscellaneous']
    corpus = []
    rows = []
    category = []
    query_tag = []
    cohort = []
    for i, row in enumerate(__corpus):
        row_doc = Row(__corpus.headers, row)
        corpus.append(row_doc)
        rows += [cell.getTF() for cell in row_doc]

        category += [cell.getTF() for cell in row_doc if row_doc['category'] is not None and row_doc['category'] is not '']
        query_tag += [cell.getTF() for cell in row_doc if row_doc['query_tag'] is not None and row_doc['query_tag'] is not '']
        cohort += [cell.getTF() for cell in row_doc if row_doc['cohort'] is not None and row_doc['cohort'] is not '']

    category = combine_tf(category)
    query_tag = combine_tf(query_tag)
    cohort = combine_tf(cohort)
    index = combine_tf(rows)

    return {'category': category, 'query_tag': query_tag, 'cohort': cohort, 'index':index }


def main():
    pass


def test():
    if __IDF_WEIGHTING:
        index = {'antony': {0: 157, 1: 73, 2: 0, 3: 0, 4: 0, 5: 0},
                 'brutus': {0: 4, 1: 157, 2: 0, 3: 1, 4: 0, 5: 0},
                 'caesar': {0: 232, 1: 227, 2: 0, 3: 2, 4: 1, 5: 1},
                 'calpurnia': {0: 0, 1: 10, 2: 0, 3: 0, 4: 0, 5: 0},
                 'cleopatra': {0: 57, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                 'mercy': {0: 2, 1: 0, 2: 3, 3: 5, 4: 5, 5: 1},
                 'worser': {0: 2, 1: 0, 2: 1, 3: 1, 4: 1, 5: 0}}

        result = __weighting('antony', 0, index)
        assert abs(result - 4.05) < 0.01, '__weighting(antony,0) must be about 4.05, result=' + str(result)
        result = __weighting('brutus', 0, index)
        assert abs(result - 1.75) < 0.01, '__weighting(brutus,0) must be about 1.75, result=' + str(result)
        result = __weighting('caesar', 0, index)
        assert abs(result - 2.93) < 0.01, '__weighting(caesar,0) must be about 2.93, result=' + str(result)
        result = __score(['brutus', 'caesar'], 0, index)
        assert abs(result - 4.67) < 0.01, '__score([brutus,caesar],0) must be about 4.67, result=' + str(result)
        result = __weighting(['brutus', 'caesar'], 0, index)
        assert abs(result - 4.67) < 0.01, '__weighting([brutus,caesar],0) must be about 4.67, result=' + str(result)
        print('\033[1m\033[92m' + '100% passed' + '\033[0m')
        print('\033[90m' + 'To run cosine similarity test, set __IDF_WEIGHTING = False' + '\033[0m')
        print('\033[90m' + 'Then rerun this test.' + '\033[0m')
    else:
        index = {
            'affection': {0: 115, 1: 58, 2: 20},
            'jealous': {0: 10, 1: 7, 2: 11},
            'gossip': {0: 2, 1: 0, 2: 6},
            'wuthering': {0: 0, 1: 0, 2: 38}}
        
        result = __length_norm('affection', 0, index)
        assert abs(result - 0.789) < 0.01, '__length_norm(affection,0) must be about 0.78, result=' + str(result)
        result = __length_norm('jealous', 0, index)
        assert abs(result - 0.515) < 0.01, '__length_norm(jealous,0) must be about 0.515, result=' + str(result)
        result = __length_norm('gossip', 0, index)
        assert abs(result - 0.335) < 0.01, '__length_norm(gossip,0) must be about 0.335, result=' + str(result)
        result = __weighting('wuthering', 0, index)
        assert abs(result - 0) < 0.01, '__weighting() Must be about 0, result=' + str(result)

        result = __cosine(0, 1, index)
        assert abs(result - 0.94) < 0.01, '__cosine(0,1) must be about 0.94, result=' + str(result)
        result = __cosine(0, 2, index)
        assert abs(result - 0.79) < 0.01, '__cosine(0,2) must be about 0.79, result=' + str(result)
        result = __cosine(1, 2, index)
        assert abs(result - 0.69) < 0.01, '__length_norm(1,2) must be about 0.69, result=' + str(result)

        print('\033[1m\033[92m' + '100% passed' + '\033[0m')
        print('\033[90m' + 'To run tf-idf weighting similarity test, set __IDF_WEIGHTING = True' + '\033[0m')
        print('\033[90m' + 'Then rerun this test.' + '\033[0m')


if __name__ == '__main__':
    if '-t' in sys.argv:
        test()
    else:
        main()


