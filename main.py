#! /usr/bin/env python
#coding=utf-8
from __future__ import print_function
import sys
from py_yacc import yacc
from util import clear_text, preprocessing
from translation import *

text=preprocessing(clear_text(open('source.txt', 'r').read()))

# syntax parse
root=yacc.parse(text)
root.print_node(0)
#
# # translation
# trans(root)
# print(v_table)
t = Translate()
t.trans(root)
