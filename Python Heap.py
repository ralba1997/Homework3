import random
from timeit import Timer
import timeit
from random import randint
import matplotlib.pyplot as plt
import math
import os
import matplotlib.patches as mpatches
import heapq

def insertnumbersinheap(aheap, alist):
    for i in range(len(alist)):
        heapq.heappush(aheap, alist[i])
    return aheap

def heapfindmax(aheap):
    aheapqmax = heapq.nlargest(1,aheap)
    return aheapqmax[0]


def heapdelmax(aheap):
    m = heapfindmax(aheap)
    qm = [x for x in aheap[dim // 2:] if x == m]
    for r in qm:
        indexr = aheap.index(r)
        aheap.pop(indexr)
    return

def genrandomnumbers(length, maxval):
    rnumbers = [random.randint(1,maxval) for b in range(length)]
    return rnumbers

def gettime(funcname, *args):
    def wrap():
        funcname(*args)
    setpar = "from __main__ import " + funcname.__name__
    t1 = Timer(wrap, setpar)
    time = str(t1.timeit(1)) + " "
    return time
    
def writef(filename,myres):
    with open(filename,"w") as f:
        text=myres
        f.write('{}'.format(text))
    return

def readf(filename):
    with open(filename,"r") as f:
        r_n=f.readline()
    return r_n    


path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)
if not os.path.exists("Data"):
    os.makedirs("Data")
os.chdir(path + "\Data")

maxpoweroften=6
numberoftests=5
maxvalue = 10000000

filenames=["pheapinsertion","pheapfindmax","pheapdelmax"]
pheapinsertion_times=""
pheapfindmax_times=""
pheapdelmax_times=""
for nrtest in range(numberoftests):
    for dim in [10**p for p in range(1,maxpoweroften+1)]:
        L=genrandomnumbers(dim, maxvalue)
        pheap = []
        heapq.heapify(pheap)
        time=gettime(insertnumbersinheap, pheap, L)
        pheapinsertion_times+=time
        time=gettime(heapfindmax, pheap)
        pheapfindmax_times+=time

        time=gettime(heapdelmax, pheap)
        pheapdelmax_times+=time
    pheapinsertion_times+="\n"
    pheapfindmax_times+="\n"
    pheapdelmax_times+="\n"
writef("pheapinsertion.txt",pheapinsertion_times)
writef("pheapfindmax.txt",pheapfindmax_times)
writef("pheapdelmax.txt",pheapdelmax_times)

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

    if filein == "pheapinsertion":
        pheapinsertiontimes = meantimes
    elif filein == "pheapfindmax":
        pheapfindmaxtimes = meantimes
    elif filein == "pheapdelmax":
        pheapdelmaxtimes = meantimes

    N = [10 ** p for p in range(1, maxpoweroften + 1)]

fig = plt.figure()
plt.plot(N, pheapinsertiontimes, "vb--")
plt.plot(N, pheapfindmaxtimes, "vr--")
plt.plot(N, pheapdelmaxtimes, "vg--")
plt.xscale('log', basex=10)
plt.yscale('log', basey=10)
plt.title("Python Heap (log-log)")
blue_patch = mpatches.Patch(color = "blue", label = "Python Heap- Insertion")
red_patch = mpatches.Patch(color = "red", label = "Python Heap- Find the max")
green_patch = mpatches.Patch(color = "green", label = "Python Heap- Delete the max ")
plt.legend(handles = [blue_patch, red_patch, green_patch])
plt.xlabel("Length of list of random numbers")
plt.ylabel("Times (sec)")
axes = plt.gca()
axes.set_ylim([10**(-6), 10**2])
fig.savefig("Python Heap.png")
