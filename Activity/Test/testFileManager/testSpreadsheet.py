# !/usr/bin/env python
"""Testing of Spreadsheet.

If the description is long, the first line should be a short summary 
that makes sense on its own, separated from the rest by a newline.
"""

import unittest
from Activity.FileManager.Spreadsheet import Spreadsheet
from pathlib import Path

PATH = Path.cwd() / Path('Activity') / Path('Test') / Path('testFileManager')

__author__ = "Mauricio Lomeli"
__date__ = "8/30/2019"
__copyright__ = "Copyright 2019, KnowNow-Nav"
__maintainer__ = "Mauricio Lomeli"
__email__ = "mjlomeli@uci.edu"
__status__ = "Prototype"


class TestSpreadsheet(unittest.TestCase):

    def setUp(self):
        # TODO: write what needs to be instantiated for each test
        self.test_csv = Path.cwd() / Path('Activity') / Path('Test') / Path('test.csv')
        self.length, self.headers, self.dictionary = _create_csv_files(self.test_csv)
        self.sheet = Spreadsheet(self.test_csv, None)
        self.start = 0
        self.total = 0

    def test_opening(self):
        """
        Date,Open,High,Low,Close,Volume,AdjClose
        2011-06-13,164.44,164.46,162.73,163.17,5099200,163.17
        2011-06-10,164.57,164.84,162.87,163.18,4683300,163.18
        2011-06-09,165.01,165.96,164.76,164.84,4288800,164.84
        """
        self.total = 44
        self.progBar("Testing Constructor")
        # these are the file naming convention we are testing (local, local Path, Path, string path)
        files = ['test.csv', Path('test.csv'), self.test_csv, 'Activity/Test/testFileManager/test.csv']
        for file in files:
            try:
                if Path(file).exists():
                    Path(file).unlink()

                length, headers, dictionary = _create_csv_files(file)  # Creates the file we are testing.
                sheet = Spreadsheet(file, None)
                header_message = "Spreadsheet.headers isn't working accurately."
                self.assertEqual(sheet.headers, headers, header_message)
                length_message = "len(Spreadsheet) isn't working accurately."
                self.assertEqual(len(sheet), length, length_message)
                found_message = "Item must have been found in the Spreadsheet."
                self.assertTrue(sheet.has('2011-06-13'), found_message)
                self.assertTrue(sheet.has('164.44'), found_message)
                self.assertTrue(sheet.has('164.84'), found_message)
                self.assertTrue(sheet.has('163.17'), found_message)
                self.assertTrue(sheet.has('2011-06-09'), found_message)
                self.assertTrue(sheet.has('164.84'), found_message)
                self.assertTrue(sheet.has('4288800'), found_message)
                self.assertTrue(sheet.has('5099200'), found_message)
                self.assertTrue(sheet.has('AdjClose'), found_message)

                self.progBar("Testing Constructor", 11)

                if Path(file).exists():
                    Path(file).unlink()
            except Exception as e:
                if Path(file).exists():
                    Path(file).unlink()
                self.fail("Unable to open a 3x7 spreadsheet. Needs investigating.")

    def test_trunc_text(self):
        self.total = 1
        self.progBar("Testing trunc_text()")
        text = "Alice in wonderland"
        self.assertEqual(self.sheet.trunc_text(text, 2), "Al...")
        self.progBar("Testing trunc_text", 1)

    def test_headers(self):
        self.total = 1
        self.progBar("Testing headers")
        self.assertListEqual(self.sheet.headers, self.headers)
        self.progBar("Testing headers", 1)

    def test_length(self):
        self.total = 1
        self.progBar("Testing len()")
        self.assertEqual(len(self.sheet), self.length)
        self.progBar("Testing length", 1)

    def test_convert_dict(self):
        self.total = 1
        self.progBar("Testing convertToDict()")
        self.assertDictEqual(self.sheet.convertToDict(self.sheet[0]), self.dictionary)
        self.progBar("Testing convertToDict", 1)

    def test_at(self):
        self.total = 7
        self.progBar("Testing at()")
        """
        Date,Open,High,Low,Close,Volume,AdjClose
        2011-06-13,164.44,164.46,162.73,163.17,5099200,163.17
        2011-06-10,164.57,164.84,162.87,163.18,4683300,163.18
        2011-06-09,165.01,165.96,164.76,164.84,4288800,164.84
        """
        self.assertTupleEqual(self.sheet.at('2011-06-13'), tuple((0, 0)))
        self.assertTupleEqual(self.sheet.at('2011-06-10'), tuple((1, 0)))
        self.assertTupleEqual(self.sheet.at('2011-06-09'), tuple((2, 0)))
        self.assertTupleEqual(self.sheet.at('164.44'), tuple((0, 1)))
        self.assertEqual(self.sheet.at(["2011-06-13","164.44","164.46","162.73","163.17","5099200","163.17"]),0)
        self.assertEqual(self.sheet.at(["2011-06-10","164.57","164.84","162.87","163.18","4683300","163.18"]), 1)
        self.assertEqual(self.sheet.at(["2011-06-09","165.01","165.96","164.76","164.84","4288800","164.84"]), 2)
        self.progBar("Testing at()", 7)

    def test_find(self):
        self.total = 3
        self.progBar("Testing find()")
        """
        Date,Open,High,Low,Close,Volume,AdjClose
        2011-06-13,164.44,164.46,162.73,163.17,5099200,163.17
        2011-06-10,164.57,164.84,162.87,163.18,4683300,163.18
        2011-06-09,165.01,165.96,164.76,164.84,4288800,164.84
        """
        self.assertListEqual(self.sheet.find('2011-06-13'),
                             [["2011-06-13","164.44","164.46","162.73","163.17","5099200","163.17"]])
        self.assertListEqual(self.sheet.find('4288800'),
                             [["2011-06-09","165.01","165.96","164.76","164.84","4288800","164.84"]])
        self.assertListEqual(self.sheet.find('164.84'),
                             [["2011-06-10","164.57","164.84","162.87","163.18","4683300","163.18"],
                              ["2011-06-09","165.01","165.96","164.76","164.84","4288800","164.84"]])
        self.progBar("Testing find()", 3)

    def test_type(self):
        self.total = 21
        self.progBar("Testing Type")
        """
        Date,Open,High,Low,Close,Volume,AdjClose
        2011-06-13,164.44,164.46,162.73,163.17,5099200,163.17
        2011-06-10,164.57,164.84,162.87,163.18,4683300,163.18
        2011-06-09,165.01,165.96,164.76,164.84,4288800,164.84
        """
        for item in self.sheet:
            for cell in item:
                self.assertTrue(isinstance(cell, str), "Error, everything in spreadsheet must be a string.")
                self.progBar("Testing Type", 1)

    def tearDown(self):
        # TODO: write what to do after a test is finished (close files?)
        if self.test_csv.exists():
            self.test_csv.unlink()

    def progBar(self, name, increment=None):
        if increment is None:
            print(name)
            _printProgressBar(self.start, self.total, name)
        else:
            self.start += increment
            _printProgressBar(self.start, self.total, name)


