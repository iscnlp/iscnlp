#!/usr/env python

import sys
import heapq
import pickle
import os.path
from collections import namedtuple, defaultdict as dfd

import numpy as np
from six.moves import xrange

from iscnlp._utils import WX
from .arceager import ArcEager
from .template import Template
from .pseudo_projectivity import deprojectivize

PV = sys.version_info[0]

MODEL_DIR = '%s/../iscnlp_data' % os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.abspath('%s/parse' % MODEL_DIR)


class Configuration:

    def __init__(self, nodes=[]):
        self.stack = []
        self.score = 0.0
        self.b0 = 1
        self.nodes = nodes


class Parser(ArcEager):

    def __init__(self, beamwidth=1, lang='hin'):
        self.leaf = namedtuple('leaf',
                               ['id', 'form', 'lemma', 'ctag', 'tag',
                                'features', 'parent', 'pparent', 'drel',
                                'pdrel', 'left', 'right'])
        self.transitions = {
            'SHIFT': 0,
            'LEFTARC': 1,
            'RIGHTARC': 2,
            'REDUCE': 3
        }
        self.beamwidth = beamwidth
        self.template = Template(lang=lang)
        with open('%s/%s_parse.pkl' % (MODEL_DIR, lang), 'rb') as fp:
            if PV >= 3:
                self.clf = pickle.load(fp, encoding='latin1')
            else:
                self.clf = pickle.load(fp)
        self.wxp = lang in ['hin']
        if self.wxp:
            self._to_wx = WX(order='utf2wx', lang=lang).utf2wx
        self.clf.classes_ = [x.split('_', 1) for x in self.clf.classes_]

    def create_beam_items(self, beam):
        beam_items = []
        for b in xrange(len(beam)):
            config = beam[b]
            prevScore = config.score
            dense_feats = self.template.feat_template(config.nodes,
                                                      config.stack,
                                                      config.b0)
            pr_scores = self.clf.predict_proba(dense_feats)[0]
            pr_scores = np.log(pr_scores)
            predictions = zip(pr_scores, self.clf.classes_)
            valid_trans = self.get_valid_transitions(config)
            for score, (action, label) in predictions:
                if self.transitions[action] in valid_trans:
                    next_transition = valid_trans[self.transitions[action]]
                    heapq.heappush(
                        beam_items,
                        (prevScore + score, b, next_transition, label))
                    if len(beam_items) > self.beamwidth:
                        heapq.heappop(beam_items)
        return beam_items

    def clone(self, config):
        new_config = Configuration()
        new_config.stack = config.stack[:]
        new_config.score = config.score
        new_config.b0 = config.b0
        new_config.nodes = []
        for node in config.nodes:
            newnode = self.leaf._make([node.id,
                                       node.form,
                                       node.lemma,
                                       node.ctag,
                                       node.tag,
                                       node.features.copy(),
                                       node.parent,
                                       node.pparent,
                                       node.drel,
                                       node.pdrel,
                                       node.left[:],
                                       node.right[:]])
            new_config.nodes.append(newnode)
        return new_config

    def static_parse(self, nodes):
        """Parses sentence incrementally till all the words are
        consumed and only root node is left.
        """
        config = Configuration(nodes)
        while not self.isFinalState([config]):
            dense_feats = self.template.feat_template(config.nodes,
                                                      config.stack,
                                                      config.b0)
            pr_scores = self.clf.predict_proba(dense_feats)[0]
            predictions = sorted(zip(pr_scores, self.clf.classes_),
                                 reverse=True)
            valid_trans = self.get_valid_transitions(config)
            for score, (action, label) in predictions:
                if self.transitions[action] in valid_trans:
                    next_transition = valid_trans[self.transitions[action]]
                    next_transition(config, label)
                    break
        return nodes

    def beam_parse(self, nodes):
        beam = [Configuration(nodes)]
        while not self.isFinalState(beam):
            new_beam = []
            beam_items = self.create_beam_items(beam)
            for b_item in beam_items:
                b = b_item[1]  # beam-item number
                score = b_item[0]  # beam-item score
                label = b_item[3]  # beam-item label
                action = b_item[2]  # beam-item action
                current_config = beam[b]
                new_config = self.clone(current_config)
                action(new_config, label)
                new_config.score = score
                new_beam.append(new_config)
            beam = new_beam
        return max(beam, key=lambda b: b.score).nodes

    def dependency_graph(self, tokens):
        leaf = namedtuple('leaf', ['id', 'form', 'lemma', 'ctag', 'tag',
                                   'features', 'parent', 'pparent', 'drel',
                                   'pdrel', 'left', 'right'])
        yield leaf._make([0, 'ROOT_F', 'ROOT_L', 'ROOT_C', 'ROOT_P',
                          dfd(lambda: '__PAD__'), -1, -1, '_', '__PAD__',
                          [], []])
        tags = self.template.tag(tokens)
        tags = [wt[1] for wt in tags]
        for idx, (word, pos) in enumerate(zip(tokens, tags)):
            yield leaf._make([idx + 1, word, word, pos, pos,
                              dfd(lambda: '__PAD__'), -1, -1, '_', '__PAD__',
                              [], []])
        yield leaf._make([0, 'ROOT_F', 'ROOT_L', 'ROOT_C', 'ROOT_P',
                          dfd(lambda: '__PAD__'), -1, -1, '_', '__PAD__',
                          [], []])

    def parse(self, sequence):
        if self.wxp:
            wx_sequence = list(map(self._to_wx, sequence))
            nodes = list(self.dependency_graph(wx_sequence))
        else:
            nodes = list(self.dependency_graph(sequence))
        if self.beamwidth > 1:
            nodes = self.beam_parse(nodes)
        else:
            nodes = self.static_parse(nodes)
        nodes = deprojectivize(nodes[1: -1])
        tree = []
        for i, node in enumerate(nodes):
            if self.wxp:
                node = node._replace(form=sequence[i], lemma=sequence[i])
            pdrel = node.pdrel.strip("%")
            tree.append([str(node.id), node.form, node.lemma, node.tag,
                         node.tag, '_', str(node.pparent), pdrel, "_", "_"])
        return tree
