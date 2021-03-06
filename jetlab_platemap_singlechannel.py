import numpy, os
os.chdir(os.path.split(os.getcwd())[0])
from readplatemap import *



xshift=50
yshift=50-2.71
fidcomp=numpy.array([0.])

maxdrops=numpy.array([300]*1)

elnames=['A']
elchannels=[1]
p='C:/Users/Gregoire/Documents/CaltechWork/platemaps/adhesionstudy/adhesionstudy_5thickness7repeats_4inquadrant.txt'
fold='C:/Users/Gregoire/Documents/CaltechWork/platemaps/adhesionstudy/jetlab_4inadhesion_300drop'
dlist, fid=readsingleplatemaptxt(p, returnfiducials=True)

for i, (x, y) in enumerate(fid):
    d={}
    for let, c in zip(elnames, fidcomp):
        d[let]=c
        d['Sample']=-i
    d['x']=x
    d['y']=y
    d['code']=-1
    dlist+=[d]

getarr_dlist=lambda key, inds:numpy.array([dlist[i][key] for i in inds])
for el, elch, maxdr in zip(elnames, elchannels, maxdrops):
    c_el=numpy.array([d[el] for d in dlist])
    inds=numpy.where(c_el>0.)[0]
    smp=getarr_dlist('Sample', inds)
    sortinds=numpy.argsort(smp)
    drops=numpy.int32(numpy.round(getarr_dlist(el, inds)*maxdr))[sortinds]
    x=getarr_dlist('x', inds)[sortinds]
    y=getarr_dlist('y', inds)[sortinds]
    x+=xshift
    y+=yshift
    elfilestr=';\nbegin\n'+'\n'.join(['%.2f %.2f %d %d' %(xv, yv, elch, dr) for xv, yv, dr in zip(x, y, drops)])+'\nend'
    p=os.path.join(fold, el+'.txt')
    f=open(p, mode='w')
    f.write(elfilestr)
    f.close()
    
