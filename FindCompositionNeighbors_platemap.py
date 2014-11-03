#reads a platemap file (requires readplatemap.py) and filters samples by code 0 then for each sample 
#then finds all samples within 5% and makes a dictionary with 
#the integer sample number as the key and the list of neighbor sample numbers as the value.
#each sample counts as one if its own neighbors

import os, numpy, pickle

#dr=os.getcwd()
#os.chdir(os.path.join(os.path.split(dr)[0], 'printingcode'))
from readplatemap import *
#os.chdir(dr)


p='C:/Users/Gregoire/Documents/CaltechWork/platemaps/0037-04-0730-mp.txt'

dlist=readsingleplatemaptxt(p)

codes=numpy.array([d['code'] for d in dlist])

smps=numpy.array([d['Sample'] for d in dlist])[codes==0]

comps=numpy.array([[d[let] for let in ['A', 'B', 'C', 'D']] for d in dlist])[codes==0]

codes=codes[codes==0]

distfcn=lambda c:numpy.array([((cv-c)**2).sum()**.5/2.**.5 for cv in comps])

dneighbor={}
for smp, comp in zip(smps, comps):
    arr=distfcn(comp)
    dneighbor[smp]=list(smps[arr<0.051])
    
fn=os.path.split(p)[1][:-4]+'_dneighbor.pck'
f=open(fn, mode='w')
pickle.dump(dneighbor, f)
f.close()

smp=444
l=numpy.array([len(v) for v in dneighbor.values()])

x=list(set(l))
y=[(l==xv).sum() for xv in x]
pylab.plot(x, y, '.')
pylab.xlabel('number of neighbors (within 5%)')
pylab.ylabel('number of samples with that many neighbors')
pylab.show()

#example use:
f=open(fn, mode='r')
dneighbor=pickle.load(f)
f.close()
data=comps.prod(axis=1)#indexed same as existing array smps.
datacompave=numpy.array([numpy.array([data[smps==smp2] for smp2 in dneighbor[smp] if smp2 in smps]).mean() for smp in smps])

#now just demo plot of example data
datacompave=datacompave[numpy.argsort(data)]
data=data[numpy.argsort(data)]
pylab.plot(data, datacompave, 'b.')
pylab.plot([data.min(), data.max()], [data.min(), data.max()], 'k-')
pylab.show()
