#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tokenizer for Indian scripts and Roman script.

This module provides a complete tokenizer for Indian languages
including Urdu, Kashmiri and Roman script.

Copyright (c) 2015-2016 Irshad Ahmad
<irshad.bhat@research.iiit.ac.in>
"""

import io
import sys
import codecs
import argparse

from .tokenizer import Tokenizer

__version__ = '1.0'


def parse_args(args):
    prog = 'Indic-Tokenizer'
    description = 'Tokenizer for Indian Scripts'
    languages = '''hin urd ben asm guj mal pan tel tam kan ori mar
                nep bod kok kas eng'''.split()
    lang_help = 'select language (3 letter ISO-639 code) {%s}' % (
                ', '.join(languages))
    # parse command line arguments
    parser = argparse.ArgumentParser(prog=prog,
                                     description=description)
    parser.add_argument('-v',
                        '--version',
                        action='version',
                        version='%s %s' % (prog, __version__))
    parser.add_argument('-i',
                        '--input',
                        metavar='',
                        dest='infile',
                        type=str,
                        help='<input-file>')
    parser.add_argument('-s',
                        '--split-sentences',
                        dest='split_sen',
                        action='store_true',
                        help='set this flag to apply'
                             ' sentence segmentation')
    parser.add_argument('-o',
                        '--output',
                        metavar='',
                        dest='outfile',
                        type=str,
                        help='<output-file>')
    parser.add_argument('-l',
                        '--language',
                        metavar='',
                        dest='lang',
                        choices=languages,
                        default='hin',
                        help=lang_help)
    args = parser.parse_args(args)
    return args


def get_file_pointers(args):
    if args.infile:
        ifp = io.open(args.infile, encoding='utf-8')
    else:
        if sys.version_info[0] >= 3:
            ifp = codecs.getreader('utf8')(sys.stdin.buffer)
        else:
            ifp = codecs.getreader('utf8')(sys.stdin)

    if args.outfile:
        ofp = io.open(args.outfile, mode='w', encoding='utf-8')
    else:
        if sys.version_info[0] >= 3:
            ofp = codecs.getwriter('utf8')(sys.stdout.buffer)
        else:
            ofp = codecs.getwriter('utf8')(sys.stdout)
    return ifp, ofp


def main():
    # parse arguments
    args = parse_args(sys.argv[1:])
    ifp, ofp = get_file_pointers(args)

    # initialize tokenizer
    tok = Tokenizer(lang=args.lang, split_sen=args.split_sen)

    # tokenize
    for line in ifp:
        line = tok.tokenize(line)
        if args.split_sen:
            line = '\n'.join([' '.join(sen) for sen in line])
        else:
            line = ' '.join(line)
        ofp.write('%s\n' % line)

    # close files
    ifp.close()
    ofp.close()
