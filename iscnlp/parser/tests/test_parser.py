#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from testtools import TestCase

from iscnlp import Parser

TEST_FILE = """

1	इसके	यह	pn	PRP	_	13	vmod	_	_
2	अतिरिक्त	अतिरिक्त	psp	PSP	_	1	lwg__psp	_	_
3	गुग्गुल	गुग्गुल	n	NNPC	_	4	pof__cn	_	_
4	कुंड	कुंड	n	NNP	_	8	ccof	_	_
5	,	COMMA	punc	SYM	_	4	rsym	_	_
6	भीम	भीम	n	NNPC	_	7	pof__cn	_	_
7	गुफा	गुफा	n	NNP	_	8	ccof	_	_
8	तथा	तथा	avy	CC	_	13	k1	_	_
9	भीमशिला	भीमशिला	n	NNP	_	8	ccof	_	_
10	भी	भी	avy	RP	_	9	lwg__rp	_	_
11	दर्शनीय	दर्शनीय	adj	JJ	_	12	nmod__adj	_	_
12	स्थल	स्थल	n	NN	_	13	k1s	_	_
13	हैं	है	v	VM	_	0	main	_	_
14	.	.	punc	SYM	_	13	rsym	_	_

"""


class TestParser(TestCase):
    def setUp(self):
        super(TestParser, self).setUp()
        self.parser = Parser(lang='hin')

    def test_parser(self):
        seq = TEST_FILE.strip().split('\n')
        word_seq = [x.split('\t')[1] for x in seq]
        # test static parser
        self.parser.parse(word_seq)
        # test beam parser
        self.parser.beamwidth = 2
        self.parser.parse(word_seq)
