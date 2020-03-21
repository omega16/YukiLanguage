"""
All stuff related to variables
"""

from types_ import Type
from Lark import Token
from scopes import Scope


class VariableError(Exception):
    """
    parent of all variables error
    """

class VariableTokenMustBeLarkToken(VariableError):
    pass

class VariableTypeMustBeType(ValueError):
    pass

class VariableScopeMustBeScope(ValueError):
    pass


class Variable:
    """
    All variables must have this info
    """
    def __init__(self, token, type_, scope):
        if isinstance(token, Token):
            self.token = token
        else:
            raise VariableTokenMustBeLarkToken
        if isinstance(type_, Type):
            self.type = type_
        else:
            raise VariableTypeMustBeType
        if isinstance(scope, Scope):
            self.scope = scope
        else:
            raise VariableScopeMustBeScope

    def __str__(self):
        return "(Var({},{}))".format(str(self.token), str(self.type))

    def __repr__(self):
        return "(Var({},{},{}))".format(repr(self.token), repr(self.type), repr(self.scope))
