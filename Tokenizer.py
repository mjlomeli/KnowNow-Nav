# !/usr/bin/env python

"""Tokenizer

If the description is long, the first line should be a short summary of tokenizer.py
that makes sense on its own, separated from the rest by a newline.
"""

from pathlib import Path
import re
import nltk
import string

PATH = Path.cwd()

__author__ = "Mauricio Lomeli"
__date__ = "8/22/2019"
__license__ = "MIT"
__version__ = "0.0.0.1"
__maintainer__ = "Mauricio Lomeli"
__email__ = "mjlomeli@uci.edu"
__status__ = "Prototype"

__dict_text = 'insights'


class Tokenizer:

    def __init__(self):
        self.__lemma = nltk.WordNetLemmatizer()
        self.__stop_words = set(nltk.corpus.stopwords.words('english'))
        self.__pattern = re.compile(r"[a-zA-Z]{3,15}")
        self.__with_stop = re.compile(r'[a-zA-Z]+[' + string.punctuation + ']*')
        self.__table = str.maketrans('', '', string.punctuation + '\r\n')

        self.__elements = None
        self.raw_text = None
        self.tf = {}
        self.count = 0
        self.tokens = []
        self.tags = []

    def __filter_pos_tags(self, text_list):
        result = []
        text_list = self.__with_stop.findall(' '.join(text_list))
        text_list = [text.translate(self.__table).strip().lower() for text in text_list]
        post_tags = nltk.pos_tag(text_list)
        for term, grammar in post_tags:
            if len(term) > 2 and len(term) < 20 and term not in self.__stop_words:
                result.append((term, grammar))
        return result

    def __filter_text(self, text):
        if text is not None:
            s = text.replace('\n', ' ').replace('\r\\', ' ').replace('\r', ' ')
            s = s.split(' ')
            return [word for word in s if string != '']
        else:
            return []

    def __start(self):
        words = set([])
        data = {'count': 0, 'tokens': set([]), 'tf': {}}
        if self.__elements is not None:
            for text in self.__elements:
                text_list = self.__filter_text(text)
                gram = self.__filter_pos_tags(text_list)
                if len(gram) > 0:
                    for pos in gram:
                        base = self.__tokenizeWord(pos[0], pos[1])
                        words.add(base)
                        if base in data['tf']:
                            self.tf[base] += 1
                        else:
                            self.tf[base] = 1
                        self.count += 1
            self.tokens = list(words)

    def __tokenizeWord(self, word, grammar):
        if word is not None and word not in self.__stop_words and len(word) > 2:
            if grammar is None:
                return self.__lemma.lemmatize(word)
            elif grammar.lower().startswith('j'):  # adjectives
                return self.__lemma.lemmatize(word, 'a')
            elif grammar.lower().startswith('v'):  # verbs
                return self.__lemma.lemmatize(word, 'v')
            elif grammar.lower().startswith('n'):  # nouns
                return self.__lemma.lemmatize(word, 'n')
            elif grammar.lower().startswith('r'):  # adverbs
                return self.__lemma.lemmatize(word, 'r')
            else:
                return self.__lemma.lemmatize(word)
        else:
            return None

    def keep_stop_words(self, query):
        if query is not None:
            grammar = nltk.pos_tag(self.__with_stop.findall(query.lower()))
            return [self.__tokenizeWord(pair[0], pair[1]) for pair in grammar if pair[0] not in self.__stop_words]
        else:
            return ['']

    def open(self, sheet):
        """
        Takes in a dictionary with headers and the row of the patient insights.
        """
        self.tf = {}
        self.count = 0
        self.tokens = []
        self.tags = []
        if sheet is not None:
            if isinstance(sheet, dict):
                self.raw_text = sheet[self.__dict_text]
                self.__elements = sheet[self.__dict_text].split('\n')
                self.tags = [sheet[header] for header in self.__tag_list]
            elif isinstance(sheet, list):
                print(sheet)
                self.__elements = sheet
                self.tags = None
                self.raw_text = ' '.join(sheet)
            elif isinstance(sheet, str):
                self.raw_text = sheet
                self.__elements = [sheet]
                self.tags = None
        self.__start()
