#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from testtools import TestCase

from iscnlp import Tagger

TEST_FILE = """

केजरीवाल   NNP
पर  PSP
प्रहार    NN
करते VM
हुए  VAUX
अखिलेश    NNP
ने   PSP
कहा  VM
कि   CC
जब  PRP
तक  PSP
पूरे  JJ
मामले NN
की   PSP
जांच  NNC
रिपोर्ट    NN
जनता NN
के   PSP
सामने NST
नहीं  NEG
आ   VM
जाती  VAUX
,   SYM
कोई  PRP
कैसे  WQ
कह  VM
सकता VAUX
है   VAUX
कि   CC
जांच  NN
निष्पक्ष   JJ
है   VM
या   CC
नहीं  NEG
।   SYM

"""


class TestTagger(TestCase):
    def setUp(self):
        super(TestTagger, self).setUp()
        self.tagger = Tagger(lang='hin')

    def test_tagger(self):
        seq = TEST_FILE.strip().split('\n')
        word_seq = [wt.split()[0] for wt in seq]
        true_tags = [wt.split()[1] for wt in seq]
        pred_tags = [wt[1] for wt in self.tagger.tag(word_seq)]
        for t, p in zip(true_tags, pred_tags):
            self.assertEqual(t, p)
