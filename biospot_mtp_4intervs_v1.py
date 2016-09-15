import numpy,pylab, os

def rgb_comp(terncoordlist):
    cmy_cmyk=lambda a:a[:3]*(1.-a[3])+a[3]
    rgb_cmy=lambda a:1.-a
    rgb_cmyk=lambda a:rgb_cmy(cmy_cmyk(a))

    return numpy.array([rgb_cmyk(numpy.array(a)) for a in terncoordlist])
        



def make_biospot_file__mtpbysample(comps, saveroot, maxndrops=4):
    nlayers=numpy.max(1./comps[comps>0.])
    if maxndrops%nlayers!=0:
        print 'cannot print max %d drops because not commensurate with %d drop intervals' %(maxndrops, nlayers)
        rasieerror
    ndropsperlayer=maxndrops//nlayers
    print 'Print %d drops per layer' %ndropsperlayer
    intcomps=numpy.int32(numpy.array(comps)*nlayers)
    layerchannels_intcomps=[['%d' %(channind+1) for channind, nlay in enumerate(ic) for repeatind in range(nlay)] for ic in intcomps]
    l_bodystr=[]
    for layerind in range(nlayers):
        intlines=[['%d' %(count+1)] for count in range(48)]
        for colind in range(32):
            for rowind in range(48):
                smpind=colind*48+rowind
                wellprintlist=layerchannels_intcomps[smpind]
                intlines[rowind]+=['0' if len(wellprintlist)==0 else wellprintlist.pop(0)]
        l_bodystr+=[';\n'.join([';'.join(il) for il in intlines[::-1]])]
    
    headstr='MTP1536,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n,Aa,Ab,Ac,Ad,Ba,Bb,Bc,Bd,Ca,Cb,Cc,Cd,Da,Db,Dc,Dd,Ea,Eb,Ec,Ed,Fa,Fb,Fc,Fd,Ga,Gb,Gc,Gd,Ha,Hb,Hc,Hd\n'
    for layercount, bodystr in enumerate(l_bodystr):
        s=headstr+bodystr+';\n'
        with open('%s_%d.csv' %(saveroot, layercount+1), mode='w') as f:
            f.write(s)

sc=2.25
xshift=-(48.-1)/2.*sc+3*25.4
yshift=-(32.-1)/2.*sc+2*25.4
xyf=numpy.array([(x*sc+xshift,y*sc+yshift) for y in numpy.arange(32)[::-1]  for x in numpy.arange(48)])*2.5

#xyfid=numpy.array([(0, y) for y in [-dfid, dfid]]+[(x, 0) for x in [-dfid, dfid]])
intervs=4
comps1=[(1.0*b/intervs, 1.0*c/intervs, 1.0*(intervs-a-b-c)/intervs, 1.0*a/intervs) for a in numpy.arange(0,intervs+1)[::-1] for b in numpy.arange(0,intervs+1-a) for c in numpy.arange(0, intervs+1-a-b)][::-1]

intervs=2
comps2=[(1.0*b/intervs, 1.0*c/intervs, 1.0*(intervs-a-b-c)/intervs, 1.0*a/intervs) for a in numpy.arange(0,intervs+1)[::-1] for b in numpy.arange(0,intervs+1-a) for c in numpy.arange(0, intervs+1-a-b)][::-1]

comps1=numpy.array(comps1)
comps2=numpy.array(comps2)
cols1=list(rgb_comp(comps1))
cols2=list(rgb_comp(comps2))
compnone=[0., 0., 0., 0.]
colnone=[1., 1., 1.]

comps=numpy.zeros((1536, 4), dtype='float32')
code=numpy.zeros(1536, dtype='int32')+4

print 'MTP column# from left or right = hoizontal plate row# from the top or bottom:'

for colind in [0, 1]:
    print '%d is %s' %(colind+1, '12 repeats of A,B,C,D with 1 drop')
    for ind in [colind, 31-colind]:
        for rowind, smpind in enumerate(numpy.arange(48)+48*ind):
            comps[smpind, rowind%4]=0.25

colind=3
print '%d is %s' %(colind+1, '6 repeats of A,B,C,D in every other well with 2 drops')
for ind in [colind, 31-colind]:
    for rowind, smpind in enumerate(numpy.arange(48)+48*ind):
        if rowind%2==1:
            continue
        comps[smpind, (rowind//2)%4]=0.5

colind=5
print '%d is %s' %(colind+1, '6 repeats of A,B,C,D in every other well with 4 drops')
for ind in [colind, 31-colind]:
    for rowind, smpind in enumerate(numpy.arange(48)+48*ind):
        if rowind%2==1:
            continue
        comps[smpind, (rowind//2)%4]=1

colind=7
print '%d is %s' %(colind+1, '10 samples wit 100% and 50-50% in every other well with 2 drops from -y and with 4 drops from +y')
for ind in [colind, 31-colind]:
    for rowind, smpind in enumerate(numpy.arange(48)+48*ind):
        if rowind%2==1:
            continue
        if rowind//2<len(comps2):
            compspaceind=(rowind//2)
            comps[smpind]=comps2[compspaceind]/2.
            continue
        rowind=47-rowind
        if rowind//2<len(comps2):
            compspaceind=(rowind//2)
            comps[smpind]=comps2[compspaceind]
            continue
       

for colind in [9, 11, 13]:
    print '%d is %s' %(colind+1, 'systematic 36 ABCD samples with 4 intervals and 4 drops')
    for ind in [colind, 31-colind]:
        for rowind, smpind in enumerate(numpy.arange(48)+48*ind):
            if rowind==len(comps1):
                break
            comps[smpind]=comps1[rowind]
for colind in [10, 12, 14]:
    print '%d is %s' %(colind+1, 'reverse-systematic 36 ABCD samples with 4 intervals and 4 drops')
    for ind in [colind, 31-colind]:
        for rowind, smpind in enumerate(numpy.arange(48)+48*ind):
            if rowind==len(comps1):
                break
            comps[smpind]=comps1[len(comps1)-rowind-1]

code[comps.sum(axis=1)>0]=0


intfmt=lambda x:'%d' %x
floatarrfmt=lambda x:', '.join(['%.3f' %xx for xx in x])
linestr=lambda smp, xy, cmp, cd:', '.join((intfmt(smp), floatarrfmt(xy), floatarrfmt([1.0, 1.0]), floatarrfmt(cmp), floatarrfmt([0.]*4), intfmt(cd)))
datastr='\n'.join([linestr(i+1, xy, cmp, cd) for i, (xy, cmp, cd) in enumerate(zip(xyf, comps, code))])

a='% Xfiducial, Yfiducial=[]'
b=' mm'
c='% Sample, x(mm), y(mm), dx(mm), dy(mm), A(fraction), B(fraction), C(fraction), D(fraction), E(fraction), F(fraction), G(fraction), H(fraction), code(0=sample; 1=spectral reference; 2=ABCD control; 3=EFGH control; 4=half thickness; 5=doublethickness; 10=empty)'
mainstr='%s%s\n%s\n%s' %(a,  b, c, datastr)
    
os.chdir(r'D:\Google Drive\Documents\CaltechWork\platemaps\20160729_biospotv1')
fn='biospot_v1_platemap'

f=open(fn+'.txt', mode='w')
f.write(mainstr)
f.close()

make_biospot_file__mtpbysample(comps, 'biospot_v1_mtpbysmp', maxndrops=4)
