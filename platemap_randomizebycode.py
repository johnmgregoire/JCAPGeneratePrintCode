import time, copy, pickle
import os, os.path
import sys, random
import numpy, pylab

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
        
        
    k_f=[\
    ('Sample','%04d'),\
    ('x','%.3f'),\
    ('y','%.3f'),\
    ('dx','%.3f'),\
    ('dx','%.3f'),\
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



fold=r'D:\Google Drive\Documents\CaltechWork\platemaps\genplatemap_100mm_quat10_tern20'

#for p1 in ['v8/plate500_100mm_v8_pl1.txt', 'v8/plate500_100mm_v8_pl2.txt']:
#    p2=p1.replace('v8', 'v8.2')
#    writerandomizedplatemap(os.path.join(fold, p1), os.path.join(fold, p2), [0, 20, 50])

#for p1 in ['v7.3/playeV7_1_newcodes.txt']:
#    p2='v7.3/playeV7_3.txt'
#    writerandomizedplatemap(os.path.join(fold, p1), os.path.join(fold, p2), [0, 100])

#for p1, p2 in zip(['v5.5/0020-04-0541-mp_newcodes.txt', 'v5.5/0021-04-0541-mp_newcodes.txt', 'v5.5/0022-04-0541-mp_newcodes.txt'], \
#                            ['v5.5/plate333_1_v5_5.txt', 'v5.5/plate333_2_v5_5.txt', 'v5.5/plate333_3_v5_5.txt']):
#    writerandomizedplatemap(os.path.join(fold, p1), os.path.join(fold, p2), [0])

#for p1 in ['100mm_4copies10interv/100mm_4copies10interv1.txt']:
#    p2='100mm_4copies10interv/100mm_4copies10interv1_random.txt'
#    writerandomizedplatemap(os.path.join(fold, p1), os.path.join(fold, p2), [0, 20, 30, 130])

#for p1 in ['Dstep1percent/Dstep1percent.txt']:
#    p2='Dstep1percent/Dstep1percent_randomized.txt'
#    writerandomizedplatemap(os.path.join(fold, p1), os.path.join(fold, p2), [0])

#for p1 in ['Epson6Elementcombinations/Epson6Elementcombinations_plate1.txt']:
#    p2=p1[:-4]+'_randomized.txt'
#    writerandomizedplatemap(os.path.join(fold, p1), os.path.join(fold, p2), numpy.arange(30)*100)
#for p1 in ['Epson6Elementcombinations/Epson6Elementcombinations_plate2.txt']:
#    p2=p1[:-4]+'_randomized.txt'
#    writerandomizedplatemap(os.path.join(fold, p1), os.path.join(fold, p2), numpy.arange(20)*100)
    

#for p1 in ['Epson6Elementcombinations_singleplate\Epson6Elementcombinations_4els_10steps.txt']:
#    p2=p1[:-4]+'_randomized.txt'
#    writerandomizedplatemap(os.path.join(fold, p1), os.path.join(fold, p2), [0])
#for p1 in ['Epson6Elementcombinations_singleplate\Epson6Elementcombinations_4els_10steps_156compsseparate.txt']:
#    p2=p1[:-4]+'_randomized.txt'
#    writerandomizedplatemap(os.path.join(fold, p1), os.path.join(fold, p2), [0, 100])   

#for p1 in ['alloy_3variations_6alloyels_chanIvolume_v2.txt']:
#    p2=p1[:-4]+'_randomized.txt'
#    writerandomizedplatemap(os.path.join(fold, p1), os.path.join(fold, p2), \
#    [2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 3000, 3100, 3200, 3300, 3400, 3500, 3600, 3700, 3800, 4000, 4100, 4200, 4300, 4400, 4500, 4600, 5000, 5100, 5200, 5300, 5400, 5500, 5600, 5700]\
#    )#0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 

for p1 in ['genplatemap_100mm_quat10_tern20_v3.txt']:
    p2=p1[:-4]+'_randomized.txt'
    writerandomizedplatemap(os.path.join(fold, p1), os.path.join(fold, p2), \
    [600, 700, 800, 900, 1000]\
    )#0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 
    
