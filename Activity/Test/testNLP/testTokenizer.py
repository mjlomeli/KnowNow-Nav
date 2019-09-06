# !/usr/bin/env python
"""Testing of Tokenizer.

If the description is long, the first line should be a short summary 
that makes sense on its own, separated from the rest by a newline.
"""

import unittest
from Activity.NLP.Tokenizer import tokenize
from pathlib import Path

PATH = Path.cwd()

__author__ = "Mauricio Lomeli"
__date__ = "8/30/2019"
__copyright__ = "Copyright 2019, KnowNow-Nav"
__maintainer__ = "Mauricio Lomeli"
__email__ = "mjlomeli@uci.edu"
__status__ = "Prototype"


class TestTokenizer(unittest.TestCase):

    def test_textA(self):
        text = "Hello how are you!??!?!"
        tokens = ['hello']
        tf = {'hello': 1}
        count = 1

        tokenizer = tokenize(text)
        self.assertListEqual(tokens, tokenizer['tokens'])
        self.assertDictEqual(tf, tokenizer['tf'])
        self.assertEqual(count, tokenizer['count'])

    def test_textB(self):
        text = "On the new page, you can select MySQL from the left drop-down box" +\
               " which automatically sets it to TCP and port 3306."
        tokens = set(['new', 'page', 'select', 'mysql', 'left', 'drop', 'box', 'automatically',
                      'set', 'tcp', 'port', '3306'])
        tf = {'new':1, 'page':1, 'select':1, 'mysql':1, 'left':1, 'drop':1, 'box':1, 'automatically':1,
                      'set':1, 'tcp':1, 'port':1, '3306':1}
        count = 12

        tokenizer = tokenize(text)
        self.assertListEqual(tokens, tokenizer['tokens'])
        self.assertDictEqual(tf, tokenizer['tf'])
        self.assertEqual(count, tokenizer['count'])

    def test_textC(self):
        text = "Hello how are you!??!?!"
        tokens = ['hello']
        tf = {'hello': 1}
        count = 1

        tokenizer = tokenize(text)
        self.assertListEqual(tokens, tokenizer['tokens'])
        self.assertDictEqual(tf, tokenizer['tf'])
        self.assertEqual(count, tokenizer['count'])

    def test_ListA(self):
        text = "Hello how are you!??!?!"
        tokens = ['hello']
        tf = {'hello': 1}
        count = 1

        tokenizer = tokenize(text)
        self.assertListEqual(tokens, tokenizer['tokens'])
        self.assertDictEqual(tf, tokenizer['tf'])
        self.assertEqual(count, tokenizer['count'])

    def test_ListB(self):
        text = "On the new page, you can select MySQL from the left drop-down box" +\
               " which automatically sets it to TCP and port 3306."
        tokens = ['new', 'page', 'select', 'mysql', 'left', 'dropdown', 'box', 'automatic']
        tf = {'hello': 1, 'name': 1, 'candice': 1}
        count = 1

        tokenizer = tokenize(text)
        self.assertListEqual(tokens, tokenizer['tokens'])
        self.assertDictEqual(tf, tokenizer['tf'])
        self.assertEqual(count, tokenizer['count'])

    def test_ListC(self):
        text = "!@#$% #$%^ ^&* *()<>?\n\n\n\n\r\r\r\r!??!?!"
        tokens = []
        tf = {}
        count = 0

        tokenizer = tokenize(text)
        self.assertListEqual(tokens, tokenizer['tokens'])
        self.assertDictEqual(tf, tokenizer['tf'])
        self.assertEqual(count, tokenizer['count'])

    def test_DictA(self):
        text = "Hello how are you!??!?!"
        tokens = ['hello']
        tf = {'hello': 1}
        count = 1

        tokenizer = tokenize(text)
        self.assertListEqual(tokens, tokenizer['tokens'])
        self.assertDictEqual(tf, tokenizer['tf'])
        self.assertEqual(count, tokenizer['count'])

    def test_DictB(self):
        text = "Hello how are you!??!?!"
        tokens = ['hello']
        tf = {'hello': 1}
        count = 1

        tokenizer = tokenize(text)
        self.assertListEqual(tokens, tokenizer['tokens'])
        self.assertDictEqual(tf, tokenizer['tf'])
        self.assertEqual(count, tokenizer['count'])

    def test_DictC(self):
        text = "Hello how are you!??!?!"
        tokens = ['hello']
        tf = {'hello': 1}
        count = 1

        tokenizer = tokenize(text)
        self.assertListEqual(tokens, tokenizer['tokens'])
        self.assertDictEqual(tf, tokenizer['tf'])
        self.assertEqual(count, tokenizer['count'])


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█'):
    """ 
    Displays a progress bar for each iteration.
    Title: Progress Bar
    Author: Benjamin Cordier
    Date: 6/10/2019
    Availability: https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    """
    if int(iteration % (total / 100)) == 0 or iteration == total or prefix is not '' or suffix is not '':
        # calculated percentage of completeness
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        # modifies the bar
        bar = fill * filledLength + '-' * (length - filledLength)
        # Creates the bar
        print('\r\t\t{} |{}| {}% {}'.format(prefix, bar, percent, suffix), end='\r')
        # Print New Line on Complete
        if iteration == total:
            print()


def main():
    print("Testing Document")
    import subprocess as sub
    import os
    if os.name == 'nt':
        sub.run(['python', '-m', 'unittest', 'Activity/Test/testNLP/testTokenizer.py'])
    elif os.name == 'posix':
        sub.run(['python3', '-m', 'unittest', 'Activity/Test/testNLP/testTokenizer.py'])
    elif os.name == 'darwin':
        sub.run(['python3', '-m', 'unittest', 'Activity/Test/testNLP/testTokenizer.py'])
    else:
        message = "Tell " + str(__maintainer__) + " the test functions can't find your OS system type"
        raise (NotImplementedError, message)


if __name__ == "__main__":
    main()
