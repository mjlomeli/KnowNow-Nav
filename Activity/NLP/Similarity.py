# !/usr/bin/env python

"""Similarity

If the description is long, the first line should be a short summary of Similarity.py
that makes sense on its own, separated from the rest by a newline.
"""

import sys
from pathlib import Path
# from Activity.FileManager.Spreadsheet import Spreadsheet
from Activity.NLP.Tokenizer import tokenize
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
__IDF_WEIGHTING = False  # must set to True to run original program
__TESTING_WEIGHTING = False
# _corpus = Spreadsheet()  # must add your file/items here like your corpus
_index = {'antony': {0: 157, 1: 73, 2: 0, 3: 0, 4: 0, 5: 0},
         'brutus': {0: 4, 1: 157, 2: 0, 3: 1, 4: 0, 5: 0},
         'caesar': {0: 232, 1: 227, 2: 0, 3: 2, 4: 1, 5: 1},
         'calpurnia': {0: 0, 1: 10, 2: 0, 3: 0, 4: 0, 5: 0},
         'cleopatra': {0: 57, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
         'mercy': {0: 2, 1: 0, 2: 3, 3: 5, 4: 5, 5: 1},
         'worser': {0: 2, 1: 0, 2: 1, 3: 1, 4: 1, 5: 0}}
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


def __prob__idf(term, index=_index):
    df_t = sum([1 for x in list(index[term].values()) if x > 0])
    corp_size = len(list(_index.values())[0]) if len(_index) > 0 else 0
    if __TESTING_WEIGHTING:
        corp_size = 37
    diff = corp_size - df_t
    return log10(diff / df_t) if diff > 0 else 0


def __score(term, row, index=_index):
    if isinstance(term, str) and term in index:
        tf = index[term][row] if row in index[term] else 0
        return (1 + log10(tf)) if tf > 0 else 0
    elif isinstance(term, list):
        return __weighting(term, row, index)


def __idf(term, index=_index, ):
    if isinstance(term, str):
        if term in index:
            n = len(list(index.values())[0]) if len(index) > 0 else 0
            if __TESTING_WEIGHTING:
                n = 37
            df_t = sum([1 for x in list(index[term].values()) if x > 0])
            return log10(n / df_t) if df_t > 0 else 0
        else:
            return 0
    else:
        raise TypeError('term in __idf function must be a string.')


def __weighting(term, row, index=_index):
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


def __length_norm(term, row, index=_index):
    if term in index and row in index[term]:
        d_term = __weighting(term, row, index) if __IDF_WEIGHTING else __score(term, row, index)
        if __IDF_WEIGHTING:
            d_norm = sqrt(sum([__weighting(words, row, index) ** 2 for words in index.keys()]))
        else:
            d_norm = sqrt(sum([__score(words, row, index) ** 2 for words in index.keys()]))
        if d_norm > 0:
            return d_term / d_norm
        else:
            return 0


def __cosine(row1, row2, index=_index):
    return sum([__length_norm(word, row1, index) * __length_norm(word, row2, index) for word in index.keys()])


def cosine_score(query, index=_index, max_results=_max_postings_size):
    """
    Optimized cosines efficiently with unweighted query terms
    :param query: a list of the query
    :param index: a custom index if the default isn't wanted
    :return: the Nth largest scores, where N = _max_postings_size = 15
    """
    if isinstance(query, str):
        query = [query]
    corp_size = len(list(_index.values())[0]) if len(_index) > 0 else 0
    if __TESTING_WEIGHTING:
        corp_size = 37
    scores = [0] * corp_size
    length = len(index[list(index.keys())[0]])
    doc_word_count = [sum([index[item][i] for item in index.keys() if index[item][i] > 0]) for i in range(length)]
    for term in query:
        w_q = __weight_query(term, query, index)
        for i in range(length):
            scores[i] += __weighting(term, i, index) * w_q
    for i in range(length):
        scores[i] = scores[i] / doc_word_count[i]
    return nlargest(max_results, list(zip(scores, [i for i in range(length)])))


def __weight_query(term, query, index=_index):
    if isinstance(query, str):
        query = [query]
    q_index = {}
    tokenizer = tokenize(query)
    tf = tokenizer['tf']
    tokens = tokenizer['tokens']
    for tok in tokens:
        if tok in q_index:
            q_index[tok][0] = tf[tok]
        else:
            q_index[tok] = {0: tf[tok]}

    return __weighting(term, 0, q_index)


def __increment_index(index, val):
    i = {}
    for key, values in index.items():
        for key1, val2 in values.items():
            if key not in i:
                i[key] = {key1 + val: val2}
            else:
                i[key][key1 + val] = val2
    return i


def __reconstruct_index(new_start, index, keys):
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


def __convert_index(tf):
    if tf is None or len(tf) == 0:
        return {}
    if len(tf.values()) > 1 and isinstance(list(tf.values())[0], dict):
        return tf
    else:
        return {key: {0: value} for key, value in tf.items()}


def __merge_indexes(index1, index2):
    if len(index1) == 0 and len(index2) > 0:
        return index2
    if len(index2) == 0 and len(index1) > 0:
        return index1
    index1 = __convert_index(index1)
    index2 = __convert_index(index2)
    start = min(list(index1.values())[0]) if len(index1) > 0 else 0
    end = max(list(index1.values())[0]) + 1 if len(index1) > 0 else 0
    if index1.keys() != index2.keys() or end == 0 and len(index2) == 0:
        keys = set(index1.keys()).union(index2.keys())
        index1 = __reconstruct_index(start, index1, keys)
        index2 = __reconstruct_index(end, index2, keys)
    for key in index1.keys():
        index1[key].update(index2[key])
    return index1


def create_index(tf):
    if isinstance(tf, dict):
        return tf
    elif isinstance(tf, list):
        if len(tf) <= 0:
            return {}
        if len(tf) > 0 and len(tf) < 2:
            return tf[0]
        else:
            merged = __merge_indexes(tf[0], tf[1])
            return __merge_indexes(merged, create_index(tf[2:]))


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


def get_docs():
    doc_0 = ' '.join(eval("(['antony'] * {}) + (['brutus'] * {}) + (['caesar'] * {}) + (['calpurnia'] * {}) + (['cleopatra'] * {}) + (['mercy'] * {}) + (['worser'] * {})".format(157, 4, 232, 0, 57, 2, 2)))
    doc_1 = ' '.join(eval("(['antony'] * {}) + (['brutus'] * {}) + (['caesar'] * {}) + (['calpurnia'] * {}) + (['cleopatra'] * {}) + (['mercy'] * {}) + (['worser'] * {})".format(73, 157, 227, 10, 0, 0, 0)))
    doc_2 = ' '.join(eval("(['antony'] * {}) + (['brutus'] * {}) + (['caesar'] * {}) + (['calpurnia'] * {}) + (['cleopatra'] * {}) + (['mercy'] * {}) + (['worser'] * {})".format(0, 0, 0, 0, 0,3, 1)))
    doc_3 = ' '.join(eval("(['antony'] * {}) + (['brutus'] * {}) + (['caesar'] * {}) + (['calpurnia'] * {}) + (['cleopatra'] * {}) + (['mercy'] * {}) + (['worser'] * {})".format(0, 1, 2, 0, 0,5, 1)))
    doc_4 = ' '.join(eval("(['antony'] * {}) + (['brutus'] * {}) + (['caesar'] * {}) + (['calpurnia'] * {}) + (['cleopatra'] * {}) + (['mercy'] * {}) + (['worser'] * {})".format(0, 0, 1, 0, 0, 5, 1)))
    doc_5 = ' '.join(eval("(['antony'] * {}) + (['brutus'] * {}) + (['caesar'] * {}) + (['calpurnia'] * {}) + (['cleopatra'] * {}) + (['mercy'] * {}) + (['worser'] * {})".format(0, 0, 1, 0, 0, 1, 0)))

    return [doc_0, doc_1, doc_2, doc_3, doc_4, doc_5]


def testIndex():
    post_0 = ' '.join(eval("(['antony'] * {}) + (['brutus'] * {}) + (['caesar'] * {}) + (['calpurnia'] * {}) + (['cleopatra'] * {}) + (['mercy'] * {}) + (['worser'] * {})".format(157, 4, 232, 0, 57, 2, 2)))
    post_1 = ' '.join(eval("(['antony'] * {}) + (['brutus'] * {}) + (['caesar'] * {}) + (['calpurnia'] * {}) + (['cleopatra'] * {}) + (['mercy'] * {}) + (['worser'] * {})".format(73, 157, 227, 10, 0, 0, 0)))
    post_2 = ' '.join(eval("(['antony'] * {}) + (['brutus'] * {}) + (['caesar'] * {}) + (['calpurnia'] * {}) + (['cleopatra'] * {}) + (['mercy'] * {}) + (['worser'] * {})".format(0, 0, 0, 0, 0,3, 1)))
    post_3 = ' '.join(eval("(['antony'] * {}) + (['brutus'] * {}) + (['caesar'] * {}) + (['calpurnia'] * {}) + (['cleopatra'] * {}) + (['mercy'] * {}) + (['worser'] * {})".format(0, 1, 2, 0, 0,5, 1)))
    post_4 = ' '.join(eval("(['antony'] * {}) + (['brutus'] * {}) + (['caesar'] * {}) + (['calpurnia'] * {}) + (['cleopatra'] * {}) + (['mercy'] * {}) + (['worser'] * {})".format(0, 0, 1, 0, 0, 5, 1)))
    post_5 = ' '.join(eval("(['antony'] * {}) + (['brutus'] * {}) + (['caesar'] * {}) + (['calpurnia'] * {}) + (['cleopatra'] * {}) + (['mercy'] * {}) + (['worser'] * {})".format(0, 0, 1, 0, 0, 1, 0)))

    print("post_0:" + post_0[:20] + '...')
    print("post_1:" + post_1[:20] + '...')
    print("post_2:" + post_2[:20] + '...')
    print("post_3:" + post_3[:20] + '...')
    print("post_4:" + post_4[:20] + '...')
    print("post_5:" + post_5[:20] + '...')

    print("call the tokenizer on each one:")
    print("tok0 = tokenize(post_0)['tf']")
    print("tok1 = tokenize(post_1)['tf']")
    print("tok2 = tokenize(post_2)['tf']")
    print("tok3 = tokenize(post_3)['tf']")
    print("tok4 = tokenize(post_4)['tf']")
    print("tok5 = tokenize(post_5)['tf']")
    print()

    posts = [post_0, post_1, post_2, post_3, post_4, post_5]
    tf = []
    for post in posts:
        tf.append(tokenize(post)['tf'])

    print("\nmake all tf's into a list:")
    print("[")
    print("\t" + str(tf[0]))
    print("\t" + str(tf[1]))
    print("\t" + str(tf[2]))
    print("\t" + str(tf[3]))
    print("\t" + str(tf[4]))
    print("\t" + str(tf[5]))
    print("]\n\n")
    print()

    print("Now call the create_index(tf_list)")
    print("This output is now your index.")
    print()
    idx = create_index(tf)
    print(idx)


    print()
    print()

    print("Lets see how much weight each post has:")
    print(cosine_score('antony', idx, 4))


def testSimilarity():
    if __IDF_WEIGHTING:
        index = {'antony':      {0: 157,    1: 73,  2: 0, 3: 0, 4: 0, 5: 0},
                 'brutus':      {0: 4,      1: 157, 2: 0, 3: 1, 4: 0, 5: 0},
                 'caesar':      {0: 232,    1: 227, 2: 0, 3: 2, 4: 1, 5: 1},
                 'calpurnia':   {0: 0,      1: 10,  2: 0, 3: 0, 4: 0, 5: 0},
                 'cleopatra':   {0: 57,     1: 0,   2: 0, 3: 0, 4: 0, 5: 0},
                 'mercy':       {0: 2,      1: 0,   2: 3, 3: 5, 4: 5, 5: 1},
                 'worser':      {0: 2,      1: 0,   2: 1, 3: 1, 4: 1, 5: 0}}

        result = __weighting('antony', 0, index)
        assert abs(result - 4.05) < 0.01, '__weighting(antony,0, index) must be about 4.05, result=' + str(result)
        result = __weighting('brutus', 0, index)
        assert abs(result - 1.75) < 0.01, '__weighting(brutus,0, index) must be about 1.75, result=' + str(result)
        result = __weighting('caesar', 0, index)
        assert abs(result - 2.93) < 0.01, '__weighting(caesar,0, index) must be about 2.93, result=' + str(result)
        result = __score(['brutus', 'caesar'], 0, index)
        assert abs(result - 4.67) < 0.01, '__score([brutus,caesar],0, index) must be about 4.67, result=' + str(result)
        result = __weighting(['brutus', 'caesar'], 0, index)
        assert abs(result - 4.67) < 0.01, '__weighting([brutus,caesar],0, index) must be about 4.67, result=' + str(result)
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
        testSimilarity()
    else:
        main()
