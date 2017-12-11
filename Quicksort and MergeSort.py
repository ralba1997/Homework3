import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
import random
from random import randint
from timeit import Timer
import timeit


def qsort(m):
    if len(m) <= 1:
        return m
    else:
        pivot=m[0]
        m1 = [x for x in m[1:] if x <= pivot]
        m2 = [x for x in m[1:] if x > pivot]
        m1 = qsort(m1)
        m2 = qsort(m2)
        return m1+[pivot]+m2


def mergesort(l):
    if len(l)<=1:
        return l

    midpoint=len(l)//2
    left = mergesort(l[:midpoint])
    right = mergesort(l[midpoint:])
    return merge_leftright(left, right)


def merge_leftright(left, right):
    result=[]
    left_pointer=0
    right_pointer=0
    while left_pointer<len(left) and right_pointer< len(right):
        if left[left_pointer] <= right[right_pointer]:
            result.append(left[left_pointer])
            left_pointer+=1
        else:
            result.append(right[right_pointer])
            right_pointer+=1
    result+=(left[left_pointer:])
    result+=(right[right_pointer:])
    return result


def genrandomnumbers(length, maxval):
    rnumbers = [random.randint(1,maxval) for b in range(length)]
    return rnumbers

def gettime(funcname, param):
    fn = funcname.__name__ + "(" + str(param) + ")"
    setpar = "from __main__ import " + funcname.__name__
    t1 = Timer(fn, setpar)
    time = str(t1.timeit(1)) + " "
    return time

def writef(filename,myres):
    with open(filename,"w") as f:
        text=myres
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

    filenames = ["quicksort", "mergesort"]
    quicksorttimes = ""
    mergesorttimes = ""

    for nrtest in range(numberoftests):
        for dim in [10 ** p for p in range(1, maxpoweroften + 1)]:
            L = genrandomnumbers(dim, maxvalue)
            L1= L[:]
            time = gettime(qsort, L)
            quicksorttimes += time
            time = gettime(mergesort, L1)
            mergesorttimes += time
        quicksorttimes += "\n"
        mergesorttimes += "\n"

    writef("quicksort.txt", quicksorttimes)
    writef("mergesort.txt", mergesorttimes)

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

    if filein == "quicksort":
        quicksorttimes = meantimes
    elif filein == "mergesort":
        mergesorttimes = meantimes

N = [10 ** p for p in range(1, maxpoweroften + 1)]

fig = plt.figure()
plt.plot(N, quicksorttimes, "vb--")
plt.plot(N, mergesorttimes, "vr--")
plt.xscale('log', basex=10)
plt.yscale('log', basey=10)
plt.title("Quicksort and MergeSort (log-log)")
plt.xlabel("Length of list of random numbers")
plt.ylabel("Times (sec)")
blue_patch = mpatches.Patch(color = "blue", label = "Quicksort")
red_patch = mpatches.Patch(color = "red", label = "MergeSort")
plt.legend(handles = [blue_patch, red_patch])
axes = plt.gca()
axes.set_ylim([10**(-6), 10**2])
plt.savefig("Quicksort and MergeSort.png")
