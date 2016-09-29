#!/usr/bin/env python

from .indic_tokenizer import IndicTokenizer
from .roman_tokenizer import RomanTokenizer


class Tokenizer():
    def __init__(self, lang='eng', split_sen=False,
                 tweets=False, from_file=False):
        self.from_file = from_file
        self.split_sen = split_sen
        if lang in ['eng', 'spa']:
            self.tok = RomanTokenizer(lang=lang, split_sen=split_sen,
                                      tweets=tweets)
        else:
            self.tok = IndicTokenizer(lang=lang, split_sen=split_sen,
                                      tweets=tweets)

    def tokenize(self, sentence):
        if self.from_file or not self.split_sen:
            return self.tok.tokenize(sentence)
        else:
            out_sents = []
            sentences = sentence.split('\n')
            for sent in sentences:
                tok_sent = self.tok.tokenize(sent)
                out_sents.extend(tok_sent)
            return out_sents
