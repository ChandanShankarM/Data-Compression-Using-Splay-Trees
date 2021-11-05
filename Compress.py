from splayTree import *
import math

trees = {}

def bin_to_int(binstr):
    n = 1
    int_ = 0
    for bit in binstr[::-1]:
        int_ += n * (bit == '1')
        n = n * 2
    return int_


def int_to_bin(int_, log):
    binstr = ''
    while log != 0:
        binstr = str(int_%2) + binstr
        int_ = int_ // 2
        log -= 1
    return binstr

class compressionTree:
    def __init__(self, fileName):
        self.fileName = fileName
        myFile = open(fileName, 'r')
        self.text = ''.join( myFile.readlines() )
        myFile.close()
        self.p={}
        self.tree = splayTree()
        for i in self.text:
            if not self.tree.get_root():
                self.tree.insert((1, None))
                curr= self.tree.get_root()
                node = splayNode((1, i))
                curr.set_left(node)
                self.p[node.get_val()[1]]=node
            elif i not in self.p.keys():
                if not curr.get_right():
                    node = splayNode((1, i))
                    curr.set_right(node)
                    root= curr.get_val()
                    curr.set_val((root[0]+1, root[1]))
                    self.swap(curr)
                    self.p[node.get_val()[1]]=node
                else:
                    temp=splayNode(None)
                    curr.deepcopy(temp)
                    root= curr.get_val()
                    curr.set_val((root[0]+1, root[1]))
                    curr.set_right(temp)
                    node = splayNode((1, i))
                    curr.set_left(node)
                    self.p[node.get_val()[1]]=node
            elif i in self.p.keys():
                for k,j in self.p.items():
                    if j.get_val()[1] == i:
                        i_node=j
                        val=j.get_val()
                        j.set_val((val[0]+1, val[1]))
                        while j.get_parent():
                            j=j.get_parent()
                            val=j.get_val()
                            j.set_val((val[0]+1, val[1]))
                            self.swap(j)
                        self.tree.semi_splay(i_node)

        self.key = {}
        for i,j in self.p.items():
            code = self.tree.code(j) 
            self.key[i] = code
            
    def swap(self, curr):
        if curr.get_right().get_val()[0] < curr.get_left().get_val()[0]:
            temp=curr.get_right()
            curr.set_right(curr.get_left())
            curr.set_left(temp)
    
    def get_text(self):
        return self.text

    def get_tree(self):
        return self.tree

    def get_key(self):
        return self.key

def compress(fileName):
    tree = compressionTree(fileName)
    trees[fileName.split('.')[0] +'_comp.txt'] = tree
    code = ''
    code_text = ''
    rem_bits=''
    for i in tree.get_text():
        code += tree.get_key()[i]
    for i in range(0, len(code), 7):
        if i+6 < len(code):
            code_text += chr(int(code[i: i+7], 2))
        else:
            rem_bits = code[i:]
    newFile = open(fileName.split('.')[0] + '_comp.txt', 'w')
    newFile.write(rem_bits + '\n' + code_text)
    newFile.close()

def decompress(fileName):
    tree = trees[fileName].get_tree()
    coded=''
    with open(fileName, 'rb') as f:
        rem_bits = f.readline()
        rem_bits = rem_bits[:len(rem_bits)-1]
        rem_bits = rem_bits.decode('UTF-8')
        for line in f:
            code = line.decode('UTF-8')
            for i in range(len(code)):
                    if code[i] == '\r' and code[i + 1] == '\n':
                        continue
                    else:
                        a = ord(code[i])
                        a = bin(a).replace("0b", "")
                        if len(a)<7:
                            a = ('0'*(7-len(a)))+a
                        coded += a
    coded += rem_bits[:len(rem_bits)-1]
    f.close()
    text = ''
    i = 0
    while i != len(coded):                                   # read the binary code and trace the corresponding path on the tree
        node = tree.get_root()
        
        while not node.is_leaf():                           # until we reach a leaf node
            
            if coded[i] == '0':
                node = node.child['left']
            elif coded[i] == '1':
                node = node.child['right']
            i += 1
        
        text = text + node.get_val()[1]                       # output the character of the leaf node
    newFile = open(fileName.split('.')[0] + '_dec.txt', 'w')
    newFile.write(text)
    newFile.close()

compress('example.txt')
decompress('example_comp.txt')