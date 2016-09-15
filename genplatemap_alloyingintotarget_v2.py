import time, copy, pickle
import os, os.path
import sys
import numpy, pylab
import numpy as np
from fcns_generatecompositions import *
sys.path.append('Z:/Documents/PythonCode/JCAP')
from readplatemap import *

modelpath=r'D:\Google Drive\Documents\CaltechWork\platemaps\201608alloy\template.txt'
newpath=r'D:\Google Drive\Documents\CaltechWork\platemaps\201608alloy\alloy_3variations_6alloyels_chanIvolume_v2.txt'

writelines=[]
f=open(modelpath, mode='r')
ls=f.readlines()[:2]
writelines+=[l.strip().replace(', H(fraction)', ', H(fraction), I(fraction)') for l in ls]
f.close()

dlist=readsingleplatemaptxt(modelpath,  returnfiducials=False)

update_d=lambda d, c, ifill, code:d.update(dict([(s, v) for s, v in zip(['A', 'B', 'C', 'D', 'E','F', 'G', 'H'], c)]+[('I', ifill), ('code', code)]))

#
#def mol_comps_chanwts(d, chanwts=None):
#    if chanwts is None:
#        chanwts=d['chanwts']
#    else:
#        chanwts=np.array(chanwts)
#        d={}
#        d['chanwts']=chanwts
#    mol_els=(M*chanwts[:, np.newaxis]).sum(axis=0)
#    comp_els=mol_els/mol_els.sum()
#    d.update(totmols=mol_els.sum(), comp=comp_els, frac_a_in_phase=comp_els[0]/comp_els[:2].sum(), alloy_loading_frac=comp_els[2:].sum()/comp_els.sum(), frac_c_in_alloy=comp_els[2]/comp_els[2:].sum(), totprintvol=chanwts.sum(),chanwts=chanwts,chanwts8=np.array(list(chanwts)+[0,0,0,0]))
#    return d

dlist_no=[]

dlist_un=[]

dlist_bi=[]
#for awt, bwt, cdtotwtlist in [(.5, 0, [.05, .1, .2, .3]), (.45, 0, [.4, .5]), (.5, 0.05, [.05, .1, .2, .3]), (.45, 0.05, [.4, .5]), (.45, 0.1, [.05, .1, .2, .3]), (.4, 0.1, [.4, .5])]:
cl0=[.05, .1, .15, .2, .25, .3]
cl1=[.35, .4, .45, .5]
for awt, bwt, cdtotwtlist in [(.55,0,[]),(.5, 0, cl0), (.45, 0, cl1), (.55,0.05,[]), (.5, 0.05, cl0), (.45, 0.05, cl1), (.5,0.1,[]), (.45, 0.1, cl0), (.4, 0.1,cl1)]:
    chanwts=np.array([awt, bwt, 0., 0.])
    d={}
    d['chanwts']=chanwts
    d.update(chanwts8=np.array(list(chanwts)+[0,0,0,0]))
    #mol_comps_chanwts(d)
    #bin_frac_a_in_phase(d)
    dlist_no+=[d]
        
    for cdtotwt in cdtotwtlist:
        chanwts=np.array([awt, bwt, cdtotwt, 0.])
        d={}
        d['chanwts']=chanwts
        d.update(chanwts8=np.array(list(chanwts)+[0,0,0,0]))
        #mol_comps_chanwts(d)
        #bin_frac_a_in_phase(d)
        dlist_un+=[d]
        if cdtotwt in [.1,.2,.3,.5]:
            if cdtotwt==.2:
                cwts=[.05,.15]
            else:
                cwts=np.arange(0,cdtotwt+.001,.05)[1:-1]
            print '*', cdtotwt
        else:
            cwts=[]
        for cwt in cwts:
            
#            if cdtotwt==.5 and int(round(cwt/.05)) in [2, 4, 6, 8]:
#                print 'skip ', cwt
#                continue
            dwt=cdtotwt-cwt
            chanwts=np.array([awt, bwt, cwt, dwt])
            d={}
            d['chanwts']=chanwts
            d.update(chanwts8=np.array(list(chanwts)+[0,0,0,0]))
            #mol_comps_chanwts(d)
            #bin_frac_a_in_phase(d)
            dlist_bi+=[d]


