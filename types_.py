"""
All stuff related to types
"""

class YKTypeError(Exception):
    """
    Default error class for types
    """

class TypeMustBeOfTupleOrStr(YKTypeError):
    """
    As in the typed lambda calculus, the only types are
    atoms or constructed from the atoms
    """

class TypeProductOnlyDefinedForTypes(YKTypeError):
    """
    Have no sense on multiply type with non type
    """


class Type:
    """
    Base class for types
    """
    def __init__(self, name):
        if isinstance(name, (Type, str)):
            self.name = name
        else:
            raise TypeMustBeOfTupleOrStr("given type {}".format(type(name)))

    def __mul__(self, other):
        if isinstance(other, Type):
            if isinstance(self.name, tuple):
                if isinstance(other.name, tuple):
                    return Type(self.name+other.name)
                return Type(self.name+(other.name,))
            if isinstance(other.name, tuple):
                return Type((self.name,)+other.name)
            return Type((self.name, other.name))
        raise TypeProductOnlyDefinedForTypes("given type {} ".format(type(other)))

    def __str__(self):
        if isinstance(self.name, tuple):
            return "(Type{})".format(self.name)
        return "(Type({}))".format(self.name)


Integer = Type("int")
