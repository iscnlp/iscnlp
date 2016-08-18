#!/usr/bin/python

import re
import os.path
from collections import defaultdict, namedtuple

import numpy as np

from iscnlp import Tagger
from iscnlp.embedder import WordVec

MODEL_DIR = '%s/../iscnlp_data' % os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.abspath('%s/embeddings' % MODEL_DIR)


class Template(Tagger):
    def __init__(self, pwindow=2, lang='hin'):
        super(Template, self).__init__(lang, wx=True)
        node = namedtuple('leaf', ('id', 'form', 'lemma', 'ctag', 'tag',
                                   'features', 'parent', 'pparent', 'drel',
                                   'pdrel', 'left', 'right'))
        self.PAD = node(-1, '__PAD__', '__PAD__', '__PAD__', '__PAD__',
                        defaultdict(lambda: '__PAD__'), -1, -1, '__PAD__',
                        '__PAD__', [], [])
        self.pvm = WordVec().load_wordvec('%s/hin_pos.vec' % MODEL_DIR)

    def _safe_indexing(self, list_, id_):
        try:
            return list_[id_]
        except IndexError:
            return None

    def feat_template(self, nodes, stack, idx):
        n_nodes = len(nodes)
        s0 = nodes[stack[-1]] if stack else self.PAD
        s1 = self._safe_indexing(stack, -2)
        s2 = self._safe_indexing(stack, -3)
        s1 = nodes[s1] if s1 else self.PAD
        s2 = nodes[s2] if s2 else self.PAD
        if s0 is not self.PAD:
            l = self._safe_indexing(s0.left, -1)
            s0l = nodes[l] if l else self.PAD
            r = self._safe_indexing(s0.right, -1)
            s0r = nodes[r] if r else self.PAD
            l = self._safe_indexing(s0.left, -2)
            s0l2 = nodes[l] if l else self.PAD
            r = self._safe_indexing(s0.right, -2)
            s0r2 = nodes[r] if r else self.PAD
        else:
            s0l = self.PAD
            s0r = self.PAD
            s0l2 = self.PAD
            s0r2 = self.PAD

        n0 = nodes[idx] if idx < n_nodes else self.PAD
        if n0 is not self.PAD:
            l = self._safe_indexing(n0.left, -1)
            n0l = nodes[l] if l else self.PAD
            l = self._safe_indexing(n0.left, -2)
            n0l2 = nodes[l] if l else self.PAD
        else:
            n0l = self.PAD
            n0l2 = self.PAD

        if s1 is not self.PAD:
            l = self._safe_indexing(s1.left, -1)
            s1l = nodes[l] if l else self.PAD
            l = self._safe_indexing(s1.left, -2)
            s1l2 = nodes[l] if l else self.PAD
            r = self._safe_indexing(s1.right, -1)
            s1r = nodes[r] if r else self.PAD
            r = self._safe_indexing(s1.right, -2)
            s1r2 = nodes[r] if r else self.PAD
        else:
            s1l = self.PAD
            s1l2 = self.PAD
            s1r = self.PAD
            s1r2 = self.PAD

        n1 = nodes[idx + 1] if idx + 1 < n_nodes else self.PAD
        n2 = nodes[idx + 2] if idx + 2 < n_nodes else self.PAD

        vec = []
        # words
        for x in (s1r.form, s1r2.form, s1l.form, s1l2.form, s0r.form,
                  s0r2.form, s0l.form, s0l2.form, n0l2.form, n0l.form,
                  s2.form, s1.form, s0.form, n0.form, n1.form, n2.form):
            if x == '__PAD__':
                vec.extend(self.embd.wvm.syn0[-3]*.01)
            elif x == 'ROOT_F':
                vec.extend(self.embd.wvm.syn0[-2]*.01)
            elif x in self.embd.wvm.vocab:
                vec.extend(self.embd.wvm[x])
            else:
                vec.extend(self.embd.wvm.syn0[-1]*.01)
        # suffixes
        for word in (s0r.form, s0l.form, n0l.form, s0.form, n0.form):
            word = ' '.join(word)
            word = re.sub(r' ([aVYZ])', r'a', word)
            word = word.split()
            sfx = ''.join(word[-3:])
            if sfx in self.embd.c3vm.vocab:
                vec.extend(self.embd.c3vm[sfx])
            else:
                vec.extend(self.embd.c3vm.syn0[-1]*.01)
        # pos-tags
        for x in (s1r.tag, s1r2.tag, s1l.tag, s1l2.tag, s0r.tag,
                  s0r2.tag, s0l.tag, s0l2.tag, n0l2.tag, n0l.tag,
                  s2.tag, s1.tag, s0.tag, n0.tag, n1.tag, n2.tag):
            if x == '__PAD__':
                vec.extend(self.embd.c3vm.syn0[-2]*0.01)
            elif x == 'ROOT_P':
                vec.extend(self.embd.c3vm.syn0[-1]*0.01)
            else:
                vec.extend(self.pvm[x])
        # chunk-tags #TODO
        # features.extend([s1r.features['chunkId'],
        #                  s1r2.features['chunkId'],
        #                  s1l.features['chunkId'],
        #                  s1l2.features['chunkId'],
        #                  s0r.features['chunkId'],
        #                  s0r2.features['chunkId'],
        #                  s0l.features['chunkId'],
        #                  s0l2.features['chunkId'],
        #                  n0l2.features['chunkId'],
        #                  n0l.features['chunkId'],
        #                  s2.features['chunkId'],
        #                  s1.features['chunkId'],
        #                  s0.features['chunkId'],
        #                  n0.features['chunkId'],
        #                  n1.features['chunkId'],
        #                  n2.features['chunkId']):
        # dep labels #TODO
        # features.extend([s1r.pdrel, s1r2.pdrel, s1l.pdrel, s1l2.pdrel,
        #                  s0r.pdrel, s0r2.pdrel, s0l.pdrel, s0l2.pdrel,
        #                  n0l2.pdrel, n0l.pdrel, s2.pdrel, s1.pdrel,
        #                  s0.pdrel])
        return np.array(vec).reshape(1, -1)
