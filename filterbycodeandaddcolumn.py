from readplatemap import *

dlist=readplatemaptxt()

samps=[d['Sample'] for d in dlist]

p='C:/Users/Gregoire/Documents/CaltechWork/NiFeCoCepapers/ees table/allfig1data.txt'
padd='C:/Users/Gregoire/Documents/CaltechWork/NiFeCoCepapers/ees table/allcp10data.txt'
ps='C:/Users/Gregoire/Documents/CaltechWork/NiFeCoCepapers/ees table/allfig1cp10datacode0.txt'

f=open(p, mode='r')
ls=f.readlines()
f.close()

f=open(padd, mode='r')
lsadd=f.readlines()
f.close()
sadd=[]
nadd=[]
for l in lsadd[1:]:
    sadd+=[eval(l.partition('\t')[0].strip())]
    nadd+=[l.rpartition('\t')[2].strip()]

code0lines=[ls[0]]

for l in ls[1:]:
    sstr=l.partition('\t')[0]
    s=eval(sstr)
    if s in samps:
        if s in sadd:
            l=l[:-1]+'\t'+nadd[sadd.index(s)]
        else:
            l=l[:-1]+'\tnan'
        code0lines+=[l]


f=open(ps, mode='w')
f.write('\n'.join(code0lines))
f.close()
