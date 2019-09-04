# !/usr/bin/env python
"""Testing of Document.

If the description is long, the first line should be a short summary 
that makes sense on its own, separated from the rest by a newline.
"""

import unittest
#from Activity.NLP.Document import Document
from pathlib import Path

PATH = Path.cwd()

__author__ = "Mauricio Lomeli"
__date__ = "8/30/2019"
__copyright__ = "Copyright 2019, KnowNow-Nav"
__maintainer__ = "Mauricio Lomeli"
__email__ = "mjlomeli@uci.edu"
__status__ = "Prototype"


class TestDocument(unittest.TestCase):

    def setUp(self):
        # TODO: write what needs to be instantiated for each test
        pass

    def test_func(self):
        # TODO: write your code here
        pass

    def tearDown(self):
        # TODO: write what to do after a test is finished (close files?)
        pass


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
        sub.run(['python', '-m', 'unittest', 'Activity/Test/testNLP/testDocument.py'])
    elif os.name == 'posix':
        sub.run(['python3', '-m', 'unittest', 'Activity/Test/testNLP/testDocument.py'])
    elif os.name == 'darwin':
        sub.run(['python3', '-m', 'unittest', 'Activity/Test/testNLP/testDocument.py'])
    else:
        message = "Tell " + str(__maintainer__) + " the test functions can't find your OS system type"
        raise (NotImplementedError, message)


if __name__ == "__main__":
    main()
