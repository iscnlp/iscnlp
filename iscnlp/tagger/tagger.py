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


class Tagger():
    def __init__(self, lang='hin'):
        self.lang = lang
        self.embd = TagEmbedder(lang=lang)
        with open('%s/%s_pos.pkl' % (MODEL_DIR, lang), 'rb') as fp:
            if PV >= 3:
                self.model = pickle.load(fp, encoding='latin1')
            else:
                self.model = pickle.load(fp)
        if lang in ['hin']:
            self.to_wx = WX(order='utf2wx', lang=lang).utf2wx

    def tag(self, sequence):
        if self.lang in ['hin']:
            wx_sequence = list(map(self.to_wx, sequence))
            feat_vec = self.embd.get_feats(wx_sequence)
        else:
            feat_vec = self.embd.get_feats(sequence)
        tags = self.model.predict(feat_vec)
        return list(zip(sequence, tags))
