import time, copy, pickle
import os, os.path
import sys, random
import numpy, pylab

sys.path.append('C:/Users/Gregoire/Documents/PythonCode/JCAP')
from readplatemap import *


def writerandomizedplatemap(modelpath, newpath, randcodes):
    writelines=[]
    f=open(modelpath, mode='r')
    ls=f.readlines()[:2]
    writelines+=[l.strip() for l in ls]
    f.close()

    dlist=readsingleplatemaptxt(modelpath,  returnfiducials=False)
    rdlist=copy.deepcopy(dlist)
    ks=dlist[0].keys()
    for rc in randcodes:
        inds=[i for i, d in enumerate(dlist) if d['code']==rc]
        smps=[d['Sample'] for i, d in enumerate(dlist) if d['code']==rc]
        rinds=copy.copy(inds)
        random.shuffle(rinds)
        for i, j, smp in zip(inds, rinds, smps):
            for k in ks:
                if not k in ['Sample', 'x', 'y']:
                    rdlist[i][k]=dlist[j][k]
    #SHIFT Y VALUES
    for d in rdlist:
        d['y']-=2.71
    print set([d['code'] for d in rdlist])
    print len([d['Sample'] for d in rdlist if d['code']==0])
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

    writelines+=[', '.join([f %d[k] for k, f in k_f]) for d in rdlist]

    f=open(newpath, mode='w')
    f.write('\n'.join(writelines))
    f.close()



fold='C:/Users/Gregoire/Documents/CaltechWork/platemaps/'

#for p1 in ['v8/plate500_100mm_v8_pl1.txt', 'v8/plate500_100mm_v8_pl2.txt']:
#    p2=p1.replace('v8', 'v8.2')
#    writerandomizedplatemap(os.path.join(fold, p1), os.path.join(fold, p2), [0, 20, 50])

for p1 in ['v6.2_6.3/plate555_1map_tempfiducialshifted.txt']:
    p2='v6.2_6.3/plate555_randomized.txt'
    writerandomizedplatemap(os.path.join(fold, p1), os.path.join(fold, p2), [0])

#for p1, p2 in zip(['v5.5/0020-04-0541-mp_newcodes.txt', 'v5.5/0021-04-0541-mp_newcodes.txt', 'v5.5/0022-04-0541-mp_newcodes.txt'], \
#                            ['v5.5/plate333_1_v5_5.txt', 'v5.5/plate333_2_v5_5.txt', 'v5.5/plate333_3_v5_5.txt']):
#    writerandomizedplatemap(os.path.join(fold, p1), os.path.join(fold, p2), [0])
    
