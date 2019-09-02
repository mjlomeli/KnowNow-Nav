# !/usr/bin/env python
"""Testing of Cell.

If the description is long, the first line should be a short summary 
that makes sense on its own, separated from the rest by a newline.
"""

import unittest
from Activity.FileManager.Cell import Cell
from pathlib import Path

PATH = Path.cwd()

__author__ = "Mauricio Lomeli"
__date__ = "8/30/2019"
__copyright__ = "Copyright 2019, KnowNow-Nav"
__maintainer__ = "Mauricio Lomeli"
__email__ = "mjlomeli@uci.edu"
__status__ = "Prototype"


class TestCell(unittest.TestCase):

    def setUp(self):
        # TODO: write what needs to be instantiated for each test
        cell = Cell()
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


if __name__ == "__main__":
    print("Testing Cell")
    unittest.main()