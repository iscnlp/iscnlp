#!/usr/bin/env python
# -*- coding=utf-8 -*-

from __future__ import (division, unicode_literals)

import re

from .base import BaseTokenizer


class RomanTokenizer(BaseTokenizer):
    def __init__(self, split_sen=False):
        super(RomanTokenizer, self).__init__(split_sen)
        # precompile regexes
        self.fit()

    def fit(self):
        # seperate "," outside
        self.notanumc = re.compile('([^0-9]),')
        self.cnotanum = re.compile(',([^0-9])')
        # split contractions right (both "'" and "’")
        self.numcs = re.compile("([0-9])'s")
        self.naca = re.compile(
            "([^a-zA-Z0-9\u0080-\u024f])'([a-zA-Z\u0080-\u024f])")
        # split hyphens
        self.hypheninnun = re.compile('(-?[0-9]-+[0-9]-?){,}')
        self.ch_hyp_noalnum = re.compile('(.)-([^a-zA-Z0-9])')
        self.noalnum_hyp_ch = re.compile('([^a-zA-Z0-9])-(.)')
        # split sentences
        if self.split_sen:
            self.splitsenr1 = re.compile(' ([.?]) ([A-Z])')
            self.splitsenr2 = re.compile(' ([.?]) ([\'"\(\{\[< ]+) ([A-Z])')
            self.splitsenr3 = re.compile(
                ' ([.?]) ([\'"\)\}\]> ]+) ([A-Z])')

    def tokenize(self, text):
        # unmask emoticons and urls
        text = self.mask_emos_urls(text)
        # normalize unicode punctituation
        text = self.normalize_punkt(text)
        # universal tokenization
        text = self.base_tokenize(text)
        # seperate "," outside
        text = self.notanumc.sub(r'\1 , ', text)
        text = self.cnotanum.sub(r' , \1', text)
        # split contractions right (both "'" and "’")
        text = self.nacna.sub(r"\1 ' \2", text)
        text = self.naca.sub(r"\1 ' \2", text)
        text = self.acna.sub(r"\1 ' \2", text)
        text = self.aca.sub(r"\1 '\2", text)
        text = self.numcs.sub(r"\1 's", text)
        text = text.replace("''", " ' ' ")
        # split dots at word beginings
        text = re.sub(r' (\.+)([^0-9])', r' \1 \2', text)
        # seperate out hyphens
        text = self.multihyphen.sub(
            lambda m: r'%s' % (' '.join(m.group(1))),
            text)
        text = self.hypheninnun.sub(
            lambda m: r'%s' % (m.group().replace('-', ' - ')),
            text)
        text = self.ch_hyp_noalnum.sub(r'\1 - \2', text)
        text = self.noalnum_hyp_ch.sub(r'\1 - \2', text)
        # handle non-breaking prefixes
        text = self.tokenize_prefixes(text)
        # restore multi-dots
        text = self.restoredots.sub(lambda m: r'.%s' %
                                    ('.' * int((len(m.group(2)) / 3))),
                                    text)
        # unmask emoticons and urls
        text = self.unmask_emos_urls(text)
        # split sentences
        if self.split_sen:
            text = self.splitsenr1.sub(r' \1\n\2', text)
            text = self.splitsenr2.sub(r' \1\n\2 \3', text)
            text = self.splitsenr3.sub(r' \1 \2\n\3', text)

        return text
