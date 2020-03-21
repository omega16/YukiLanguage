"""
Tool to test the othert part of module easy.
"""
from parser import Parser, SpineTransform
from console import Console


def test():
    """
    Just the stantandar test
    """
    with open("grammar.lk", "r") as grammar_file:
        grammar = grammar_file.read()
    parser = Parser(grammar, transformer=SpineTransform)
    promt = Console(parser,
                    init_msg="Starting test console", max_line_break=1,
                    history=".history", max_history=50, history_out=".history")
    promt.start()

if __name__ == '__main__':
    test()