def _create_csv_files(file=None, string=None):
    if file is None:
        file = 'Activity/Test/testFileManager/test.csv'
    path = Path(file)
    if path.exists():
        path.unlink()
    if string is None:
        csv_1 = """Date,Open,High,Low,Close,Volume,AdjClose
                2011-06-13,164.44,164.46,162.73,163.17,5099200,163.17
                2011-06-10,164.57,164.84,162.87,163.18,4683300,163.18
                2011-06-09,165.01,165.96,164.76,164.84,4288800,164.84
                """.replace(' ', '')
    else:
        csv_1 = string

    with open(path, 'w') as w:
        w.write(csv_1)

    dictionary = {"Date":"2011-06-13","Open":"164.44","High":"164.46",
                  "Low":"162.73","Close":"163.17","Volume":"5099200",
                  "AdjClose":"163.17"}
    length = 3
    headers = ["Date","Open","High","Low","Close","Volume","AdjClose"]
    return length, headers, dictionary


def _printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█'):
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
            print("")


def main():
    print("Testing Spreadsheet")
    import subprocess as sub
    import os
    if os.name == 'nt':
        sub.run(['python', '-m', 'unittest', 'Activity/Test/testFileManager/testSpreadsheet.py'])
    elif os.name == 'posix':
        sub.run(['python3', '-m', 'unittest', 'Activity/Test/testFileManager/testSpreadsheet.py'])
    elif os.name == 'darwin':
        sub.run(['python3', '-m', 'unittest', 'Activity/Test/testFileManager/testSpreadsheet.py'])
    else:
        message = "Tell " + str(__maintainer__) + " the test functions can't find your OS system type"
        raise (NotImplementedError, message)


if __name__ == "__main__":
    main()

