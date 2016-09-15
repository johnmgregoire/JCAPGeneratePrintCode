import time, copy, pickle
import os, os.path
import sys
import numpy, pylab
from fcns_generatecompositions import *
sys.path.append('Z:/Documents/PythonCode/JCAP')
from readplatemap import *

modelpath='Z:/Documents/CaltechWork/platemaps/Epson6Elementcombinations_singleplate/template.txt'
newpath='Z:/Documents/CaltechWork/platemaps/Epson6Elementcombinations_singleplate/Epson6Elementcombinations_4els_10steps.txt'

writelines=[]
f=open(modelpath, mode='r')
ls=f.readlines()[:2]
writelines+=[l.strip() for l in ls]
f.close()

dlist=readsingleplatemaptxt(modelpath,  returnfiducials=False)


updatecomp=lambda d, c:d.update(dict([(s, v) for s, v in zip(['A', 'B', 'C', 'D', 'E','F', 'G', 'H'], c)]))


#put the binary compositions as code 100 at the last row and last columns except for right-most ref column
bincompinds=numpy.arange(2176-22-41,2176-1-41)

indstemp=[[i,j] for i in range(6) for j in range(i,6)]

for inds, dlistind in zip(indstemp, bincompinds):
    z=numpy.zeros(6, dtype='float32')
    z[inds]=1.
    z/=z.sum()
    updatecomp(dlist[dlistind], z)
    dlist[dlistind]['code']=100


#comp refs as code 3 or 4 at right-most ref column
comprefinds=numpy.arange(34)*64#+63

indstemp=[i for i in range(-1, 6)]
indstemp=indstemp*5
indstemp=indstemp[1:]
#indstemp=indstemp[::-1]#reverse so AB.. at bottom right and ..DEF at top

ccompref=[]
for inds, dlistind in zip(indstemp, comprefinds):
    z=numpy.zeros(6, dtype='float32')
    if inds>=0:
        z[inds]=1.
    updatecomp(dlist[dlistind], z)
    dlist[dlistind]['code']=2 if inds<4 else 3
#    
#
#
c6=[]
for fcn in [combi_6el_inner1, combi_6el_inner2, combi_6el_inner3, combi_6el_inner4]:
    c6+=list(fcn(10))
comps=c6

comps2pop=copy.copy(comps)

for count, d in enumerate(dlist):
    if count in comprefinds or count in bincompinds:
        continue
    updatecomp(d, comps2pop.pop(0))
    d['code']=0


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
if 1:
    f=open(newpath, mode='w')
    f.write('\n'.join(writelines))
    f.close()

sys.path.append('Z:/Documents/PythonCode/ternaryplot')
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
x, y=numpy.array([[d['x'], d['y']] for d in dlist if (d['code'])==0]).T
x2, y2=numpy.array([[d['x'], d['y']] for d in dlist if (d['code'])==100]).T
xn, yn=numpy.array([[d['x'], d['y']] for d in dlist if (d['code']%100)!=0]).T
pylab.plot(x, y, 'rs')
pylab.plot(x2, y2, 'bs')
pylab.plot(xn, yn, 'k.')

pylab.show()
