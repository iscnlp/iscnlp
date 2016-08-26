#!/usr/bin/env python
# -*- coding=utf-8 -*-

from __future__ import (division, unicode_literals)

import re
import os


class BaseTokenizer(object):
    def __init__(self, split_sen=False):
        self.split_sen = split_sen
        file_path = os.path.dirname(os.path.abspath(__file__))

        with open('%s/data/emoticons.txt' % file_path) as fp:
            self.emoticons = set(fp.read().split())

        self.NBP = dict()
        with open('%s/data/NONBREAKING_PREFIXES' % file_path) as fp:
            for line in fp:
                if line.startswith('#'):
                    continue
                if '#NUMERIC_ONLY#' in line:
                    line = line.replace('#NUMERIC_ONLY#', '').split()[0]
                    self.NBP[line] = 2
                else:
                    self.NBP[line.strip()] = 1

        # precompile regexes
        self.base_fit()

    def base_fit(self):
        # ASCII junk characters
        self.ascii_junk = re.compile('[\x00-\x1f]')
        # Latin-1 supplementary characters
        self.latin = re.compile('([\xa1-\xbf\xd7\xf7])')
        # general unicode punctituations except "’"
        self.upunct = re.compile('([\u2012-\u2018\u201a-\u206f])')
        # unicode mathematical operators
        self.umathop = re.compile('([\u2200-\u2211\u2213-\u22ff])')
        # unicode fractions
        self.ufrac = re.compile('([\u2150-\u2160])')
        # unicode superscripts and subscripts
        self.usupsub = re.compile('([\u2070-\u209f])')
        # unicode currency symbols
        self.ucurrency = re.compile('([\u20a0-\u20cf])')
        # all "other" ASCII special characters
        self.specascii = re.compile(r'([\\!@#$%^&*()_+={\[}\]|";:<>?`~/])')
        # keep multiple dots together
        self.multidot = re.compile(r'(\.\.+)([^\.])')
        # seperate "," outside
        self.notanumc = re.compile('([^0-9]),')
        self.cnotanum = re.compile(',([^0-9])')
        # split contractions right (both "'" and "’")
        self.numcs = re.compile("([0-9])'s")
        self.aca = re.compile(
            "([a-zA-Z\u0080-\u024f])'([a-zA-Z\u0080-\u024f])")
        self.acna = re.compile(
            "([a-zA-Z\u0080-\u024f])'([^a-zA-Z\u0080-\u024f])")
        self.nacna = re.compile(
            "([^a-zA-Z\u0080-\u024f])'([^a-zA-Z\u0080-\u024f])")
        # split hyphens
        self.multihyphen = re.compile('(-+)')
        # restore multi-dots
        self.restoredots = re.compile(r'(DOT)(\1*)MULTI')

    def normalize_punkt(self, text):
        """replace unicode punctuation by ascii"""
        text = re.sub('[\u2010\u2043]', '-', text)  # hyphen
        text = re.sub('[\u2018\u2019]', "'", text)  # single quotes
        text = re.sub('[\u201c\u201d]', '"', text)  # double quotes
        return text

    def unmask_emos_urls(self, text):
        text = text.split()
        for i, token in enumerate(text):
            if token.startswith('eMoTiCoN-'):
                emo_id = int(token.split('-')[1])
                text[i] = self.emos_dict[emo_id]
            elif token.startswith('sItEuRl-'):
                url_id = int(token.split('-')[1])
                text[i] = self.url_dict[url_id]
        return ' '.join(text)

    def mask_emos_urls(self, text):
        n_e, n_u = 0, 0
        text = text.split()
        self.url_dict = dict()
        self.emos_dict = dict()
        for i, token in enumerate(text):
            if token in self.emoticons:
                text[i] = 'eMoTiCoN-%d' % n_e
                self.emos_dict[n_e] = token
                n_e += 1
            elif (token.startswith('http://') or
                  token.startswith('https://') or
                  token.startswith('www.')):
                text[i] = 'sItEuRl-%d' % n_u
                self.url_dict[n_u] = token
                n_u += 1
        text = ' '.join(text)
        text = ' %s ' % (text)
        return text

    def tokenize_prefixes(self, text):
        words = text.split()
        text_len = len(words) - 1
        text = str()
        for i, word in enumerate(words):
            if word[-1] == '.':
                dotless = word[:-1]
                if dotless.isdigit():
                    word = dotless + ' .'
                elif ('.' in dotless and re.search('[a-zA-Z]', dotless)) or \
                        self.NBP.get(dotless, 0) == 1 or \
                        (i < text_len and words[i + 1][0].islower()):
                    pass
                elif self.NBP.get(dotless, 0) == 2 and \
                        (i < text_len and words[i + 1][0].isdigit()):
                    pass
                elif i < text_len and words[i + 1][0].isdigit():
                    pass
                else:
                    word = dotless + ' .'
            text += "%s " % word
        return ' %s ' % text

    def base_tokenize(self, text):
        text = ' %s ' % (text)
        # seperate out on Latin-1 supplementary characters
        text = self.latin.sub(r' \1 ', text)
        # seperate out on general unicode punctituations except "’"
        text = self.upunct.sub(r' \1 ', text)
        # seperate out on unicode mathematical operators
        text = self.umathop.sub(r' \1 ', text)
        # seperate out on unicode fractions
        text = self.ufrac.sub(r' \1 ', text)
        # seperate out on unicode superscripts and subscripts
        text = self.usupsub.sub(r' \1 ', text)
        # seperate out on unicode currency symbols
        text = self.ucurrency.sub(r' \1 ', text)
        # remove ascii junk
        text = self.ascii_junk.sub('', text)
        # seperate out all "other" ASCII special characters
        text = self.specascii.sub(r' \1 ', text)
        # keep multiple dots together
        text = self.multidot.sub(lambda m: r' %sMULTI %s' % (
            'DOT' * len(m.group(1)), m.group(2)), text)
        return text
