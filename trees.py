"""
All the trees neded on the package.
"""
class TreeError(Exception):
    """
    Usually all of exceptions on module are inherits from just one class
    """

class AddNonTreeNodeAsNodeError(TreeError):
    """
    Only nodes can be append to nodes.
    """


class BTree():
    """
    Binary tree implementation
    """
    def __init__(self, data, parent=None, left=None, right=None):
        self.data = data
        self.add_node(parent, "p")
        self.add_node(left, "l")
        self.add_node(right, "r")


    def add_node(self, tree, kind_flag):
        """
        Just check the type
        """
        if isinstance(tree, BTree) or (tree is None):
            if kind_flag == "p":
                self.parent = tree
            elif kind_flag == "l":
                self.left = tree
            elif kind_flag == "r":
                self.right = tree
            return
        raise AddNonTreeNodeAsNodeError("with type {}".format(type(tree)))

    def __str__(self):
        return "BTree({},{},{})".format(self.data, str(self.left), str(self.right))


    def get_left_most(self):
        """
        returns most left leaft of tree
        """
        nod = self
        while nod:
            if nod:
                old = nod
                nod = nod.left
            else:
                break
        return old


    def pre_traverse(self,f,state):
        remain=[self]
        while(remain):
            current= remain.pop()
            state = f(current,state)
            if current.left :
                remain.append(current.right)
            if current.right :
                remain.append(current.left)
        return state

    def pre_traverse_same_state(self,f,state):
        remain=[(self,state)]
        while(remain):
            current,state= remain.pop()
            state = f(current,state)
            if current.left :
                remain.append((current.right,state))
            if current.right :
                remain.append((current.left,state))
        return state

    def pre_traverse_as_generator(self,f,state):
        remain=[self]
        while(remain):
            current= remain.pop()
            state = f(current,state)
            yield state
            if current.left :
                remain.append(current.right)
            if current.right :
                remain.append(current.left)



    def pos_traverse_rec(self,f,state):
        if self.left:
            state = self.left.pos_traverse_rec(f,state)
        if self.right:
            state = self.right.pos_traverse_rec(f,state)
        state = f(self,state)
        return state

    def pos_traverse(self,f,state):
        node_uneval = 0
        node_eval = 1

        remain = [(self,node_uneval)]
        while(remain):
            current,status = remain.pop()
            if status == node_uneval:
                if current.right :
                    aux_remain=[]
                    aux_remain.append((current.right,node_uneval))
                    if current.left :
                        aux_remain.append((current.left,node_uneval))
                    remain.append((current,node_eval))
                    remain+= aux_remain
                elif current.left:
                    remain.append((current,node_eval))
                    remain.append((current.left,node_uneval))
                else :
                    state = f(current,state)
            elif status == node_eval :
                state = f(current,state)
        return state

    def pos_traverse2(self,f,state):
        in_nodes = [self]
        out_nodes = []
        while(in_nodes):
            current = in_nodes.pop()
            out_nodes.append(current)
            if current.right:
                in_nodes.append(current.right)
            if current.left:
                in_nodes.append(current.left)

        while(out_nodes):
            current = out_nodes.pop()
            state = f(current,state)
        return state

    def nodes2list(self,f,state):
        datas = self.pre_traverse_as_generator(lambda x,y: x.data, 0)

    def get_nodes_data(self):
        return self.pre_traverse_as_generator(lambda x,y: x.data,0)

    def pretty2(self,ident_step=4):
        def aux(node,state):
            l,ident = state
            l.append("\n")
            l.append(" "*(ident*ident_step))
            l.append(str(node.data))
            ident +=1
            return (l,ident)
        out,_ = self.pre_traverse_same_state(aux,([],0))
        return "".join(out)

    def pretty(self,ident_step=4,translate=0):
        if translate<=0:
            def aux(node,state):
                l,ident = state
                l.append("\n"*min(ident,1))
                l.append(" "*(ident-1)*ident_step)
                l.append("|"*min(ident,1))
                l.append("-"*((ident_step-1))*min(ident,1))
                l.append(str(node.data))
                ident +=1
                return (l,ident)
        else :
            def aux(node,state):
                l,ident = state
                l.append("\n"*min(ident,1))
                l.append(" "*translate)
                l.append(" "*(ident-1)*ident_step)
                l.append("|"*min(ident,1))
                l.append("-"*((ident_step-1))*min(ident,1))
                l.append(str(node.data))
                ident +=1
                return (l,ident)
        out,_ = self.pre_traverse_same_state(aux,([],0))
        return "".join(out)


def test():
    b = BTree("b",None,BTree(1),BTree(2))
    c = BTree("c",None,BTree(3),BTree(4))
    a = BTree("a",None,b,c)
    print(a.pretty())
    print(a.pretty(10))




if __name__ == '__main__':
    test()