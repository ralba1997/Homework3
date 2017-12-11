from timeit import Timer
import random
from random import randint
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

class TreeNode:
    def __init__(self, key, val, left=None, right=None, parent=None):
        self.key = key
        self.val = val
        self.leftChild = left
        self.rightChild = right
        self.parent = parent

    def hasLeftChild(self):
        return self.leftChild

    def hasRightChild(self):
        return self.rightChild

    def hasAnyChildren(self):
        return self.rightChild or self.leftChild

    def hasBothChildren(self):
        return self.rightChild and self.leftChild

    def isLeftChild(self):
        return self.parent and self.parent.leftChild == self

    def isRightChild(self):
        return self.parent and self.parent.rightChild == self

    def isRoot(self):
        return not self.parent

    def isLeaf(self):
        return not (self.rightChild or self.leftChild)

    def replaceNodeData(self, key, value, lc, rc):
        self.key = key
        self.val = value
        self.leftChild = lc
        self.rightChild = rc
        if self.hasLeftChild():
            self.leftChild.parent = self
        if self.hasRightChild():
            self.rightChild.parent = self

    def findSuccessor(self):
        succ = None
        if self.hasRightChild():
            succ = self.rightChild.findMin()
        else:
            if self.parent:
                if self.isLeftChild():
                    succ = self.parent
                else:
                    self.parent.rightChild = None
                    succ = self.parent.findSuccessor()
                    self.parent.rightChild = self
        return succ

    def spliceOut(self):
        if self.isLeaf():
            if self.isLeftChild():
                self.parent.leftChild = None
            else:
                self.parent.rightChild = None
        elif self.hasAnyChildren():
            if self.hasLeftChild():
                if self.isLeftChild():
                    self.parent.leftChild = self.leftChild
                else:
                    self.parent.rightChild = self.leftChild
                self.leftChild.parent = self.parent
            else:
                if self.isLeftChild():
                    self.parent.leftChild = self.rightChild
                else:
                    self.parent.rightChild = self.rightChild
                self.rightChild.parent = self.parent

    def findMin(self):
        current = self
        while current.hasLeftChild():
            current = current.leftChild
        return current

    def findMax(self):
        current = self
        while current.hasRightChild():
            current = current.rightChild
        return current


class BinarySearchTree:
    def __init__(self):
        self.name = None
        self.root = None
        self.size = 0

    def length(self):
        return self.size

    def __len__(self):
        return self.size

    def put(self, key, val):
        if self.root:
            self._put(key, val, self.root)
        else:
            self.root = TreeNode(key, val)
        self.size = self.size + 1

    def _put(self, key, val, currentNode):
        if key < currentNode.key:
            if currentNode.hasLeftChild():
                self._put(key, val, currentNode.leftChild)
            else:
                currentNode.leftChild = TreeNode(key, val, parent=currentNode)
        elif key > currentNode.key:
            if currentNode.hasRightChild():
                self._put(key, val, currentNode.rightChild)
            else:
                currentNode.rightChild = TreeNode(key, val, parent=currentNode)
        else:
            currentNode.val = val

    def __setitem__(self, k, v):
        self.put(k, v)

    def get(self, key):
        if self.root:
            res = self._get(key, self.root)
            if res:
                return res.val
            else:
                return None
        else:
            return None

    def _get(self, key, currentNode):
        if not currentNode:
            return None
        elif currentNode.key == key:
            return currentNode
        elif key < currentNode.key:
            return self._get(key, currentNode.leftChild)
        else:
            return self._get(key, currentNode.rightChild)

    def __getitem__(self, key):
        return self.get(key)

    def __contains__(self, key):
        if self._get(key, self.root):
            return True
        else:
            return False

    def delete(self, key):
        if self.size > 1:
            nodeToRemove = self._get(key, self.root)
            if nodeToRemove:
                self.remove(nodeToRemove)
                self.size = self.size - 1
            else:
                raise KeyError('Error, key not in tree')
        elif self.size == 1 and self.root.key == key:
            self.root = None
            self.size = self.size - 1
        else:
            raise KeyError('Error, key not in tree')

    def __delitem__(self, key):
        self.delete(key)

    def remove(self, currentNode):
        if currentNode.isLeaf():
            if currentNode == currentNode.parent.leftChild:
                currentNode.parent.leftChild = None
            else:
                currentNode.parent.rightChild = None
        elif currentNode.hasBothChildren():  # interior
            succ = currentNode.findSuccessor()
            succ.spliceOut()
            currentNode.key = succ.key
            currentNode.val = succ.val
        else:  # this node has one child
            if currentNode.hasLeftChild():
                if currentNode.isLeftChild():
                    currentNode.leftChild.parent = currentNode.parent
                    currentNode.parent.leftChild = currentNode.leftChild
                elif currentNode.isRightChild():
                    currentNode.leftChild.parent = currentNode.parent
                    currentNode.parent.rightChild = currentNode.leftChild
                else:
                    currentNode.replaceNodeData(currentNode.leftChild.key,
                                                currentNode.leftChild.val,
                                                currentNode.leftChild.leftChild,
                                                currentNode.leftChild.rightChild)
            else:
                if currentNode.isLeftChild():
                    currentNode.rightChild.parent = currentNode.parent
                    currentNode.parent.leftChild = currentNode.rightChild
                elif currentNode.isRightChild():
                    currentNode.rightChild.parent = currentNode.parent
                    currentNode.parent.rightChild = currentNode.rightChild
                else:
                    currentNode.replaceNodeData(currentNode.rightChild.key,
                                                currentNode.rightChild.val,
                                                currentNode.rightChild.leftChild,
                                                currentNode.rightChild.rightChild)

