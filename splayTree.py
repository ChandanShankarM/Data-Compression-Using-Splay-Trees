# from BSTree import *

# add rotation related functions as your implementation requires:
    # zig(x), zig-zag(x), zig-zig(x)
class splayNode:
    def __init__(self, val, parent=None):
        self.val = val
        self.child = dict()
        self.parent = parent
        self.child['right'] = None
        self.child['left'] = None

    def get_val(self):
        return self.val
    
    def set_val(self, value):
        self.val=value

    def get_parent(self):
        return self.parent

    def set_parent(self, node):
        self.parent = node

    def get_right(self):
        return self.child['right']
    
    def get_left(self):
        return self.child['left']

    def set_right(self, node):
        self.child['right']=node
        node.set_parent(self)
    
    def set_left(self, node):
        self.child['left']=node
        node.set_parent(self)

    def deepcopy(self, node):
        node.set_val(self.val)
        node.parent=self.parent
        node.set_left(self.child['left'])
        node.set_right(self.child['right'])


    """ Ignore Following methods of node... Read them in the end as they are related to splay process """
    
    def which_child(x): # if x is right-child, or left-child. Returns a tuple (x_position, sibling_position)
        p = x.parent
        if p.child['right'] == x:
            return ('right', 'left')
        elif p.child['left'] == x:
            return ('left', 'right')
        
    def rotate_edge(x): # rotates edge joining x to its parent p... or in other words, switches their positions in the tree
        p = x.parent
        g = p.parent

        this_edge, other_edge = x.which_child()
        c = x.child[other_edge]
        x.child[other_edge] = p
        p.child[this_edge] = c
        
        if c != None:
            c.parent = p

        if g != None:
            this_edge, other_edge = p.which_child()
            g.child[this_edge] = x

        x.parent = g
        p.parent = x

    def zig(x): # rotates edge x->p
        x.rotate_edge()

    def zig_zig(x): # rotates edges in following order: p->g then x->p
        p = x.parent
        p.rotate_edge()
        x.rotate_edge()

    def zig_zag(x): # rotates edge x->p, then the resuting edge x->g
        x.rotate_edge()
        x.rotate_edge()

    def is_leaf(node):
        return node.child['left'] == None and node.child['right'] == None
    
    def node_print(self, d): # displays the 'parent:node' data for all children of self, where d is its depth
        p = self.parent
        pv = None
        if p != None:
            pv = p.val
        print(d*'    ', pv, ':', self.val, sep = '')
        if self.child['left']:
            self.child['left'].node_print(d + 1)
        else:
            print((d+1)*'    ', self.val, ':No_left_child', sep = '')
        if self.child['right']:
            self.child['right'].node_print(d + 1)
        else:
            print((d+1)*'    ', self.val, ':No_right_child', sep = '')
    
class splayTree:
    def __init__(self):
        self.root = None

    def insert(self, val):          # inserts new node of value 'val'
        if self.root == None:
            self.root = splayNode(val)
            return 0

        node = self.root
        while node != None:
            if node.val < val:
                look_at = 'right'
            elif node.val >= val:
                look_at = 'left'
                
            parent = node
            node = node.child[look_at]
            
        new_node = splayNode(val, parent)
        parent.child[look_at] = new_node
        
        # self.splay( new_node ) # removing this line will make this tree just an ordinary binary tree
        return 1

    def splay(self, x):
        while x.parent != None:
            p = x.parent
            if p == self.root:                          # if p is root
                x.zig()
            elif p.which_child() == x.which_child():    # when both p and x are left children or both are right children
                x.zig_zig()
            else:                                       # otherwise
                x.zig_zag()
        self.root = x

    def semi_splay(self, x):
        if x.parent == None:
            return 0
        if x.parent.parent == None:
            return 0
        
        while x.parent.parent != None:
                a=x.parent.parent
                p = x.parent
                p.rotate_edge()         # Both cases of zig-zig and zig-zag are reduced to just p.rotate_edge()
                a.set_val((a.child['left'].get_val()[0]+a.child['right'].get_val()[0],a.get_val()[1]))
                p.set_val((p.child['left'].get_val()[0]+p.child['right'].get_val()[0],p.get_val()[1]))
                x = p
                if x.parent == None:
                    break
                
        if x.parent != None:            # The zig case determines the new root of the tree
            a=x.parent
            x.rotate_edge()
            a.set_val((a.child['left'].get_val()[0]+a.child['right'].get_val()[0],a.get_val()[1]))
            x.set_val((x.child['left'].get_val()[0]+x.child['right'].get_val()[0],x.get_val()[1]))
        self.root = x

    def code(self, leaf): # returns binary code of given leaf node in the binary tree and also performs semi-splay on it
        node = leaf
        code = ''
        while node.parent != None:
            
                if node.which_child()[0]=='right':
                    node = node.parent
                    code = code + '1'
                elif node.which_child()[0]=='left':
                    node = node.parent
                    code = code + '0'
                
        return code[::-1]

    def print(self): # displays entire tree in the indentation fashion and each line of form 'parent:node'
        print('----------- Splaytree -----------')
        self.root.node_print(0)

    def find_node(self, val):
        node = self.root
        while node != None:
            
                if node.val < val:
                    node = node.child['right']
                elif node.val > val:
                    node = node.child['left']
                else:
                    self.splay( node ) # removing this line will make this tree just an ordinary binary tree
                    break
                
        return node

    def get_root(self):
        return self.root

    def set_root(self, val):
        self.root == val

    def join_trees(self, tree2):
        lc=self.root
        self.root.val=(self.root.val[0]+ tree2.get_root().get_val()[0], None)
        self.root.child['left']=lc
        self.root.child['right']=tree2.get_root()

    def join_node(self, val):
        lc=self.root
        self.root.val=(self.root.val[0]+ val[0], None)
        self.root.child['left']=lc
        self.root.child['right']=splayNode(val)
