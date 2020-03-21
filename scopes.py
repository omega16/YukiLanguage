"""
All stuff related to scopes
"""

from collections import UserDict

class ScopeError(Exception):
    """
    Class for Scope errors
    """

class ScopeParentMustBeScopeOrNone(ScopeError):
    """
    Scope parent must be a scope or if root it could be None.
    """

class ScopeModuleParentMustBeModuleOrNone(ScopeError):
    """
    Same as in Scope but for Module
    """

class ScopeLocalParentMustBeScope(ScopeError):
    """
    LocalScopes Don't need to have Local or Module as parent but 
    is needed that parent is Scope 
    """

class Scope(UserDict): # pylint: disable=too-many-ancestors
    """
        Scope needs to handle circular references and search for key on parent
    """
    def __init__(self, parent, *args):
        super().__init__(*args)
        if isinstance(parent, Scope) or (parent is None):
            self.parent = parent
        else:
            raise ScopeParentMustBeScopeOrNone("given type : {} ".format(type(parent)))

    def __getitem__(self, key):
        if not (value := self.data.get(key)) is None:
            return value
        if not self.parent is None:
            return self.parent[key]

        raise KeyError("can't find {} in scope".format(key))

    def get(self, key, default=None):
        if not (value := self.data.get(key)) is None:
            return value
        if not self.parent is None:
            return self.parent.get(key)

        return default

    def __contains__(self, key):
        if key in self.data.get(key):
            return True
        if not self.parent is None:
            return key in self.parent

        return False

class Module(Scope): # pylint: disable=too-many-ancestors
    """
    Since is a functional language and most of them is not implemented yet
    the only things that can go on a module scope are :
        - Combinator (function) definition
    """
    def __init__(self, parent, name, *args):
        if isinstance(parent, Module) or (parent is None):
            super().__init__(parent, *args)
        else:
            raise ScopeModuleParentMustBeModuleOrNone("current type {} ".format(type(parent)))
        self.name = name

    def __str__(self):
        return "Module({},parent = {})".format(self.name, self.parent)

class LocalScope(Scope): # pylint: disable=too-many-ancestors
    """
    There are plenty of places for LocalScopes, as :
        - Every combinator definition has it's local scope
        - Every Let (some1) in (some2) defines changes on local scope for some2
    What are the elements of LocalScopes?
    There must be one of :
        - Variable
        - Combinator name
    """
    def __init__(self, parent, location, *args):
        if isinstance(parent, Scope):
            super().__init__(parent, *args)
        else:
            raise ScopeModuleParentMustBeModuleOrNone("current type {} ".format(type(parent)))
        self.location = location

    def __str__(self):
        return "LocalScope({},parent = {})".format(self.location,self.parent)
        