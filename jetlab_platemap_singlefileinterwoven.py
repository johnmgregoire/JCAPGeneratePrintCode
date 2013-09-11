import numpy, os
os.chdir(os.path.split(os.getcwd())[0])
from readplatemap import *



xshift=0.
yshift=0.
fidcomp=numpy.array([.1]*4)

maxdrops=numpy.array([500]*4)

nlinesperwovensegment=150

elnames=['A', 'B', 'C', 'D']
elchannels=[1, 2, 3, 4]
p='C:/Users/Gregoire/Documents/CaltechWork/platemaps/V7.1/playeV7_1_fromDB.txt'
pout='C:/Users/Gregoire/Documents/CaltechWork/platemaps/V7.1/plateV7_1_jetlabsingle150_500drop.txt'
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
ellines=[]
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
    ellines+=[['%.2f %.2f %d %d' %(xv, yv, elch, dr) for xv, yv, dr in zip(x, y, drops)]]

wovenlines=[]
nlines_ch=[len(ellin) for ellin in ellines]
nlines=max(nlines_ch)
nsegs=nlines//nlinesperwovensegment+int(bool(nlines%nlinesperwovensegment))

elchannels1=elchannels+[elchannels[0]]
elchannels2=elchannels[1:]+elchannels[:2]
for i in range(nsegs):
    for ellin, ch in zip(ellines, elchannels):
        if len(wovenlines)==0:
            wovenlines+=['select %d\nbegin' %ch]
        else:
            wovenlines+=['end\nselect %d\nbegin' %ch]
        wovenlines+=ellin[i*nlinesperwovensegment:(i+1)*nlinesperwovensegment]
        
print 'number of individual lines :', numpy.array(nlines_ch).sum()
#print 'number of combined lines: ', len(wovenlines)
print 'number of times rotate through channels',  nsegs
elfilestr=';\n'+'\n'.join(wovenlines)+'\nend'

f=open(pout, mode='w')
f.write(elfilestr)
f.close()
    
