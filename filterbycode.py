from readplatemap import *

dlist=readplatemaptxt()

samps=[d['Sample'] for d in dlist]

p='C:/Users/Gregoire/Documents/CaltechWork/NiFeCoCepapers/ees table/allfig1data.txt'
ps='C:/Users/Gregoire/Documents/CaltechWork/NiFeCoCepapers/ees table/allfig1datacode0.txt'

f=open(p, mode='r')
ls=f.readlines()
f.close()

code0lines=[ls[0]]

for l in ls[1:]:
    sstr=l.partition('\t')[0]
    if eval(sstr) in samps:
        code0lines+=[l]


f=open(ps, mode='w')
f.write(''.join(code0lines))
f.close()
