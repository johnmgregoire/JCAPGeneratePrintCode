import time, copy, pickle
import os, os.path
import sys
import numpy, pylab
from fcns_generatecompositions import *
sys.path.append('Z:/Documents/PythonCode/JCAP')
from readplatemap import *

modelpath='Z:/Documents/CaltechWork/platemaps/Epson6Elementcombinations/xx0037-04-0730-mp_all0.txt'
newpath='Z:/Documents/CaltechWork/platemaps/Epson6Elementcombinations/Epson6Elementcombinations_plate2.txt'

writelines=[]
f=open(modelpath, mode='r')
ls=f.readlines()[:2]
writelines+=[l.strip() for l in ls]
f.close()

dlist=readsingleplatemaptxt(modelpath,  returnfiducials=False)

indforstartingsystematicbianries=30*8*8
for count, d in enumerate(dlist):
    if d['code']==100 or d['code']==4 or d['code']==4:
        d['code']=4
    if d['code']==0:
        for k in ['A', 'B', 'C', 'D', 'E','F', 'G', 'H']:
            d[k]=0
        if count<indforstartingsystematicbianries:
            d['code']=4
zc=numpy.zeros(6., dtype='float32')




relinds_terncomps=numpy.array([i*8*8+j for i in range(5) for j in range(7)+range(8,15)])

startindex=[i+j*8*8*6 for j in range(5) for i in [0, 16, 32, 48]]

combs3=list(itertools.combinations(range(6),3))
c3=all_3(10)
nper=len(c3)

lastusedcode=0
for count, inds3 in enumerate(combs3):
    c6=numpy.zeros((nper, 6), dtype='float32')
    c6[:, inds3]=c3[:, :]
    popinds=list(startindex[count]+relinds_terncomps)
    for c in c6:
        i=popinds.pop(0)
        d=dlist[i]
        for k, v in zip(['A', 'B', 'C', 'D', 'E','F'], c):
            d[k]=v
        d['code']=count*100
    lastusedcode=count*100
    for i in popinds:
        d=dlist[i]
        for k, v in zip(['A', 'B', 'C', 'D', 'E','F'], c):
            d[k]=0
        d['code']=4
    

#additionalnotusedinds=[max(popinds)]

#additionalnotusedinds=[i+j*8*8+k*8 for j in [5,11,17,23,30] for k in range(8) for i in range(7)]
#for i in additionalnotusedinds:
#    d=dlist[i]
#    for k in ['A', 'B', 'C', 'D', 'E','F']:
#        d[k]=0
#    d['code']=4


codes=[]
comps=[]

c6, co=combi_6el_all2(10, codes='blocks as duplicates')
co+=lastusedcode+100
for i in range(3):
    codes+=list(co[i*55:(i+1)*55])+[4]
    comps+=list(c6[i*55:(i+1)*55])+[zc]



comps2pop=copy.copy(comps)
codespop=copy.copy(codes)

for count, d in enumerate(dlist[indforstartingsystematicbianries:]):
    if d['code']==0:
        if len(comps2pop)==0:
            c=[0.]*6
            cd=4
        else:
            c=comps2pop.pop(0)
            cd=codespop.pop(0)
        for k, v in zip(['A', 'B', 'C', 'D', 'E','F'], c):
            d[k]=v
        d['code']=cd

#change all code 2 and 3 to be code 2 and rotate through 6 compositions
inds=[count for count, d in enumerate(dlist) if d['code'] in [2, 3]]
for count, i in enumerate(inds):
    for k in ['A', 'B', 'C', 'D', 'E','F', 'G', 'H']:
        dlist[i][k]=0.
    k=['A', 'B', 'C', 'D', 'E','F'][count%6]
    dlist[i][k]=1.
    dlist[i]['code']=2

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
x, y=numpy.array([[d['x'], d['y']] for d in dlist if (d['code']%100)==0]).T
xn, yn=numpy.array([[d['x'], d['y']] for d in dlist if (d['code']%100)!=0]).T
pylab.plot(x, y, 'rs')
pylab.plot(xn, yn, 'k.')

pylab.show()
