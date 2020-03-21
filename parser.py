"""
All related to parsing and shaping
"""

import logging
from trees import BTree
from combinator import Combinator
from lark import Lark, Token, Transformer, Tree

logging.basicConfig(level=logging.DEBUG)




class SpineTransform(Transformer):
    """
    Lark transformer, it makes the parser input to be a "Spine" tree.
    """

    def application(args):
        name = args[0]
        node = BTree(None, None, BTree(name), BTree(args[1]))
        for arg in args[2:]:
            node = BTree(None, None, node, BTree(arg))
        return node

    def definition(args):
        name = args[0]
        patterns = args[1:-1]
        expr = args[-1]
        out = Combinator(name, [patterns], [expr])
        return repr(out)

    def program(args):
        return args



class Parser:
    """
    Wrapper for Lark parser
    """

    def __init__(self, grammar, start="program", transformer=None):
        self.parser = Lark( grammar,
                            parser='lalr',
                            debug=True,
                            start=start,
                            maybe_placeholders=True,
                            transformer=transformer)

    def parse(self, text):
        return self.parser.parse(text)
