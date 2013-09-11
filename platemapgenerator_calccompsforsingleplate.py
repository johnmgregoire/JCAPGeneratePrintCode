import time, copy, pickle
import os, os.path
import sys
import numpy, pylab

sys.path.append('C:/Users/Gregoire/Documents/PythonCode/JCAP')
from readplatemap import *

modelpath='C:/Users/Gregoire/Documents/CaltechWork/platemaps/Quaternarysingleplate/plate333_1map_full.txt'
newpath='C:/Users/Gregoire/Documents/CaltechWork/platemaps/Quaternarysingleplate/plate20intervwbin.txt'

writelines=[]
f=open(modelpath, mode='r')
ls=f.readlines()[:2]
writelines+=[l.strip() for l in ls]
f.close()

dlist=readsingleplatemaptxt(modelpath,  returnfiducials=False)
dlistsrc=readplatemaptxt(codes=[0, 1, 2, 3])

smpsrc=numpy.array([d['Sample'] for d in dlistsrc])
codesrc=numpy.array([d['code'] for d in dlistsrc])

intervs=20
comps=[[1.0*b/intervs, 1.0*c/intervs, 1.0*(intervs-a-b-c)/intervs, 1.0*a/intervs] for a in numpy.arange(0,intervs+1)[::-1] for b in numpy.arange(0,intervs+1-a) for c in numpy.arange(0, intervs+1-a-b)][::-1]

def genbinarycomps(intervs, elind1, elind2, ndim=4):
    aa=numpy.linspace(0.,1.,intervs+1)
    c=numpy.zeros((len(aa), ndim), dtype='float64')
    c[:, elind1]=aa
    c[:, elind2]=1.-aa
    return c

comps2=comps
codes=[0]*len(comps)
binintervs=5
for i, j in [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]:
    comps2+=list(genbinarycomps(binintervs, i, j))+[numpy.zeros(4, dtype='float64')] #add 6 compositions in binary line and then zeros
    codes+=[4]*6+[1]
comps2+=[numpy.zeros(4, dtype='float64')]*6 #6 more zeros to round out the 1819 code0 samples in a standard platemap
codes+=[1]*6
comps2=[numpy.array(c) for c in comps2]

comps2pop=copy.copy(comps2)
codespop=copy.copy(codes)

for d in dlist:
    if d['code']==0:
        c=comps2pop.pop(0)
        cd=codespop.pop(0)
        for k, v in zip(['A', 'B', 'C', 'D'], c):
            d[k]=v
        d['code']=cd

k_f=[\
('Sample','%04d'),\
('x','%.2f'),\
('y','%.2f'),\
('dx','%.2f'),\
('dx','%.2f'),\
('A','%.3f'),\
('B','%.3f'),\
('C','%.3f'),\
('D','%.3f'),\
('E','%.3f'),\
('F','%.3f'),\
('G','%.3f'),\
('H','%.3f'),\
('code','%d'),\
]

writelines+=[', '.join([f %d[k] for k, f in k_f]) for d in dlist]

f=open(newpath, mode='w')
f.write('\n'.join(writelines))
f.close()

sys.path.append('C:/Users/Gregoire/Documents/PythonCode/ternaryplot')
from myquaternaryutility import QuaternaryPlot

for d in dlist:
    c=numpy.array([d[el] for el in ['A', 'B', 'C', 'D']])
    if c.sum()>0:
        c/=c.sum()
    d['compositions']=c

carr=numpy.array([d['compositions'] for d in dlist])
stpq=QuaternaryPlot(111)
stpq.scatter(carr)
pylab.show()
