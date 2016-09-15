#reads a platemap file (requires readplatemap.py) and filters samples by code 0 then for each sample 
#then finds all samples within 5% and makes a dictionary with 
#the integer sample number as the key and the list of neighbor sample numbers as the value.
#each sample counts as one if its own neighbors

import os, numpy, pickle, itertools

#dr=os.getcwd()
#os.chdir(os.path.join(os.path.split(dr)[0], 'printingcode'))
from readplatemap import *
#os.chdir(dr)


p=r'Z:\Documents\CaltechWork\platemaps\Epson6Elementcombinations_singleplate\0069-04-0100-mp.txt'
os.chdir(r'Z:\Documents\CaltechWork\platemaps\Epson6Elementcombinations_singleplate\smoothfiltermaps_0069')


dlist=readsingleplatemaptxt(p)

codes=numpy.array([d['code'] for d in dlist])
codes[codes==100]=0 #in this platemap the XRF samples are separated as code 0 but the compsoition space is code 0 and 100 together so for purposes of neighbor ID, marge code 0 and 100.
smps_=numpy.array([d['Sample'] for d in dlist])[codes==0]

lets=numpy.array(['A', 'B', 'C', 'D', 'E', 'F'])
comps_=numpy.array([[d[let] for let in lets] for d in dlist])[codes==0]

#codes=codes[codes==0]

combs4=list(itertools.combinations(range(6),4))



for count, inds4 in enumerate(combs4):
    indsnot2=list(set(range(6)).difference(set(inds4)))
    qautinds=numpy.where(comps_[:, indsnot2].sum(axis=1)==0.)[0]#no quatern comps
    smps=smps_[qautinds]
    comps=comps_[qautinds][:, inds4]
    ellab=''.join(lets[list(inds4)])
    
    p0='0069-04-0100-mp_subspace__%s.pck' %ellab
    dselquat=dict([(smp, [smp]) for smp in smps])
    with open(p0, mode='w') as f:
        pickle.dump(dselquat, f)
    
    
    distfcn=lambda c:numpy.array([((cv-c)**2).sum()**.5/2.**.5 for cv in comps])

    invdim_all=numpy.array([(cv==0.).sum() for cv in comps])
    indeceszero_all=[set(numpy.where(cv==0.)[0]) for cv in comps]
    dneighbor={}
    for smp, comp in zip(smps, comps):
        arr=distfcn(comp)
        invdim=(comp==0.).sum()
        indeceszero=set(numpy.where(comp==0.)[0])
        inds0=numpy.where((arr<0.101)&(invdim_all>=invdim))[0]
        inds1=[i for i in inds0 if indeceszero.issubset(indeceszero_all[i])]
        dneighbor[smp]=list(smps[inds1])
    
    
    p='0069-04-0100-mp_subspace_dneighbor_symm__%s.pck' %ellab
    with open(p, mode='w') as f:
        pickle.dump(dneighbor, f)

    
    if count==11:
        with open(p, mode='r') as f:
            dneighbor=pickle.load(f)
            
        smp=444
        l=numpy.array([len(v) for v in dneighbor.values()])

        x=list(set(l))
        y=[(l==xv).sum() for xv in x]
        pylab.plot(x, y, '.')
        pylab.xlabel('number of neighbors (within 10%)')
        pylab.ylabel('number of samples with that many neighbors')
        pylab.show()

        #example use:
        
        
        data=comps[:, 3]#numpy.random.rand(len(comps))#comps.prod(axis=1)#indexed same as existing array smps.
        datacompave=numpy.array([numpy.array([data[smps==smp2] for smp2 in dneighbor[smp] if smp2 in smps]).mean() for smp in smps])

        #now just demo plot of example data
        datacompave=datacompave[numpy.argsort(data)]
        data=data[numpy.argsort(data)]
        pylab.plot(data, datacompave, 'b.')
        pylab.plot([data.min(), data.max()], [data.min(), data.max()], 'k-')
        pylab.show()

    
