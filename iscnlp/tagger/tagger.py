#!/usr/bin/env python

import sys
import pickle
import os.path

from iscnlp._utils import WX
from iscnlp.embedder import TagEmbedder
from iscnlp.mlp import MultiLayerPerceptron

__all__ = ['MultiLayerPerceptron', 'WX', 'TagEmbedder']

PV = sys.version_info[0]

MODEL_DIR = '%s/../iscnlp_data' % os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.abspath('%s/pos' % MODEL_DIR)


class Tagger(object):
    def __init__(self, lang='hin', wx=False):
        self.lang = lang
        self.embd = TagEmbedder(lang=lang)
        self.wxp = not wx and lang in ['hin']
        with open('%s/%s_pos.pkl' % (MODEL_DIR, lang), 'rb') as fp:
            if PV >= 3:
                self.model = pickle.load(fp, encoding='latin1')
            else:
                self.model = pickle.load(fp)
        if self.wxp:
            self.to_wx = WX(order='utf2wx', lang=lang).utf2wx

    def tag(self, sequence):
        if self.wxp:
            wx_sequence = list(map(self.to_wx, sequence))
            feat_vec = self.embd.get_feats(wx_sequence)
        else:
            feat_vec = self.embd.get_feats(sequence)
        tags = self.model.predict(feat_vec)
        return list(zip(sequence, tags))
