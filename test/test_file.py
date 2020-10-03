import unittest
from unittest.mock import Mock

from rpp import Element

from rppFile import *


class FileTestCase(unittest.TestCase):
    def test_file_open_not_exists(self):
        mock = Mock()
        sg.popup_error = mock
        ret = openFile('abcd.def')
        mock.assert_called_with('Could not open this file')
        self.assertIsNone(ret, msg='Return should be None')

    def test_file_open_not_rpp(self):
        mock = Mock()
        sg.popup_error = mock
        ret = openFile('test_file.py')
        mock.assert_called_with('Could not parse this file')
        self.assertIsNone(ret, msg='Return should be None')

    def test_file_open_good_rpp(self):
        mock = Mock()
        sg.popup_error = mock
        ret = openFile('test.RPP')
        mock.assert_not_called()
        self.assertIsInstance(ret, Element, msg='Return should be rpp.Element')
        printStruct(ret)

    def test_file_open_rpp_structure(self):
        mock = Mock()
        sg.popup_error = mock
        ret = openFile('test.RPP')
        self.assertEqual(ret.tag, 'REAPER_PROJECT', msg='No Reaper project found')
        children = ret.children
        self.assertTrue(len(children) == 63)  # this is an empty project


if __name__ == '__main__':
    unittest.main()
