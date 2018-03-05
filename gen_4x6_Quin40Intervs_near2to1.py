import time, copy, pickle
import os, os.path
import sys
import numpy, pylab, itertools


wd=os.getcwd()
PyCodePath=os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(PyCodePath)
sys.path.append(os.path.join(PyCodePath,'PythonCompositionPlots'))
from readplatemap import *
from myquaternaryutility import QuaternaryPlot


sp=r'D:\Google Drive\Documents\CaltechWork\platemaps\4x6_40intervs_5els_near2to1\binarytoquinarycomps.pck'
with open(sp, mode='rb') as f:
    comps=pickle.load(f)
    
comps=list(comps)
modelpath=r'D:\Google Drive\Documents\CaltechWork\platemaps\4x6_20intervs_rightcolumnsforcharacterization\0037-04-0730-mp.txt'
newpath=r'D:\Google Drive\Documents\CaltechWork\platemaps\4x6_40intervs_5els_near2to1\4x6_40intervs_5els_near2to1_v1.txt'

writelines=[]
f=open(modelpath, mode='r')
ls=f.readlines()[:2]
writelines+=[l.strip() for l in ls]
f.close()

dlist=readsingleplatemaptxt(modelpath,  returnfiducials=False)


smps=numpy.array([d['Sample'] for d in dlist])
codes=numpy.array([d['code'] for d in dlist])

xset=sorted(list(set([d['x'] for d in dlist])))
xposns_refcolumns=numpy.array(xset)[[7, 15, 23, 31, 39, 47, 55, 63]]#range(7, 64, 8)
xtouse=[x for x in xset if not x in xposns_refcolumns]
[d.update(code=4, A=0, B=0, C=0, D=0, E=0) for d in dlist if d['x'] in xtouse]


xset=sorted(list(set([d['x'] for d in dlist])))
xposns_refcolumns=numpy.array(xset)[range(7, 64, 8)]
#xforchar=xtouse[-14:]
#
#yset=sorted(list(set([d['y'] for d in dlist])))
#yforchar=yset[:16]

inds_char=[]
#inds_char=[count for count, d in enumerate(dlist) if d['x'] in xforchar and d['y'] in yforchar]
#
#inds_char=sorted(inds_char[3:]+[1911, 1975, 2039, 2103])
inds_charpop=copy.copy(inds_char)

inds_main=[count for count, d in enumerate(dlist) if d['code']==4 and not count in inds_char]
inds_mainpop=copy.copy(inds_main)

#intervs=20
##comps=[[1.0*b/intervs, 1.0*c/intervs, 1.0*(intervs-a-b-c)/intervs, 1.0*a/intervs] for a in numpy.arange(0,intervs+1)[::-1] for b in numpy.arange(0,intervs+1-a) for c in numpy.arange(0, intervs+1-a-b)][::-1]
#comps=[[b, c, (intervs-a-b-c), a] for a in numpy.arange(0,intervs+1)[::-1] for b in numpy.arange(0,intervs+1-a) for c in numpy.arange(0, intervs+1-a-b)][::-1]
#compsnotinnertern10=copy.copy(comps)
#ternintervs=10
#compsinnertern=[[2*b, 2*(ternintervs-a-b), 2*a, 0] for a in numpy.arange(1,ternintervs)[::-1] for b in numpy.arange(1,ternintervs-a) ][::-1]
#compstern=numpy.array(compsinnertern)[:, :3]


a=numpy.arange(1, 20, 1, dtype='float64')/20.

compsbin=[]

for i in range(5):
    c=numpy.zeros(5, dtype='float32')
    c[i]=1.
    compsbin+=[copy.copy(c)]
    comps+=[copy.copy(c)]

for i0, i1 in itertools.combinations(range(5), 2):
    c=numpy.zeros(5, dtype='float32')
    for v in a:
        
        c[i0]=v
        c[i1]=1.-v
        compsbin+=[copy.copy(c)]

#for count, t in enumerate(itertools.combinations(range(4),3)):
#    tempcompsinnertern=numpy.zeros((len(compstern), 4), dtype='int32')
#    tempcompsinnertern[:, list(t)]=compstern[:, :]
#    compsnotinnertern10=[c for c in numpy.array(compsnotinnertern10) if not True in [numpy.all(c==cv) for cv in tempcompsinnertern]]
#    code=100*(count+1)
#    for av, bv, cv, dv in tempcompsinnertern:
#        i=inds_charpop.pop(0)
#        dlist[i].update(A=av, B=bv, C=cv, D=dv, code=code)
for av, bv, cv, dv, ev in comps:
    i=inds_mainpop.pop(0)
    dlist[i].update(A=av, B=bv, C=cv, D=dv, E=ev, code=0)

for av, bv, cv, dv, ev in compsbin:
    i=inds_mainpop.pop(-1)
    dlist[i].update(A=av, B=bv, C=cv, D=dv, E=ev, code=100)
    
#for count in range(15):
#    i=inds_charpop.pop(0)
#    dlist[i].update(code=4)
    


    
    
for d in dlist:
#    for k in ['A', 'B', 'C', 'D']:
#        d[k]*=1./intervs
    c=numpy.float64([d[el] for el in ['A', 'B', 'C', 'D']])
    if c.sum()>0:
        c/=c.sum()
        av, bv, cv, dv=c
        d.update(A=av, B=bv, C=cv, D=dv)#assume only full loading samples in this platemap. This replaces /intrv normalization
    d['compositions']=c

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

codeset=sorted(list(set([d['code'] for d in dlist])))
marks=['s', 's', 's', 's','o', 'v', '^', '<','>','o','D','o','D','o','D']



def rgb_comp(cmp):
    cmy_cmyk=lambda a:a[:3]*(1.-a[3])+a[3]
    rgb_cmy=lambda a:1.-a
    rgb_cmyk=lambda a:rgb_cmy(cmy_cmyk(a))

    return rgb_cmyk(cmp)

fig=pylab.figure()
ax=pylab.subplot(111)
ax.set_aspect(1)
for d in dlist:
    mark=marks[codeset.index(d['code'])]
    col=rgb_comp(d['compositions'])
    if d['compositions'].sum()==0:
        pylab.scatter(d['x'], d['y'],color=col,s=14,marker=mark, edgecolor='k')
    else:
        pylab.scatter(d['x'], d['y'],color=col,s=14,marker=mark, edgecolor='none')

for cd, ma in zip(codeset, marks):
    pylab.plot([], [], 'k'+ma, mec='none', label=`cd`)
pylab.subplots_adjust(left=.05, right=.8)
#cbax=pylab.axes([.8, .1, .2, .8])
pylab.legend( loc='center', bbox_to_anchor=(1.1, 0.5), numpoints=1)




pylab.figure()
carr=numpy.array([d['compositions'] for d in dlist])
stpq=QuaternaryPlot(111)
stpq.scatter(carr)
pylab.show()
errortime
