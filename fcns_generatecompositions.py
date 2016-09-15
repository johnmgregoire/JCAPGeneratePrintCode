import time, copy, pickle, itertools
import os, os.path
import sys
import numpy, pylab

def genbinarycomps(intervs, elind1, elind2, ndim=4):
    aa=numpy.linspace(0.,1.,intervs+1)
    c=numpy.zeros((len(aa), ndim), dtype='float64')
    c[:, elind1]=aa
    c[:, elind2]=1.-aa
    return c
    
def inner_4(intervs):
    return numpy.float32([(b, c, intervs-a-b-c, a) for a in range(1,intervs)[::-1] for b in range(1,intervs-a) for c in range(1,intervs-a-b) if (intervs-a-b-c)>0 and (intervs-a-b-c)<intervs][::-1])/intervs

def all_4(intervs):
    return numpy.float32([(b, c, intervs-a-b-c, a) for a in numpy.arange(0,intervs+1)[::-1] for b in numpy.arange(0,intervs+1-a) for c in numpy.arange(0, intervs+1-a-b)][::-1])/intervs
    

def inner_3(intervs):
    return numpy.float32([(b, intervs-a-b, a) for a in range(1,intervs) for b in range(1,intervs-a) if (intervs-a-b)>0 and (intervs-a-b)<intervs][::-1])/intervs

def all_3(intervs):
    return numpy.float32([(b, intervs-a-b, a) for a in numpy.arange(0,intervs+1)[::-1] for b in numpy.arange(0,intervs+1-a)][::-1])/intervs

def inner_2(intervs):
    return numpy.float32([(intervs-a, a) for a in range(1,intervs)][::-1])/intervs

def all_2(intervs):
    return numpy.float32([(intervs-a, a) for a in numpy.arange(0,intervs+1)[::-1]][::-1])/intervs
    

def combi_6el_inner4(intervs, codes=None):
    combs4=list(itertools.combinations(range(6),4))
    c4=inner_4(intervs)
    nper=len(c4)
    c6=numpy.zeros((len(combs4)*nper, 6), dtype='float32')
    for count, inds4 in enumerate(combs4):
        c6[count*nper:(count+1)*nper, inds4]=c4[:, :]
    if not codes:
        return c6
    if codes=='blocks as duplicates':
        co=[]
        for count in range(len(c6)//nper):
            co+=[count*100]*nper
    return c6, numpy.array(co)

def combi_6el_inner3(intervs, codes=None):
    combs3=list(itertools.combinations(range(6),3))
    c3=inner_3(intervs)
    nper=len(c3)
    c6=numpy.zeros((len(combs3)*nper, 6), dtype='float32')
    for count, inds3 in enumerate(combs3):
        c6[count*nper:(count+1)*nper, inds3]=c3[::-1, :]
    if not codes:
        return c6
    if codes=='blocks as duplicates':
        co=[]
        for count in range(len(c6)//nper):
            co+=[count*100]*nper
    return c6, numpy.array(co)

def combi_6el_inner2(intervs, codes=None):
    combs2=list(itertools.combinations(range(6),2))
    c2=inner_2(intervs)
    nper=len(c2)
    c6=numpy.zeros((len(combs2)*nper, 6), dtype='float32')
    for count, inds2 in enumerate(combs2):
        c6[count*nper:(count+1)*nper, inds2]=c2[::-1, :]
    if not codes:
        return c6
    if codes=='blocks as duplicates':
        co=[]
        for count in range(len(c6)//nper):
            co+=[count*100]*nper
    return c6, numpy.array(co)

def combi_6el_inner1(intervs, codes=None):
    ctemp=numpy.zeros(11, dtype='float32')
    ctemp[5]=1.
    c6=numpy.float32([ctemp[i:i+6] for i in range(5, -1, -1)])
    if not codes:
        return c6
    return c6, numpy.array([0]*len(c6))
    
def combi_6el_all3(intervs, codes=None):
    combs3=list(itertools.combinations(range(6),3))
    c3=all_3(intervs)
    nper=len(c3)
    c6=numpy.zeros((len(combs3)*nper, 6), dtype='float32')
    for count, inds3 in enumerate(combs3):
        c6[count*nper:(count+1)*nper, inds3]=c3[:, :]
    if not codes:
        return c6
#    co=numpy.zeros(len(combs2)*nper, dtype='int32')
    if codes=='blocks as duplicates':
        co=[]
        for count in range(len(c6)//nper):
            co+=[count*100]*nper
    return c6, numpy.array(co)
    
def combi_6el_all2(intervs, codes=None):
    combs2=list(itertools.combinations(range(6),2))
    c2=all_2(intervs)
    nper=len(c2)
    c6=numpy.zeros((len(combs2)*nper, 6), dtype='float32')
    for count, inds2 in enumerate(combs2):
        c6[count*nper:(count+1)*nper, inds2]=c2[:, :]
    if not codes:
        return c6
#    co=numpy.zeros(len(combs2)*nper, dtype='int32')
    if codes=='blocks as duplicates':
        co=[]
        for count in range(len(c6)//nper):
            co+=[count*100]*nper
    return c6, numpy.array(co)

def get_custom_select_comps_6els_5intervs():
    #unary
    comps=[[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0][i:i+6] for i in [5, 4, 3, 2, 1, 0]]
    #binary
    perm2=list(itertools.combinations(range(6),2))
    for count, tup in enumerate(perm2):
        tup=list(tup)
        for i in tup:
            c0=numpy.zeros(6, dtype='float32')
            c0[tup]=.2
            c0[i]=.8
            comps+=[c0]
    #tern
    perm3=list(itertools.combinations(range(6),3))
    for count, tup in enumerate(perm3):
        tup=list(tup)
        for i in tup:
            c0=numpy.zeros(6, dtype='float32')
            c0[tup]=.2#set all 3 of ternary space to 0.2
            c0[i]=.6#then change 1 of them to 0.6
            comps+=[c0]
    #quat
    perm4=list(itertools.combinations(range(6),4))
    for count, tup in enumerate(perm4):
        tup=list(tup)
        for i in tup:
            c0=numpy.zeros(6, dtype='float32')
            c0[tup]=.2#set all 3 of ternary space to 0.2
            c0[i]=.4#then change 1 of them to 0.6
            comps+=[c0]
    return numpy.array(comps)
sys.path.append('C:/Users/Gregoire/Documents/PythonCode/ternaryplot')
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
#
#pylab.figure()
#for count, tv in enumerate(comps_d):
#    stpq=TernaryPlot((4, 2, count+1))
#    tvnorm=[tvv/tvv.sum() for tvv in tv]
#    stpq.scatter(tvnorm, marker='.', c='r', edgecolor='none')
#    if count<5:
#        ttt=tc
#    else:
#        ttt=tc19
#    stpq.scatter(ttt, marker='.', c='g', edgecolor='none')
#
#pylab.show()

#####################
#indsnonz=[[i,j] for i in range(6) for j in range(i,6)]
#crotate2=[]
#for inds in indsnonz:
#    z=numpy.zeros(6, dtype='float32')
#    z[inds]=1.
#    z/=z.sum()
#    crotate2+=[z]
#    
#indsnonz=[i for i in range(-1, 6)]
#indsnonz=indsnonz*5
#indsnonz=indsnonz[1:]
#ccompref=[]
#for inds in indsnonz:
#    z=numpy.zeros(6, dtype='float32')
#    if inds>=0:
#        z[inds]=1.
#    ccompref+=[z]



        
