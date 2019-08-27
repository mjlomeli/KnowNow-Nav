# !/usr/bin/env python

"""KnowNow

If the description is long, the first line should be a short summary of KnowNowNav.py
that makes sense on its own, separated from the rest by a newline.
"""

from pathlib import Path
import sys
from TestCases import testAll

__DATA = Path.cwd() / Path('Data')

__author__ = ["Mauricio Lomeli", "Shiyu Qiu", "Jennifer Kwon", "Anne Wang",
              "Derek Eijansantos", "Dhruv Seth", "Niva Ranavat", "Matthew Cleveland"]
__date__ = "8/22/2019"
__credits__ = ["Rebecca Zhuo, Smruti Vidwans"]
__license__ = "MIT"
__version__ = "0.0.0.1"
__maintainer__ = "Mauricio Lomeli"
__email__ = "mjlomeli@uci.edu"
__status__ = "Prototype"

# TODO: This is the main file to run everyone's code.
# TODO: This will combine everyone's material and should
# TODO: be the only file anyone should ever see.


def main():
    pass


def __reset():
    for file in __DATA.iterdir():
        if '.pickle' in file.name:
            file.unlink()


def testKnowNow():
    pass


if __name__ == '__main__':
    if '-r' in sys.argv:
        __reset()
    if '-t' in sys.argv:
        test()



    main()
