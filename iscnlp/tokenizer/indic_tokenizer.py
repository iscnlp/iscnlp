#!/usr/bin/env python
# -*- coding=utf-8 -*-

from __future__ import division, unicode_literals

import re

from .base import BaseTokenizer


class IndicTokenizer(BaseTokenizer):
    def __init__(self, lang='hin', split_sen=False):
        super(IndicTokenizer, self).__init__(split_sen)
        self.lang = lang
        self.urd = lang in ['urd', 'kas']
        if lang == 'asm':
            self.lang = 'ben'
        if lang in ["mar", "nep", "bod", "kok"]:
            self.lang = 'hin'
        # precompile regexes
        self.fit()

    def fit(self):
        if self.urd:
            # keep multiple dots (urdu-dots) together
            self.multidot_urd = re.compile('(\u06d4\u06d4+)([^\u06d4])')
        else:
            # keep multiple purna-viram together
            self.multiviram = re.compile('(\u0964\u0964+)([^\u0964])')
            # keep multiple purna deergh-viram together
            self.multidviram = re.compile('(\u0965\u0965+)([^\u0965])')
        # split contractions right (both "'" and "’")
        self.numcs = re.compile("([0-9\u0966-\u096f])'s")
        self.naca = re.compile(
            "([^a-zA-Z0-9\u0966-\u096f\u0080-\u024f])"
            "'([a-zA-Z\u0080-\u024f])")
        # restore multi-dots
        if self.urd:
            self.restoreudots = re.compile(r'(DOTU)(\1*)MULTI')
        else:
            self.restoreviram = re.compile(r'(PNVM)(\1*)MULTI')
            self.restoredviram = re.compile(r'(DGVM)(\1*)MULTI')
        # split sentences
        if self.urd:
            self.splitsenur1 = re.compile(
                ' ([.?\u06d4]) '
                '([\u0617-\u061a\u0620-\u065f\u066e-\u06d3'
                '\u06d5\u06fa-\u06ffA-Z\(\{\[<])')
            self.splitsenur2 = re.compile(
                ' ([.?\u06d4]) ([\)\}\]\'"> ]+) ')
        else:
            self.splitsenir1 = re.compile(
                ' ([|.?\u0964\u0965]) ([\u0900-\u0d7fA-Z\(\{\[<])')
            self.splitsenir2 = re.compile(
                ' ([|.?\u0964\u0965]) ([\)\}\]\'"> ]+) ')

    def normalize_punkt_ext(self, text):
        """Performs some common normalization:
          - Removal of Byte order mark, word joiner, etc.
          - Removal of ZERO_WIDTH_NON_JOINER and ZERO_WIDTH_JOINER
          - ZERO_WIDTH_SPACE and NO_BREAK_SPACE replaced by spaces
        """
        text = text.replace('\u00A0', ' ')  # NO_BREAK_SPACE
        text = text.replace('\u00AD', '')  # SOFT_HYPHEN
        text = text.replace('\u2060', '')  # WORD_JOINER
        text = text.replace('\u200A', ' ')  # H_SP
        text = text.replace('\u200B', ' ')  # ZERO_WIDTH_SPACE
        text = text.replace('\u200C', '')  # ZERO_WIDTH_NON_JOINER
        text = text.replace('\u200D', '')  # ZERO_WIDTH_JOINER
        text = text.replace('\u200E', '')  # LEFT_TO_RIGHT_MARK
        text = text.replace('\u200F', '')  # RIGHT_TO_LEFT_MARK
        text = text.replace('\uFEFF', '')  # BYTE_ORDER_MARK
        text = text.replace('\uFFFE', '')  # BYTE_ORDER_MARK_2
        return text

    def tokenize_by_script(self, text, digits, letters,
                           lang, special_ch=''):
        if lang != self.lang:
            return text
        # seperate out "," except for Indic and Ascii digits
        text = re.sub('([^0-9%s]),' % digits, r'\1 , ', text)
        text = re.sub(',([^0-9%s])' % digits, r' , \1', text)
        # separate out on Indic letters followed by non-Indic letters
        text = re.sub(
            '([%s])([^%s-])' % (letters, letters),
            r'\1 \2',
            text)
        text = re.sub(
            '([^%s-])([%s])' % (letters, letters),
            r'\1 \2',
            text)
        # seperate out Indic special chars
        if special_ch:
            text = re.sub('([%s])' % special_ch, r' \1 ', text)
        # separate out hyphens
        text = re.sub(
            '(-?[0-9%s]-+[0-9%s]-?){,}' % (digits, digits),
            lambda m: r'%s' % (m.group().replace('-', ' - ')),
            text)
        # separate out hyphens not in between alphabets
        text = re.sub(
            r'(.)-([^0-9a-zA-Z%s])' % letters,
            r'\1 - \2',
            text)
        text = re.sub(
            r'([^0-9a-zA-Z%s])-(.)' % letters,
            r'\1 - \2',
            text)
        return text

    def tokenize(self, text):
        # mask emoticons and urls
        text = self.mask_emos_urls(text)
        # normalize unicode punctituation
        text = self.normalize_punkt(text)
        text = self.normalize_punkt_ext(text)
        # universal tokenization
        text = self.base_tokenize(text)
        if self.urd:
            # keep multiple dots (urdu-dots) together
            text = self.multidot_urd.sub(lambda m: r' %sMULTI %s' % (
                'DOTU' * len(m.group(1)), m.group(2)), text)
        else:
            # keep multiple purna-viram together
            text = self.multiviram.sub(lambda m: r' %sMULTI %s' % (
                'PNVM' * len(m.group(1)), m.group(2)), text)
            # keep multiple purna deergh-viram together
            text = self.multidviram.sub(lambda m: r' %sMULTI %s' % (
                'DGVM' * len(m.group(1)), m.group(2)), text)
        # split contractions right (both "'" and "’")
        text = self.nacna.sub(r"\1 ' \2", text)
        text = self.naca.sub(r"\1 ' \2", text)
        text = self.acna.sub(r"\1 ' \2", text)
        text = self.aca.sub(r"\1 '\2", text)
        text = self.numcs.sub(r"\1 's", text)
        text = text.replace("''", " ' ' ")
        # seperate out hyphens
        text = self.multihyphen.sub(lambda m: r'%s' % ' '.join(m.group(1)),
                                    text)
        # handle non-breaking prefixes
        text = self.tokenize_prefixes(text)
        # tokenize by language script
        text = self.tokenize_by_script(text, '\u0966-\u096f',
                                       '\u0900-\u0963\u0970-\u097f', 'hin')
        text = self.tokenize_by_script(text, '\u09e6-\u09ef',
                                       '\u0980-\u09e3\u09f0-\u09ff', 'ben',
                                       special_ch='\u09f2\u09f3\u09fa\u09fb')
        text = self.tokenize_by_script(text, '\u0ae6-\u0aef',
                                       '\u0A80-\u0AE3\u0Af0-\u0Aff', 'guj',
                                       special_ch='\u0AD0\u0AF1')
        text = self.tokenize_by_script(text, '\u0d66-\u0d6f',
                                       '\u0D00-\u0D63\u0D73-\u0D7f', 'mal',
                                       special_ch='\u0d73\u0d74\u0d75')
        text = self.tokenize_by_script(text, '\u0a66-\u0a6f',
                                       '\u0A00-\u0A63\u0A70-\u0A7f', 'pan')
        text = self.tokenize_by_script(text, '\u0c66-\u0c6f',
                                       '\u0c00-\u0c63\u0c70-\u0c7f', 'tel',
                                       special_ch='\u0c78-\u0c7f')
        text = self.tokenize_by_script(text, '\u0be6-\u0bef',
                                       '\u0B80-\u0Be3\u0Bf3-\u0Bff', 'tam',
                                       special_ch='\u0bd0\u0bf3-\u0bff')
        text = self.tokenize_by_script(text, '\u0ce6-\u0cef',
                                       '\u0C80-\u0Ce3\u0Cf1-\u0Cff', 'kan')
        text = self.tokenize_by_script(text, '\u0b66-\u0b6f',
                                       '\u0B00-\u0B63\u0B70-\u0B7f', 'ori',
                                       special_ch='\u0B72-\u0B77')
        if self.urd:
            # seperate out urdu full-stop (۔)
            text = re.sub('([\u0600-\u06ff])(\u06d4 )', r'\1 \2', text)
            text = re.sub('( \u06d4)([\u0600-\u06ff])', r'\1 \2', text)
            # seperate out Urdu comma i.e., "،" except for Urdu digits
            text = re.sub(
                '([^0-9\u0660-\u0669\u06f0-\u06f9])(\u060C)',
                r'\1 \2 ',
                text)
            text = re.sub(
                '(\u060C)([^0-9\u0660-\u0669\u06f0-\u06f9])',
                r' \1 \2',
                text)
            # separate out on Urdu letters followed by non-Urdu letters
            # and vice-versa
            text = re.sub(
                '([\u0617-\u061a\u0620-\u065f\u066e-\u06d3\u06d5'
                '\u06fa-\u06ff\ufe70-\ufeff\ufb50-\ufdff])'
                '([^\u0617-\u061a\u0620-\u065f\u066e-\u06d3\u06d5'
                '\u06fa-\u06ff\ufe70-\ufeff\ufb50-\ufdff'
                '\u06d4\u066b-])',
                r'\1 \2',
                text)
            text = re.sub(
                '([^\u0617-\u061a\u0620-\u065f\u066e-\u06d3\u06d5'
                '\u06fa-\u06ff\ufe70-\ufeff\ufb50-\ufdff'
                '\u06d4\u066b-])'
                '([\u0617-\u061a\u0620-\u065f\u066e-\u06d3\u06d5\u06fa-\u06ff'
                '\ufe70-\ufeff\ufb50-\ufdff])',
                r'\1 \2',
                text)
            # separate out on every other special character
            text = re.sub(
                '([\u0600-\u0607\u0609\u060a\u060d\u060e\u0610-\u0614'
                '\u061b-\u061f\u066a\u066c\u066d\u06dd\u06de\u06e9])',
                r' \1 ',
                text)
            # separate out hyphens
            text = re.sub(
                '(-?[0-9\u0660-\u0669\u06f0-\u06f9]-+'
                '[0-9\u0660-\u0669\u06f0-\u06f9]-?){,}',
                lambda m: r'%s' % (m.group().replace('-', ' - ')),
                text)
            text = re.sub(
                '(.)-([^a-zA-Z\u0617-\u061a\u0620-\u065f\u066e-\u06d3'
                '\u06d5\u06fa-\u06ff\ufe70-\ufeff\ufb50-\ufdff])',
                r'\1 - \2',
                text)
            text = re.sub(
                '([^a-zA-Z\u0617-\u061a\u0620-\u065f\u066e-\u06d3\u06d5'
                '\u06fa-\u06ff\ufe70-\ufeff\ufb50-\ufdff])-(.)',
                r'\1 - \2',
                text)
        text = text.split()
        text = ' '.join(text)
        # restore multiple dots, purna virams and deergh virams
        text = self.restoredots.sub(lambda m: r'.%s' %
                                    ('.' * int((len(m.group(2))) / 3)),
                                    text)
        if self.urd:
            text = self.restoreudots.sub(lambda m: '\u06d4%s' % (
                '\u06d4' * int((len(m.group(2))) / 4)), text)
        else:
            text = self.restoreviram.sub(lambda m: '\u0964%s' % (
                '\u0964' * int((len(m.group(2))) / 4)), text)
            text = self.restoredviram.sub(lambda m: '\u0965%s' % (
                '\u0965' * int((len(m.group(2))) / 4)), text)
        # unmask emoticons and urls
        text = self.unmask_emos_urls(text)
        # split sentences
        if self.split_sen:
            if self.urd:
                text = self.splitsenur1.sub(r' \1\n\2', text)
                text = self.splitsenur2.sub(r' \1 \2\n', text)
            else:
                text = self.splitsenir1.sub(r' \1\n\2', text)
                text = self.splitsenir2.sub(r' \1 \2\n', text)
        return text
