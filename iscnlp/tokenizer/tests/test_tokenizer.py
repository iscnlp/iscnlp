#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import six

from testtools import TestCase
from iscnlp.tokenizer import IndicTokenizer, RomanTokenizer, parse_args


class TestTokenizer(TestCase):
    def setUp(self):
        super(TestTokenizer, self).setUp()
        self.languages = "eng hin urd ben guj mal pan tel tam kan ori".split()
        self.test_dir = os.path.dirname(os.path.abspath(__file__))

    def test_tokenizer(self):
        for lang in self.languages:
            if lang == 'eng':
                tok = RomanTokenizer(split_sen=True)
            else:
                tok = IndicTokenizer(split_sen=True, lang=lang)
            with io.open('%s/%s.txt' % (self.test_dir, lang),
                         encoding='utf-8') as fp:
                for line in fp:
                    tokenized_text = tok.tokenize(line)
                    self.assertIsInstance(tokenized_text, six.text_type)

    def test_parser(self):
        parser = parse_args(['--input', 'path/to/input_file',
                             '--output', 'path/to/output_file',
                             '--language', 'kas',
                             '--split-sentences'])
        self.assertEqual(parser.infile, 'path/to/input_file')
        self.assertEqual(parser.outfile, 'path/to/output_file')
        self.assertEqual(parser.lang, 'kas')
        self.assertTrue(parser.split_sen)
