import numpy,pylab

def rgb_comp(terncoordlist):
    cmy_cmyk=lambda a:a[:3]*(1.-a[3])+a[3]
    rgb_cmy=lambda a:1.-a
    rgb_cmyk=lambda a:rgb_cmy(cmy_cmyk(a))

    return numpy.array([rgb_cmyk(numpy.array(a)) for a in terncoordlist])

plateradius=2.5*25.4/2.        
sc=2.032
#xy=numpy.array([(x,y) for x in numpy.linspace(-25,25,51)  for y in numpy.linspace(-25,25,51) if (x**2+y**2)<(46/sc)**2])
xyfid=numpy.array([[]])

rcrit=24.5
ncrit=12
xyall=numpy.array([(x,y) for y in numpy.linspace(ncrit,-ncrit,2*ncrit+1)  for x in numpy.linspace(-ncrit,ncrit,2*ncrit+1) if (x**2+y**2)<(rcrit/sc)**2])
xynotcrit=numpy.array([(x,y) for y in numpy.linspace(ncrit,-ncrit,2*ncrit+1)  for x in numpy.linspace(-ncrit,ncrit,2*ncrit+1) if (x**2+y**2)<(rcrit/sc)**2 and x>-ncrit and x<ncrit and y>-ncrit and y<ncrit])
print len(xyall)

numrefs=len(xynotcrit)-404
numrefspersectiononends=0
numrefsinsmallsections=16
numrefsinmiddle=numrefs-2*numrefsinsmallsections
fr=1./numrefsinsmallsections
ref_inds1=numpy.round(numpy.linspace(fr, 1.-fr, numrefsinsmallsections)*(202.+numrefsinsmallsections))


starti=202+numrefsinsmallsections+numrefspersectiononends
middleinds=range(starti, starti+numrefsinmiddle)
starti+=numrefsinmiddle
ref_inds1=numpy.concatenate([ref_inds1, ref_inds1+starti])
ref_inds1=numpy.concatenate([ref_inds1, middleinds])
#ref_inds=numpy.concatenate([ref_inds, numpy.where(xyall[:, 0]==ncrit)[0]])
#ref_inds=numpy.concatenate([ref_inds, numpy.where(xyall[:, 1]==ncrit)[0]])
ref_inds1=numpy.int32(ref_inds1)
ref_inds=[numpy.argmin((xyall[:, 0]-xv)**2+(xyall[:, 1]-yv)**2) for xv, yv in xynotcrit[ref_inds1]]
ref_inds+=[i for i, (xv, yv) in enumerate(xyall) if numpy.min((xynotcrit[:, 0]-xv)**2+(xynotcrit[:, 1]-yv)**2)>0.]
#ref_inds=sorted(list(numpy.int32(ref_inds)))
ref_inds=sorted(list(numpy.int32(ref_inds)))

compinds=[i for i in range(len(xyall)) if not i in ref_inds]

xyall=xyall*sc
xyf=xyall[compinds]

xypureref=numpy.array([])#[(x,y) for y in numpy.linspace(25,-25,51)  for x in numpy.linspace(-25,25,51) if (x**2+y**2)<(rcrit/sc)**2 and x>=-ncrit and x<=ncrit and y>=-ncrit and y<=ncrit and (y==-ncrit ) and not (x in refl)])#and x in [2, 3, 4, 5]
xyspecref=xyall[ref_inds] #numpy.array([(x,y) for y in numpy.linspace(15,-15,31)  for x in numpy.linspace(-15,15,31) if (x**2+y**2)<(rcrit/sc)**2 and x>=-ncrit and x<=ncrit and y>=-ncrit and y<=ncrit and (x in refl)])
xypureref*=sc
xyspecref*=sc
dfid=13.5*sc
xyfid=numpy.array([[-dfid, 0], [dfid, 0], [0, dfid], [0, -dfid], [-4*sc, -dfid], [2*sc, -dfid]])
#xyfid=numpy.array([(0, y) for y in [-dfid, dfid]]+[(x, 0) for x in [-dfid, dfid]])
intervs=10
comps1=[(1.0*b/intervs, 1.0*c/intervs, 1.0*(intervs-a-b-c)/intervs, 1.0*a/intervs) for a in numpy.arange(0,intervs+1)[::-1] for b in numpy.arange(0,intervs+1-a) for c in numpy.arange(0, intervs+1-a-b) if 0 in [a, b, c, intervs-a-b-c]][::-1]
#comps2=[(1.0*b/intervs, 1.0*c/intervs, 1.0*(intervs-a-b-c)/intervs, 1.0*a/intervs) for a in numpy.arange(0,intervs+1)[::-1] for b in numpy.arange(0,intervs+1-a) for c in numpy.arange(0, intervs+1-a-b)][::-1]
comps2=[(1.0*b/intervs, 1.0*c/intervs, 1.0*(intervs-a-b-c)/intervs, 1.0*a/intervs) for a in numpy.arange(0,intervs+1)[::-1] for b in numpy.arange(0,intervs+1-a) for c in numpy.arange(0, intervs+1-a-b) if 0 in [a, b, c, intervs-a-b-c]][::-1]

