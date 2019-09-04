# !/usr/bin/env python

"""Similarity

If the description is long, the first line should be a short summary of Similarity.py
that makes sense on its own, separated from the rest by a newline.
"""

import sys
from pathlib import Path
from Activity.FileManager.Spreadsheet import Spreadsheet
from Activity.NLP.Tokenizer import Tokenizer
import pickle
from math import log10, sqrt
from heapq import nlargest

__author__ = "Mauricio Lomeli"
__credits__ = ['Prof. Mustafa Ibrahim']
__date__ = "8/22/2019"
__license__ = "MIT"
__version__ = "0.0.0.1"
__maintainer__ = "Mauricio Lomeli"
__email__ = "mjlomeli@uci.edu"
__status__ = "Prototype"

_data = Path.cwd() / Path('data') / Path('scores.pickle')
_IDF_WEIGHTING = True  # must set to True to run original program
_corpus = Spreadsheet()  # must add your file/items here like your corpus
_corp_size = len(_corpus)  # must change value
_tokenizer = Tokenizer()
_index = {}
_max_postings_size = 15  # choose maximum number of results for cosine

"""
def file():
    if not _data.exists():
        _index = _process_index()
        with open(_data, 'wb') as w:
            pickle.dump(_index, w)
        return _index
    else:
        with open(_data, 'rb') as f:
            _index = pickle.load(f)
            return _index


def query(query_list, index=file()):
    query_list = _tokenizer.keep_stop_words(query_list)
    result = {
        'index': cosine_score(query_list, index['index']),
        'category': cosine_score(query_list, index['category']),
        'cohort': cosine_score(query_list, index['cohort']),
        'query_tag': cosine_score(query_list, index['query_tag'])
    }
    return result
"""

def _prob_idf(term, index=_index):
    df_t = sum([1 for x in list(index[term].values()) if x > 0])
    diff = _corp_size - df_t
    return log10(diff / df_t) if diff > 0 else 0


def _score(term, row, index=_index):
    if isinstance(term, str) and term in index:
        tf = index[term][row] if row in index[term] else 0
        return (1 + log10(tf)) if tf > 0 else 0
    elif isinstance(term, list):
        return _weighting(term, row, index)


"""
def _score(term, row, index=_index):
    if isinstance(term, str) and term in index:
        tf = index[term][row] if row in index[term] else 0
        return (1 + log10(tf)) if tf > 0 else 0
    elif isinstance(term, list):
        score = 0
        for word in term:
            score += _score(word, row, index)
        return score
"""


def _idf(term, index=_index):
    if isinstance(term, str):
        if term in index:
            n = _corp_size
            df_t = sum([1 for x in list(index[term].values()) if x > 0])
            return log10(n / df_t) if df_t > 0 else 0
        else:
            return 0
    else:
        raise TypeError('term in _idf function must be a string.')


def _weighting(term, row, index=_index):
    if isinstance(term, str):
        if _IDF_WEIGHTING:
            return _score(term, row, index) * _idf(term, index)
        else:
            return _score(term, row, index)
    elif isinstance(term, list):
        score = 0
        for word in term:
            if _IDF_WEIGHTING:
                score += _score(word, row, index) * _idf(word, index)
            else:
                score += _score(word, row, index)
        return score
    else:
        raise TypeError('term in function _weighting must be a string or list of strings.')


def _length_norm(term, row, index=_index):
    if term in index and row in index[term]:
        d_term = _weighting(term, row, index) if _IDF_WEIGHTING else _score(term, row, index)
        if _IDF_WEIGHTING:
            d_norm = sqrt(sum([_weighting(words, row, index) ** 2 for words in index.keys()]))
        else:
            d_norm = sqrt(sum([_score(words, row, index) ** 2 for words in index.keys()]))
        if d_norm > 0:
            return d_term / d_norm
        else:
            return 0


def _cosine(row1, row2, index=_index):
    return sum([_length_norm(word, row1, index) * _length_norm(word, row2, index) for word in index.keys()])


def cosine_score(query, index=_index, max_results=_max_postings_size):
    """
    Optimized cosines efficiently with unweighted query terms
    :param query: a list of the query
    :param index: a custom index if the default isn't wanted
    :return: the Nth largest scores, where N = _max_postings_size = 15
    """
    if isinstance(query, str):
        query = [query]
    scores = [0] * _corp_size
    length = len(index[list(index.keys())[0]])
    doc_word_count = [sum([index[item][i] for item in index.keys() if index[item][i] > 0]) for i in range(length)]
    for term in query:
        w_q = _weight_query(term, query, index)
        for i in range(length):
            scores[i] += _weighting(term, i, index) * w_q
    for i in range(length):
        scores[i] = scores[i] / doc_word_count[i]
    return nlargest(_max_postings_size, list(zip(scores, [i for i in range(length)])))


def _weight_query(term, query, index=_index):
    if isinstance(query, str):
        query = [query]
    q_index = {}
    _tokenizer.open(query)
    q_tf = _tokenizer.tf

    tokens = _tokenizer.tokens
    for tok in tokens:
        if tok in q_index:
            q_index[tok][0] = q_tf[tok]
        else:
            q_index[tok] = {0: q_tf[tok]}

    return _weighting(term, 0, q_index)


def combine_tf(tf: list):
    combined = {}
    for item in tf:
        for term, freq in item.items():
            if term in combined:
                combined[term] += freq
            else:
                combined[term] = freq
    return combined