chanlabs='A B C D E F G H'.split(' ')
def genwts_lab(s):
    if s=='N':
        return np.array([])
    if s=='AB':
        return np.array([d['chanwts8'] for d in dlist_no])
    if len(s)==1:
        i=chanlabs.index(s)
        inds=range(8)
        inds[i]=2
        inds[2]=i
        return np.array([d['chanwts8'][inds] for d in dlist_un])
    i=chanlabs.index(s[0])
    j=chanlabs.index(s[1])
    inds=[0,1,-1,-1,-1,-1,-1,-1]#keep A and B and then use -1 to mean 0 for the rest, then replace the 2 channels with 2 and 3 to get the pre-defined C and D values in the right places
    inds[i]=2
    inds[j]=3
    l=[d['chanwts8'] for d in dlist_no]+[d['chanwts8'][inds] for d in dlist_bi]
    return np.array(l)


mastercomps=numpy.zeros((2112,8),dtype='float32')
mastercode=numpy.ones(2112,dtype='int32')*4

inds0=np.array(range(0,15)+range(16,31))
inds1=np.array(range(32,47)+range(48,63))

codes0=[0,100,200,300,400,500,600,4,4,4,2000,4000,2100,4100,2200,4200,2300,4300,2400,4400,2500,4500,2600,2700,4600,2800]
codes1=[700,800,900,1000,1100,1200,4,4,3000,5000,3100,5100,3200,5200,3300,5300,3400,5400,3500,5500,3600,5600,3700,5700,3800]
labs0='AB,C,D,E,F,G,H,N,N,N,E,EC,C,CF,F,FD,D,DH,H,HE,E,EG,G,F,FH,H'
labs1='C,D,E,F,G,H,N,N,C,CD,D,DE,E,EF,F,FG,G,GC,C,CH,H,HG,G,GD,D'

for cl,lstr,inds in [(codes0,labs0,inds0),(codes1,labs1,inds1)]:
    labl=lstr.split(',')
    j=0
    for cd,lab in zip(cl,labl):
        if lab=='N':
            mastercode[[j*64+15+inds[0],j*64+31+inds[0]]]=1
            j+=1
            continue
        arr=genwts_lab(lab)
        if len(arr)>30:
            arrl=[arr[:30],arr[30:]]
        else:
            arrl=[arr]
        for ar in arrl:
            mastercode[list(j*64+inds[:len(ar)])]=cd
            mastercomps[list(j*64+inds[:len(ar)]),:]=ar[:,:]
            #mastercomps[list(j*64+inds[:15])]=ar[:15,:]
            #mastercomps[list(j*64+inds[15:])]=ar[15:,:]
            mastercode[[j*64+15+inds[0],j*64+31+inds[0]]]=1
            j+=1

I_volfill=1.-mastercomps.sum(axis=1)
I_volfill[mastercode%10!=0]=0


for d, c, ifill, code in zip(dlist,mastercomps, I_volfill, mastercode):
    update_d(d, c, ifill, code)

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
('I','%.3f'),\
('code','%d'),\
]

writelines+=[', '.join([f %d[k] for k, f in k_f]) for d in dlist]
if 1:
    f=open(newpath, mode='w')
    f.write('\n'.join(writelines))
    f.close()

#sys.path.append('Z:/Documents/PythonCode/ternaryplot')
#from myquaternaryutility import QuaternaryPlot
#from myternaryutility import TernaryPlot
#
#for d in dlist:
#    c=numpy.array([d[el] for el in ['A', 'B', 'C', 'D']])
#    if c.sum()>0:
#        c/=c.sum()
#    d['compositions']=c
#
#carr=numpy.array([d['compositions'] for d in dlist])
#stpq=QuaternaryPlot(111)
#stpq.scatter(carr)


pylab.figure()
x, y, c=numpy.array([[d['x'], d['y'], d['code']] for d in dlist if not (d['code'] in [1, 4])]).T
x2, y2=numpy.array([[d['x'], d['y']] for d in dlist if (d['code'])==1]).T

pylab.scatter(x, y, c=c, cmap='jet')
pylab.plot(x2, y2, 'k.')


pylab.show()