cols1=list(rgb_comp(comps1))
cols2=list(rgb_comp(comps2))
#cols3=list(rgb_comp(comps3))
compnone=[0., 0., 0., 0.]
colnone=[1., 1., 1.]
spaces=[0, 0, 0]
compsf=[]
colsf=[]
codef=[]


for cmps, cols, sp, cd, th in zip([comps1, comps2], [cols1, cols2], spaces, [0, 20], [1., .2]):
    cmps=numpy.array(cmps)
    compsf+=list(cmps*th)+[compnone]*sp
    colsf+=cols+[colnone]*sp
    codef+=[cd]*len(cmps)+[4]*sp

comps8all=numpy.zeros((len(xyall), 8))
comps8all[compinds, :4]=numpy.array(compsf)
codeall=numpy.ones(len(xyall), dtype='int32')
codeall[compinds]=numpy.array(codef)
colall=numpy.zeros((len(xyall), 3))
colall[compinds, :]=numpy.array(colsf)

xyallshift=numpy.array([[x+plateradius, y+plateradius-0.] for x, y in xyall])
xyfidshift=numpy.array([[x+plateradius, y+plateradius-0.] for x, y in xyfid])
startsmp=1

intfmt=lambda x:'%d' %x
floatarrfmt=lambda x:', '.join(['%.3f' %xx for xx in x])
linestr=lambda smp, xy, cmp, cd:', '.join((intfmt(smp), floatarrfmt(xy), floatarrfmt([1.016, 1.016]), floatarrfmt(cmp), intfmt(cd)))
datastr='\n'.join([linestr(i+startsmp, xy, cmp, cd) for i, (xy, cmp, cd) in enumerate(zip(xyallshift, comps8all, codeall))])
fidstr=', '.join(['(%.3f, %.3f)' %tuple(xyv) for xyv in xyfidshift])

a='% Xfiducial, Yfiducial='
b=' mm'
c='% Sample, x(mm), y(mm), dx(mm), dy(mm), A(fraction), B(fraction), C(fraction), D(fraction), E(fraction), F(fraction), G(fraction), H(fraction), code(0=sample; 1=spectral reference; 2=ABCD control; 3=EFGH control; 4=half thickness; 5=doublethickness; 10=empty)'
mainstr='%s%s%s\n%s\n%s' %(a, fidstr, b, c, datastr)

fn=r'D:\Google Drive\Documents\CaltechWork\platemaps\2.5inchwith3quatspaces\2.5inchwith3quatspaces'

f=open(fn+'.txt', mode='w')
f.write(mainstr)
f.close()


marks=['s', 's', 's', 'o', 'v', '^', '','','','','.']
def marks(cd):
    dup=cd//100
    cd=cd%100
    if cd<5:
        return ['s', 's', 's', 'o', '.'][cd]
    if (cd//10)<4:
        return 'v'
    else:
        return '^'

circ=pylab.Circle((plateradius,plateradius-0.),radius=plateradius,edgecolor='k',lw=1,facecolor='none')
ax=pylab.subplot(111)
ax.add_patch(circ)
#pylab.plot([-16.25+50, 16.24+50], [0, 0], 'k-', lw=2)

for x, y, col, cd in zip(xyallshift.T[0],xyallshift.T[1], colall, codeall):
    if cd%10 in [1, 2, 3, 9]:
        pylab.scatter(x, y,color=col,s=14,marker=marks(cd), edgecolor='r')
    elif cd in [4]:
        pylab.scatter(x, y,color='k',s=2,marker=marks(cd), edgecolor='k')
    else:
        pylab.scatter(x, y,color=col,s=14,marker=marks(cd), edgecolor='none')

#pylab.scatter(xypureref.T[0],xypureref.T[1],color='w', edgecolor='r',s=10,marker='s', lw=1)
if len(xyfidshift)>0:
    pylab.plot(xyfidshift.T[0],xyfidshift.T[1],'k+', ms=6)
pylab.xlim(0, 2*plateradius)
pylab.ylim(0, 2*plateradius)
ax.set_aspect(1)

lablist=['%d:%d' %(cd, (codeall==cd).sum()) for cd in [0, 20, 30, 1]]
pylab.title(','.join(lablist))


pylab.savefig(fn+'.png', dpi=300)


pylab.show()