def _increment_index(index, val):
    i = {}
    for key, values in index.items():
        for key1, val2 in values.items():
            if key not in i:
                i[key] = {key1 + val: val2}
            else:
                i[key][key1 + val] = val2
    return i


def _reconstruct_index(new_start, index, keys):
    new_index = {}
    length = 0
    if len(index) > 0:
        k = list(index.values())[0]
        if k is not None:
            length = len(k)
    if length > 0:
        for key in keys:
            if key in index:
                for i, value in enumerate(index[key].values()):
                    if key not in new_index:
                        new_index[key] = {new_start + i: value}
                    else:
                        new_index[key][new_start + i] = value
            else:
                for i in range(length):
                    if key not in new_index:
                        new_index[key] = {new_start + i: 0}
                    else:
                        new_index[key][new_start + i] = 0
    else:
        return {key: {i: 0} for i, key in enumerate(keys)}
    return new_index


def _convert_index(tf):
    if tf is None or len(tf) == 0:
        return {}
    if len(tf.values()) > 1 and isinstance(list(tf.values())[0], dict):
        return tf
    else:
        return {key: {0: value} for key, value in tf.items()}


def _merge_indexes(index1, index2):
    index1 = _convert_index(index1)
    index2 = _convert_index(index2)
    start = min(list(index1.values())[0]) if len(index1) > 0 else 0
    end = max(list(index1.values())[0]) + 1 if len(index1) > 0 else 0
    if index1.keys() != index2.keys() or end == 0 and len(index2) == 0:
        keys = set(index1.keys()).union(index2.keys())
        index1 = _reconstruct_index(start, index1, keys)
        index2 = _reconstruct_index(end, index2, keys)
    for key in index1.keys():
        index1[key].update(index2[key])
    return index1



def _process_index():
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

    return None


def main():
    pass


def testSimilarity():
    if _IDF_WEIGHTING:
        index = {'antony': {0: 157, 1: 73, 2: 0, 3: 0, 4: 0, 5: 0},
                 'brutus': {0: 4, 1: 157, 2: 0, 3: 1, 4: 0, 5: 0},
                 'caesar': {0: 232, 1: 227, 2: 0, 3: 2, 4: 1, 5: 1},
                 'calpurnia': {0: 0, 1: 10, 2: 0, 3: 0, 4: 0, 5: 0},
                 'cleopatra': {0: 57, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                 'mercy': {0: 2, 1: 0, 2: 3, 3: 5, 4: 5, 5: 1},
                 'worser': {0: 2, 1: 0, 2: 1, 3: 1, 4: 1, 5: 0}}

        result = _weighting('antony', 0, index)
        assert abs(result - 4.05) < 0.01, '_weighting(antony,0) must be about 4.05, result=' + str(result)
        result = _weighting('brutus', 0, index)
        assert abs(result - 1.75) < 0.01, '_weighting(brutus,0) must be about 1.75, result=' + str(result)
        result = _weighting('caesar', 0, index)
        assert abs(result - 2.93) < 0.01, '_weighting(caesar,0) must be about 2.93, result=' + str(result)
        result = _score(['brutus', 'caesar'], 0, index)
        assert abs(result - 4.67) < 0.01, '_score([brutus,caesar],0) must be about 4.67, result=' + str(result)
        result = _weighting(['brutus', 'caesar'], 0, index)
        assert abs(result - 4.67) < 0.01, '_weighting([brutus,caesar],0) must be about 4.67, result=' + str(result)
        print('\033[1m\033[92m' + '100% passed' + '\033[0m')
        print('\033[90m' + 'To run cosine similarity test, set _IDF_WEIGHTING = False' + '\033[0m')
        print('\033[90m' + 'Then rerun this test.' + '\033[0m')
    else:
        index = {
            'affection': {0: 115, 1: 58, 2: 20},
            'jealous': {0: 10, 1: 7, 2: 11},
            'gossip': {0: 2, 1: 0, 2: 6},
            'wuthering': {0: 0, 1: 0, 2: 38}}

        result = _length_norm('affection', 0, index)
        assert abs(result - 0.789) < 0.01, '_length_norm(affection,0) must be about 0.78, result=' + str(result)
        result = _length_norm('jealous', 0, index)
        assert abs(result - 0.515) < 0.01, '_length_norm(jealous,0) must be about 0.515, result=' + str(result)
        result = _length_norm('gossip', 0, index)
        assert abs(result - 0.335) < 0.01, '_length_norm(gossip,0) must be about 0.335, result=' + str(result)
        result = _weighting('wuthering', 0, index)
        assert abs(result - 0) < 0.01, '_weighting() Must be about 0, result=' + str(result)

        result = _cosine(0, 1, index)
        assert abs(result - 0.94) < 0.01, '_cosine(0,1) must be about 0.94, result=' + str(result)
        result = _cosine(0, 2, index)
        assert abs(result - 0.79) < 0.01, '_cosine(0,2) must be about 0.79, result=' + str(result)
        result = _cosine(1, 2, index)
        assert abs(result - 0.69) < 0.01, '_length_norm(1,2) must be about 0.69, result=' + str(result)

        print('\033[1m\033[92m' + '100% passed' + '\033[0m')
        print('\033[90m' + 'To run tf-idf weighting similarity test, set _IDF_WEIGHTING = True' + '\033[0m')
        print('\033[90m' + 'Then rerun this test.' + '\033[0m')


if __name__ == '__main__':
    if '-t' in sys.argv:
        testSimilarity()
    else:
        main()
