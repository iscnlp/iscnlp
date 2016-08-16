#!/usr/bin/env python

from .indic_tokenizer import IndicTokenizer
from .roman_tokenizer import RomanTokenizer


class Tokenizer():
    def __init__(self, lang='hin', split_sen=False):
        if lang == 'eng':
            self.tok = RomanTokenizer(split_sen=split_sen)
        else:
            self.tok = IndicTokenizer(lang=lang, split_sen=split_sen)

    def tokenize(self, sentence):
        return self.tok.tokenize(sentence)
