import numpy,pylab, os, copy
from collections import Counter


os.chdir(os.path.split(os.getcwd())[0])
from readplatemap import *

def rgb_comp(terncoordlist):
    cmy_cmyk=lambda a:a[:3]*(1.-a[3])+a[3]
    rgb_cmy=lambda a:1.-a
    rgb_cmyk=lambda a:rgb_cmy(cmy_cmyk(a))

    return numpy.array([rgb_cmyk(numpy.array(a)) for a in terncoordlist])


p='C:/Users/Gregoire/Documents/CaltechWork/platemaps/template.txt'
dlist, fid=readsingleplatemaptxt(p, returnfiducials=True)

f=open(p, mode='r')
headlines=f.readlines()[:2]
f.close()

mapsmps=[d['Sample'] for d in dlist]
mapsmpsindex=[]
for count, d in enumerate(dlist[:-32]):
    
    if d['code']==2 or d['code']==3:
        d['code']=1
    if not d['code']==1:
        d['code']=4
        mapsmpsindex+=[count]
    for k in 'ABCDEFGH':
        d[k]=0.
        
        
    



c_L=numpy.concatenate([[0,.24,.36], numpy.linspace(.4,.6,21),[.64,.76,1.]])
c_L_r=copy.copy(c_L)
numpy.random.shuffle(c_L_r)
c_L_r2=copy.copy(c_L_r)
numpy.random.shuffle(c_L_r2)
c_34L=numpy.concatenate([[0,.24,.36], numpy.linspace(.4,.6,16),[.64,.76,1.]])
c_34L_r=copy.copy(c_34L)
numpy.random.shuffle(c_34L_r)
c_34L_r2=copy.copy(c_34L_r)
numpy.random.shuffle(c_34L_r2)
c_12L=numpy.concatenate([[0,.24,.36], numpy.linspace(.4,.6,11),[.64,.76,1.]])
c_12L_r=copy.copy(c_12L)
numpy.random.shuffle(c_12L_r)
c_12L_r2=copy.copy(c_12L_r)
numpy.random.shuffle(c_12L_r2)




code_comps=[(0, c_L_r), (130, c_12L_r2), (70, c_34L_r), (170, c_34L_r2), (30, c_12L_r), (100, c_L_r2)]

blocksmps=[]
blockc=[]
blockcode=[]
for count, (co, c) in enumerate(code_comps):
    si=numpy.arange(len(c))
    if count%2==1:
        si=55-si
    smps=56*(count//2)+si
    blocksmps+=list(smps)
    blockc+=list(c)
    blockcode+=list([co]*len(c))
blankkey='D'
inkkeys_blocks=[['A', 'B'], ['A', 'B'], ['A', 'B'], ['A', 'B'], ['A', 'C'], ['A', 'C'], ['A', 'C'], ['A', 'C']]

for count, (k0, k1) in enumerate(inkkeys_blocks):
    startsmp=0+4*56*count
    for co, c, s in zip(blockcode, blockc, blocksmps):
        i=mapsmpsindex[startsmp+s]#mapsmps.index(startsmp+s)
        thickfact=1.
        if (co%100)//10==3:
            thickfact=0.5
        if (co%100)//10==7:
            thickfact=0.75
        dlist[i][k0]=c*thickfact
        dlist[i][k1]=(1.-c)*thickfact
        dlist[i][blankkey]=1.-thickfact
        dlist[i]['code']=co+(count%4)*200
        comp=numpy.array([dlist[i][k] for k in ['A', 'B', 'C']]+[0.])
        comp/=comp.sum()
        dlist[i]['col']=rgb_comp([comp])[0]


intfmt=lambda x:'%d' %x
floatarrfmt=lambda x:', '.join(['%.3f' %xx for xx in x])
linestr=lambda smp, xy, cmp, cd:', '.join((intfmt(smp), floatarrfmt(xy), floatarrfmt([1.016, 1.016]), floatarrfmt(cmp), intfmt(cd)))
datastr='\n'.join([linestr(d['Sample'], [d['x'], d['y']], [d['A'], d['B'], d['C'], d['D'], 0, 0, 0, 0], d['code']) for d in dlist])
#    fidstr=', '.join(['(%.3f, %.3f)' %tuple(xyv) for xyv in xyfidshift])
#
#    a='% Xfiducial, Yfiducial='
#    b=' mm'
#    c='% Sample, x(mm), y(mm), dx(mm), dy(mm), A(fraction), B(fraction), C(fraction), D(fraction), E(fraction), F(fraction), G(fraction), H(fraction), code(0=sample; 1=spectral reference; 2=ABCD control; 3=EFGH control, 4=half thickness, 5=doublethickness, 10=empty)'
#    mainstr='%s%s%s\n%s\n%s' %(a, fidstr, b, c, datastr)
mainstr=''.join(headlines+[datastr])
fn='C:/Users/Gregoire/Documents/CaltechWork/platemaps/binaryoptimize/binaryplatemap'

f=open(fn+'.txt', mode='w')
f.write(mainstr)
f.close()
    
    

def marks(cd):
    dup=cd//100
    cd=cd%100
    if cd<5:
        return ['s', 's', 's', 'o', '.'][cd]
    if (cd//10)<4:
        return 'v'
    else:
        return '^'
pylab.figure(figsize=(12, 8))
ax=pylab.subplot(111)

for d in dlist:
    if d['code']%10 in [1, 2, 3, 9]:
        pylab.scatter(d['x'], d['y'],color='w',s=14,marker=marks(d['code']), edgecolor='r')
    elif d['code'] in [4]:
        pylab.scatter(d['x'], d['y'],color='k',s=2,marker=marks(d['code']), edgecolor='k')
    else:
        pylab.scatter(d['x'], d['y'],color=d['col'],s=14,marker=marks(d['code']), edgecolor='none')


for l in range(33):
    for lr in [0, 1]:
        if lr==0:
            smps=range(1+l*64, 1+l*64+32)
            ha='right'
            xsh=-2
        else:
            smps=range((1+l)*64, (1+l)*64-32, -1)
            ha='left'
            xsh=2
        cd=[dlist[mapsmps.index(s)]['code'] for s in smps]
        data=Counter(cd)
        repsmp=data.most_common(1)[0][0]
        d=dlist[mapsmps.index(smps[0])]
        pylab.text(d['x']+xsh, d['y'], `repsmp`, ha=ha, va='center', fontsize=9)
#    #pylab.scatter(xypureref.T[0],xypureref.T[1],color='w', edgecolor='r',s=10,marker='s', lw=1)
#    if len(xyfidshift)>0:
#        pylab.plot(xyfidshift.T[0],xyfidshift.T[1],'k+', ms=6)
pylab.xlim(0, 150)
pylab.ylim(0, 100)
ax.set_aspect(1)

codeall=numpy.array([d['code'] for d in dlist])
lablist=['%d:%d' %(cd, (codeall==cd).sum()) for cd in set(codeall)]
labstr='\n'.join([','.join(lablist[i*6:(i+1)*6]) for i in range(len(lablist)//6+1)])
pylab.title(labstr)
pylab.subplots_adjust(top=.6, bottom=.02)

pylab.savefig(fn+'.png', dpi=300)
    

pylab.show()
