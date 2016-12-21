import numpy,pylab

def rgb_comp(terncoordlist):
    cmy_cmyk=lambda a:a[:3]*(1.-a[3])+a[3]
    rgb_cmy=lambda a:1.-a
    rgb_cmyk=lambda a:rgb_cmy(cmy_cmyk(a))

    return numpy.array([rgb_cmyk(numpy.array(a)) for a in terncoordlist])
        
sc=2.032
#xy=numpy.array([(x,y) for x in numpy.linspace(-25,25,51)  for y in numpy.linspace(-25,25,51) if (x**2+y**2)<(46/sc)**2])
xyfid=numpy.array([[]])
refl=[-15,  1]
#refl=[-13, -5, 3, 11, 19]
rcrit=42.5
ncrit=20
xyf=numpy.array([(x,y) for y in numpy.linspace(25,-25,51)  for x in numpy.linspace(-25,25,51) if (x**2+y**2)<(rcrit/sc)**2 and x>=-ncrit and x<=ncrit and y>=-ncrit and y<=ncrit and (y!=-ncrit) and not (x in refl)])
xypureref=numpy.array([(x,y) for y in numpy.linspace(25,-25,51)  for x in numpy.linspace(-25,25,51) if (x**2+y**2)<(rcrit/sc)**2 and x>=-ncrit and x<=ncrit and y>=-ncrit and y<=ncrit and (y==-ncrit ) and not (x in refl)])#and x in [2, 3, 4, 5]
xyspecref=numpy.array([(x,y) for y in numpy.linspace(25,-25,51)  for x in numpy.linspace(-25,25,51) if (x**2+y**2)<(rcrit/sc)**2 and x>=-ncrit and x<=ncrit and y>=-ncrit and y<=ncrit and (x in refl)])
xypureref*=sc
xyspecref*=sc
dfid=22*sc
xyfid=numpy.array([[-dfid, 0], [dfid, 0], [0, dfid], [-7*sc, -21*sc]])
#xyfid=numpy.array([(0, y) for y in [-dfid, dfid]]+[(x, 0) for x in [-dfid, dfid]])

intervs=20

binarylist_compslist=[]
for i, j in [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]:
    tc=numpy.zeros((intervs+1, 4), dtype='float64')
    tc[:, j]=1.*numpy.arange(intervs+1)/intervs
    tc[:, i]=1.-tc[:, j]
    binarylist_compslist+=[list(tc)]

intervs=20
comps1=[(1.0*c/intervs, 1.0*(intervs-a-c)/intervs, 1.0*a/intervs, 0.) for a in numpy.arange(0,intervs+1)[::-1] for c in numpy.arange(0, intervs+1-a)][::-1]
comps2=[(1.0*c/intervs, 1.0*(intervs-a-c)/intervs, 0, 1.0*a/intervs) for a in numpy.arange(0,intervs+1)[::-1] for c in numpy.arange(0, intervs+1-a)][::-1]
comps3=[(1.0*c/intervs, 0, 1.0*(intervs-a-c)/intervs, 1.0*a/intervs) for a in numpy.arange(0,intervs+1)[::-1] for c in numpy.arange(0, intervs+1-a)][::-1]
comps4=[(0, 1.0*c/intervs, 1.0*(intervs-a-c)/intervs, 1.0*a/intervs) for a in numpy.arange(0,intervs+1)[::-1] for c in numpy.arange(0, intervs+1-a)][::-1]

intervs=8
comps5=[(1.0*b/intervs, 1.0*c/intervs, 1.0*(intervs-a-b-c)/intervs, 1.0*a/intervs) for a in numpy.arange(0,intervs+1)[::-1] for b in numpy.arange(0,intervs+1-a) for c in numpy.arange(0, intervs+1-a-b)][::-1]
comps5=[l for l in comps5 if numpy.array(l).prod()>0.]

compnone=[0., 0., 0., 0.]
colnone=[1., 1., 1.]
spaces=[0, 0, 0, 0, 0, 29, 50, 41, 38, 43, 1]
compsf=[]
colsf=[]
codef=[]
comps1=numpy.array(comps1)
for sp, cd, compsx in zip(spaces, numpy.arange(11, dtype='int32')*100, binarylist_compslist+[comps1, comps2, comps3, comps4, comps5]):
    compsf+=list(compsx)+[compnone]*sp
    colsf+=list(rgb_comp(compsx))+[colnone]*sp
    codef+=[cd]*len(compsx)+[4]*sp


pylab.figure()

comps=compsf[:len(xyf)]
cols=colsf[:len(xyf)]
code=codef[:len(xyf)]

cols=numpy.array(cols)
code=numpy.array(code)
xy=xyf[:len(comps)]*sc

print len(comps), len(xy)

temp=numpy.zeros(16)
temp[4]=1.
comps8pure=numpy.array([temp[i:i+8] for i in [4, 3, 2, 1]])
comps8pureinspec=numpy.array([temp[i:i+8] for i in [0, 4, 0, 3, 0, 2, 0, 8, 0, 7, 0, 6, 0, 5]])
codeinspec=[1, 3, 1, 3, 1, 3, 1, 2, 1, 2, 1, 2, 1, 2]
colinspec=rgb_comp(comps8pureinspec[:, :4]+comps8pureinspec[:, 4:])
colinpure=rgb_comp(comps8pure[:, :4])
codeinpure=[2]*len(colinpure)

