import time, copy, pickle
import os, os.path
import sys
import numpy, pylab

sys.path.append('C:/Users/Gregoire/Documents/PythonCode/JCAP')
from readplatemap import *

modelpath='C:/Users/Gregoire/Documents/CaltechWork/platemaps/Dstep1percent/0037-04-0730-mp.txt'
newpath='C:/Users/Gregoire/Documents/CaltechWork/platemaps/Dstep1percent/Dstep1percent.txt'

writelines=[]
f=open(modelpath, mode='r')
ls=f.readlines()[:2]
writelines+=[l.strip() for l in ls]
f.close()

dlist=readsingleplatemaptxt(modelpath,  returnfiducials=False)

for d in dlist:
    if d['code']==100 or d['code']==4:
        d['code']=0

def genbinarycomps(intervs, elind1, elind2, ndim=4):
    aa=numpy.linspace(0.,1.,intervs+1)
    c=numpy.zeros((len(aa), ndim), dtype='float64')
    c[:, elind1]=aa
    c[:, elind2]=1.-aa
    return c
intervs=20
tc=[[1.0*b/intervs, 1.0*(intervs-a-b)/intervs, 1.0*a/intervs] for a in numpy.arange(0,intervs+1)[::-1] for b in numpy.arange(0,intervs+1-a)][::-1]
tc=numpy.array(tc)
intervs=19
tc19=[[1.0*b/intervs, 1.0*(intervs-a-b)/intervs, 1.0*a/intervs] for a in numpy.arange(0,intervs+1)[::-1] for b in numpy.arange(0,intervs+1-a)][::-1]
tc19=numpy.array(tc19)


comps_d=[tc]

q=numpy.zeros((len(tc), 4), dtype='float64')
q[:, :3]=tc[:, :]
comps2=list(q)

for dval in [.01, .02, .03, .04]:
    t=tc*(1.-dval)
    t=numpy.round(t, decimals=2)
    for v in t:
        i=numpy.argmax(v)
        v[i]=numpy.round((1.-dval-(v.sum()-v[i])), decimals=2)
    
    comps_d+=[t]
    q=numpy.zeros((len(t), 4), dtype='float64')
    q[:, :3]=t[:, :]
    q[:, 3]=dval
    comps2+=list(q)

for dval in [.05, .06, .07]:
    t=tc19*(1.-dval)
    t=numpy.round(t, decimals=2)
    for v in t:
        i=numpy.argmax(v)
        v[i]=numpy.round((1.-dval-(v.sum()-v[i])), decimals=2)
    
    comps_d+=[t]
    q=numpy.zeros((len(t), 4), dtype='float64')
    q[:, :3]=t[:, :]
    q[:, 3]=dval
    comps2+=list(q)

codes=[0]*len(comps2)

#comps2+=[numpy.zeros(4, dtype='float64')]*6 #6 more zeros to round out the 1819 code0 samples in a standard platemap
#codes+=[1]*6
#comps2=[numpy.array(c) for c in comps2]

comps2pop=copy.copy(comps2)
codespop=copy.copy(codes)

for count, d in enumerate(dlist):
    if d['code']==0:
        if len(comps2pop)==0:
            c=[0.]*4
            cd=4
        else:
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
from myternaryutility import TernaryPlot

for d in dlist:
    c=numpy.array([d[el] for el in ['A', 'B', 'C', 'D']])
    if c.sum()>0:
        c/=c.sum()
    d['compositions']=c

carr=numpy.array([d['compositions'] for d in dlist])
stpq=QuaternaryPlot(111)
stpq.scatter(carr)

pylab.figure()
for count, tv in enumerate(comps_d):
    stpq=TernaryPlot((4, 2, count+1))
    tvnorm=[tvv/tvv.sum() for tvv in tv]
    stpq.scatter(tvnorm, marker='.', c='r', edgecolor='none')
    if count<5:
        ttt=tc
    else:
        ttt=tc19
    stpq.scatter(ttt, marker='.', c='g', edgecolor='none')

pylab.show()
