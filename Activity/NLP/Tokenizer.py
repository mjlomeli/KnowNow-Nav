# !/usr/bin/env python

"""Tokenizer

If the description is long, the first line should be a short summary of tokenizer.py
that makes sense on its own, separated from the rest by a newline.
"""

import re
import nltk
import string

__author__ = "Mauricio Lomeli"
__date__ = "8/22/2019"
__license__ = "MIT"
__version__ = "0.0.0.1"
__maintainer__ = "Mauricio Lomeli"
__email__ = "mjlomeli@uci.edu"
__status__ = "Prototype"

__lemma = nltk.WordNetLemmatizer()
__stop_words = set(nltk.corpus.stopwords.words('english'))
__pattern = re.compile(r"[a-zA-Z]{3,15}")
__with_stop = re.compile(r'[a-zA-Z]+[' + string.punctuation + ']*')
__table = str.maketrans('', '', string.punctuation + '\r\n')
__tags_list = []


def tokenize(content):
    """
    Takes in a dictionary with headers and the row of the patient insights.
    """
    tags = []
    if content is not None:
        if isinstance(content, dict):
            elements = list(content.keys()) + list(content.values())
        elif isinstance(content, list):
            elements = content
        elif isinstance(content, str):
            elements = [content]
    return __assemble(elements, tags)


def __filter_pos_tags(text_list):
    result = []
    text_list = __with_stop.findall(' '.join(text_list))
    text_list = [text.translate(__table).strip().lower() for text in text_list]
    post_tags = nltk.pos_tag(text_list)
    for term, grammar in post_tags:
        if len(term) > 2 and len(term) < 20 and term not in __stop_words:
            result.append((term, grammar))
    return result


def __filter_text(text):
    if text is not None:
        s = text.replace('\n', ' ').replace('\r\\', ' ').replace('\r', ' ')
        s = s.split(' ')
        return [word for word in s if string != '']
    else:
        return []


def __assemble(elements, tags):
    words = set([])
    data = {'count': 0, 'tags': [], 'tf': {}, 'tokens': set([])}
    if elements is not None:
        for text in elements:
            text_list = __filter_text(text)
            gram = __filter_pos_tags(text_list)
            if len(gram) > 0:
                for pos in gram:
                    root_word = __tokenizeWord(pos[0], pos[1])
                    words.add(root_word)
                    if root_word in data['tf']:
                        data['tf'][root_word] += 1
                    else:
                        data['tf'][root_word] = 1
                    data['count'] += 1
        data['tokens'] = words
    return data


def __tokenizeWord(word, grammar):
    if word is not None and word not in __stop_words and len(word) > 2:
        if grammar is None:
            return __lemma.lemmatize(word)
        elif grammar.lower().startswith('j'):  # adjectives
            return __lemma.lemmatize(word, 'a')
        elif grammar.lower().startswith('v'):  # verbs
            return __lemma.lemmatize(word, 'v')
        elif grammar.lower().startswith('n'):  # nouns
            return __lemma.lemmatize(word, 'n')
        elif grammar.lower().startswith('r'):  # adverbs
            return __lemma.lemmatize(word, 'r')
        else:
            return __lemma.lemmatize(word)
    else:
        return None


def __keep_stop_words(query):
    if query is not None:
        grammar = nltk.pos_tag(__with_stop.findall(query.lower()))
        return [__tokenizeWord(pair[0], pair[1]) for pair in grammar if pair[0] not in __stop_words]
    else:
        return ['']