def insertnumbersintree(atree, alist):
    for i in range(len(alist)):
        atree.put(alist[i], alist[i])
    return atree

def getrelement(atree, element):
    relemvalue = atree.get(element)
    return relemvalue


def maxelement(atree):
    maxnodekey = atree.root.findMax().key
    return maxnodekey

def delrelement(atree,element):
    atree.delete(element)


def genrandomnumbers(length, maxval):
    rnumbers = [random.randint(1,maxval) for b in range(length)]
    return rnumbers

def gettime(funcname, param, param2):
    if param2 == "":
        fn = funcname.__name__ + "(" + param.name + ")"
    else:
        fn = funcname.__name__ + "(" + param.name + "," + str(param2) + ")"
    setpar = "from __main__ import " + funcname.__name__ + "," + param.name
    t1 = Timer(fn, setpar)
    time = str(t1.timeit(1)) + " "
    return time

def writef(filename, myres):
    with open(filename, "w") as f:
        text = myres
        f.write('{}'.format(text))
    return


def readf(filename):
    with open(filename, "r") as f:
        r_n = f.readline()
    return r_n


if __name__ == '__main__':
    path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(path)
    if not os.path.exists("Data"):
        os.makedirs("Data")
    os.chdir(path + "\Data")
    maxpoweroften = 6
    numberoftests = 5
    maxvalue = 10000000

    filenames = ["insertion", "getrandomelement", "maxtree", "delrandomelement"]
    insertion_times = ""
    getrandomelement_times = ""
    findmax_times = ""
    delrandomelement_times = ""

    for nrtest in range(numberoftests):
        for dim in [10 ** p for p in range(1, maxpoweroften + 1)]:
            L = genrandomnumbers(dim, maxvalue)
            mytree = BinarySearchTree()
            mytree.name="mytree"
            time = gettime(insertnumbersintree, mytree , L)
            insertion_times += time
            elem = random.choice(L)
            time = gettime(getrelement, mytree , elem)
            getrandomelement_times += time
            time = gettime(maxelement,mytree, "")
            findmax_times += time
            elem = random.choice(L)
            time = gettime(delrelement, mytree, elem)
            delrandomelement_times += time
        insertion_times += "\n"
        getrandomelement_times += "\n"
        findmax_times += "\n"
        delrandomelement_times += "\n"

    writef("insertion.txt", insertion_times)
    writef("getrandomelement.txt", getrandomelement_times)
    writef("maxtree.txt", findmax_times)
    writef("delrandomelement.txt", delrandomelement_times)

for filein in filenames:

    filename = filein + ".txt"
    t = []
    with open(filename, "r") as f:
        for i in range(numberoftests):
            t.append(list(map(float, f.readline().split())))

    meantimes = []
    for j in range(maxpoweroften):
        sumt = sum(t[i][j] for i in range(numberoftests))
        meantimes.append(sumt / numberoftests)

    if filein == "insertion":
        insertiontimes = meantimes
    elif filein == "getrandomelement":
        gettimes = meantimes
    elif filein == "maxtree":
        maxtreetimes = meantimes
    elif filein == "delrandomelement":
        deltimes = meantimes

N = [10 ** p for p in range(1, maxpoweroften + 1)]

fig = plt.figure()
plt.plot(N, insertiontimes, "vb--")
plt.plot(N, gettimes, "vr--")
plt.plot(N, maxtreetimes, "vg--")
plt.plot(N, deltimes, "vc--")
plt.xscale('log', basex=10)
plt.yscale('log', basey=10)
plt.title("Binary Tree (log-log)")
plt.xlabel("Length of list of random numbers")
plt.ylabel("Times (sec)")
blue_patch = mpatches.Patch(color = "blue", label = "Binary Tree- Insertion")
red_patch = mpatches.Patch(color = "red", label = "Binary Tree- Get random element")
green_patch = mpatches.Patch(color = "green", label = "Binary Tree- Get the max ")
cyan_patch = mpatches.Patch(color = "cyan", label = "Binary Tree- Delete random element")
plt.legend(handles = [blue_patch, red_patch, green_patch, cyan_patch])
axes = plt.gca()
axes.set_ylim([10**(-6), 10**2])
plt.savefig("Binary Tree.png")
