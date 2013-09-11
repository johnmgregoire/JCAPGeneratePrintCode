import numpy, os
os.chdir(os.path.split(os.getcwd())[0])
from readplatemap import *



xshift=0.
yshift=0.
fidcomp=numpy.array([.1]*4)

maxdr=300

elnames_sum=['A', 'B', 'C', 'D']
elch=1
p='C:/Users/Gregoire/Documents/CaltechWork/platemaps/V7.1/playeV7_1_fromDB.txt'
pout='C:/Users/Gregoire/Documents/CaltechWork/platemaps/V7.1/plateV7_1_jetlabwetting_300drop.txt'
dlist, fid=readsingleplatemaptxt(p, returnfiducials=True)

for i, (x, y) in enumerate(fid):
    d={}
    for let, c in zip(elnames_sum, fidcomp):
        d[let]=c
        d['Sample']=-i
    d['x']=x
    d['y']=y
    d['code']=-1
    dlist+=[d]

getarr_dlist=lambda key, inds:numpy.array([dlist[i][key] for i in inds])

c_el=numpy.array([numpy.sum([d[el] for el in elnames_sum]) for d in dlist])
inds=numpy.where(c_el>0.)[0]
smp=getarr_dlist('Sample', inds)
sortinds=numpy.argsort(smp)
drops=numpy.int32(numpy.round(numpy.sum([getarr_dlist(el, inds) for el in elnames_sum], axis=0)*maxdr))[sortinds]
x=getarr_dlist('x', inds)[sortinds]
y=getarr_dlist('y', inds)[sortinds]
x+=xshift
y+=yshift
elfilestr=';\nbegin\n'+'\n'.join(['%.2f %.2f %d %d' %(xv, yv, elch, dr) for xv, yv, dr in zip(x, y, drops)])+'\nend'

f=open(pout, mode='w')
f.write(elfilestr)
f.close()
    
