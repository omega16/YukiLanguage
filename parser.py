from lark import Lark,Token,Transformer,Tree
import logging
logging.basicConfig(level=logging.DEBUG)

from trees import BTree
from combinator import Combinator

class SpineTransform(Transformer):

    def application(args):
        name = args[0]
        node = BTree(None,None,BTree(name),BTree(args[1]))
        for arg in args[2:]:
            node = BTree(None,None,node,BTree(arg))
        return node

    def definition(args):
        name = args[0]
        patterns = args[1:-1]
        expr = args[-1]
        out = Combinator(name,[patterns],[expr])
        return repr(out)

    def program(args):
        return args



class Parser:
    def __init__(self,grammar,start="program",transformer=None):
        self.parser = Lark(grammar, parser='lalr', debug=True,start = start,maybe_placeholders=True,transformer=transformer)

    def parse(self,text):
        return self.parser.parse(text)
