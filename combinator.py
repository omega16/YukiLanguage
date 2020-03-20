from lark import Lark,Token,Transformer,Tree

class Combinator:
    def __init__(self,name,patterns,expressions,identation=4):
        self.name=name
        self.patterns = patterns
        self.expressions = expressions
        self.identation = identation

    def arg_number(self):
        if self.expressions:
            return len(self.expressions[0])
        return 0

    def __add__(self,b):
        if isinstance(b,Combinator):
            if b.name != self.name:
                raise Exception("Can't add combinators of diferent names")
            else :
                return Combinator(self.name,self.patterns+b.patterns,self.expressions+b.expressions)
        else :
            raise Exception("Can't add non combinator to combinator")

    def __str__(self):
        return "Combinator(name = {}, patterns number = {} , expressions number = {})".format(
                self.name,len(self.patterns),len(self.expressions))

    def __repr__(self):
        first = "{} = \n".format(self.name)
        out = [first]
        for pattern,expr in zip(self.patterns,self.expressions):
            second = "{}{} -> ".format(" "*len(first),pattern)
            third = expr.pretty(ident_step=self.identation,translate=len(second))
            out.append("{}\n{}".format(second,third))
        return "".join(out)