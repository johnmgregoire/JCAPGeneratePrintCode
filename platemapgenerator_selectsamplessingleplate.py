import time, copy, pickle
import os, os.path
import sys
import numpy, pylab

sys.path.append('C:/Users/Gregoire/Documents/PythonCode/JCAP')
from readplatemap import *

modelpath='C:/Users/Gregoire/Documents/CaltechWork/platemaps/NiFeCoCepseudoternary/plate333_1map_full.txt'
selectpath='C:/Users/Gregoire/Documents/CaltechWork/platemaps/NiFeCoCepseudoternary/201304NiFeCoCeI400mV_I400mVLinSub_2Dcut_.txt'
newpath='C:/Users/Gregoire/Documents/CaltechWork/platemaps/NiFeCoCepseudoternary/NiFeCoCeselect_platemap.txt'

writelines=[]
f=open(modelpath, mode='r')
ls=f.readlines()[:2]
writelines+=[l.strip() for l in ls]
f.close()

dlist=readsingleplatemaptxt(modelpath,  returnfiducials=False)
dlistsrc=readplatemaptxt(codes=[0, 1, 2, 3])

smpsrc=numpy.array([d['Sample'] for d in dlistsrc])
codesrc=numpy.array([d['code'] for d in dlistsrc])

f=open(selectpath, mode='r')
ls=f.readlines()
f.close()
samplestocopy=[eval(s.strip()) for s in ls]
print 'start with:', len(samplestocopy)
samplestocopy=[s for s in samplestocopy if codesrc[smpsrc==s].sum()==0]
print 'filter code0:', len(samplestocopy)
samplestocopy+=[8]*74 #17 blank to fill out 2nd to last row
samplestocopy+=[5050]*14
samplestocopy+=[692]*13
print 'add extras:', len(samplestocopy)

srcinds=[numpy.where(smpsrc==i)[0][0] for i in samplestocopy]
srcindspop=copy.copy(srcinds)
smpreplacelist=[]
for d in dlist:
    if d['code']==0:
        for k, v in dlistsrc[srcindspop.pop(0)].items():
            if k=='Sample':
                smpreplacelist+=[(d[k], v)]
            if k in ['Sample', 'x', 'y']:
                continue
            d[k]=v
    
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