comps8pure=numpy.concatenate([comps8pure])
codepure=numpy.concatenate([codeinpure])
colpure=numpy.concatenate([colinpure])

    
rgb_comp(comps1)
sortmetricspec=numpy.array([x*100-y for x, y in xyspecref])
sortindsspec=numpy.argsort(sortmetricspec)
xyspecref=xyspecref[sortindsspec]
comps8spec=[]
codespec=[]
colspec=[]
jshift=0
for i in range(len(xyspecref)):
    if i in [29, 68]:
        jshift+=1
    j=(i-jshift)%len(comps8pureinspec)
    comps8spec+=[comps8pureinspec[j]]
    codespec+=[codeinspec[j]]
    colspec+=[colinspec[j]]

temp=numpy.zeros(4)
comps8=numpy.array([numpy.concatenate([c, temp]) for c in comps])
temp=numpy.zeros(8)
#comps8spec=numpy.array([temp for q in xyspecref])
#xyall=numpy.concatenate([xy, xypureref, xyspecref])
#compall=numpy.concatenate([comps8, comps8pure, comps8spec])
#colall=numpy.concatenate([cols, colpure, colspec])
#codeall=numpy.concatenate([code, codepure, codespec])
xyall=numpy.concatenate([xy])
compall=numpy.concatenate([comps8])
colall=numpy.concatenate([cols])
codeall=numpy.concatenate([code])
sortmetric=numpy.array([-y*100+x for x, y in xyall])
sortinds=numpy.argsort(sortmetric)
xyallsort=xyall[sortinds]
codeallsort=codeall[sortinds]
compallsort=compall[sortinds]
colallsort=colall[sortinds]

xyallsortshift=numpy.array([[x+50., y+50-2.71] for x, y in xyallsort])
xyfidshift=numpy.array([[x+50., y+50-2.71] for x, y in xyfid])

startsmp=1

intfmt=lambda x:'%d' %x
floatarrfmt=lambda x:', '.join(['%.3f' %xx for xx in x])
linestr=lambda smp, xy, cmp, cd:', '.join((intfmt(smp), floatarrfmt(xy), floatarrfmt([1.016, 1.016]), floatarrfmt(cmp), intfmt(cd)))
datastr='\n'.join([linestr(i+startsmp, xy, cmp, cd) for i, (xy, cmp, cd) in enumerate(zip(xyallsortshift, compallsort, codeallsort))])
fidstr=', '.join(['(%.3f, %.3f)' %tuple(xyv) for xyv in xyfidshift])

a='% Xfiducial, Yfiducial='
b=' mm'
c='% Sample, x(mm), y(mm), dx(mm), dy(mm), A(fraction), B(fraction), C(fraction), D(fraction), E(fraction), F(fraction), G(fraction), H(fraction), code(0=sample; 1=spectral reference; 2=ABCD control; 3=EFGH control; 4=half thickness; 5=doublethickness; 10=empty)'
mainstr='%s%s%s\n%s\n%s' %(a, fidstr, b, c, datastr)

fn=r'D:\Google Drive\Documents\CaltechWork\platemaps\genplatemap_100mm_quat10_tern20_v1\genplatemap_100mm_quat10_tern20_v1'


#    f=open(fn+'.txt', mode='w')
#    f.write(mainstr)
#    f.close()


#marks=['s', 's', 's', 'o', 'v', '^', '','','','','.']
def marks(cd):
    dup=cd//100
    cd2=cd%100
    if cd>0 and cd<5:
        return ['', 's', 's', 'o', '.'][cd]
    return (['s']*6+['^', '>', 'v', '<', 's'])[dup]

circ=pylab.Circle((50.,50.-2.71),radius=50,edgecolor='k',lw=1,facecolor='none')
ax=pylab.subplot(111)
ax.add_patch(circ)
pylab.plot([-16.25+50, 16.24+50], [0, 0], 'k-', lw=2)
print set(codeallsort)
for x, y, col, cd in zip(xyallsortshift.T[0],xyallsortshift.T[1], colallsort, codeallsort):

    if cd in [4]:
        pylab.scatter([x], [y],color='k',s=2,marker=marks(cd), edgecolor='k')
    else:
        pylab.scatter([x], [y],color=col,s=14,marker=marks(cd), edgecolor='none')

#pylab.scatter(xypureref.T[0],xypureref.T[1],color='w', edgecolor='r',s=10,marker='s', lw=1)
if len(xyfidshift)>0:
    pylab.plot(xyfidshift.T[0],xyfidshift.T[1],'k+', ms=6)
pylab.xlim(0, 100)
pylab.ylim(0, 100)
ax.set_aspect(1)

lablist=['%d:%d' %(cd, (codeallsort==cd).sum()) for cd in [0, 100, 200, 300, 400, 1, 2, 3, 4]]
pylab.title(','.join(lablist))


#pylab.savefig(fn+'.png', dpi=300)


pylab.show()
