#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys

from testtools import TestCase

from iscnlp._utils import WX


if sys.version_info[0] >= 3:
    unicode = str


class TestWX(TestCase):
    def setUp(self):
        super(TestWX, self).setUp()
        self.languages = "hin ben guj mal pan tel tam kan ori".split()
        pwd = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.abspath('%s/../../tokenizer/tests' % pwd)

    def test_wx(self):
        for lang in self.languages:
            utf2wx = WX(order='utf2wx', lang=lang).utf2wx
            wx2utf = WX(order='wx2utf', lang=lang).wx2utf
            with io.open('%s/%s.txt' % (self.file_path, lang),
                         encoding='utf-8') as fp:
                for line in fp:
                    wx_text = utf2wx(line)
                    utf_text = wx2utf(wx_text)
                    # Dummy Assertions
                    self.assertIsInstance(wx_text, unicode)
                    self.assertIsInstance(utf_text, unicode)
