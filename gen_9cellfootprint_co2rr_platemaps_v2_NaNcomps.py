import numpy,pylab

def rgb_comp(terncoordlist):
#    if numpy.array(terncoordlist).sum()==0:
#        return numpy.array([1, 1, 1.])
    cmy_cmyk=lambda a:a[:3]*(1.-a[3])+a[3]
    rgb_cmy=lambda a:1.-a
    rgb_cmyk=lambda a:rgb_cmy(cmy_cmyk(a))

    return numpy.array([rgb_cmyk(numpy.array(a)) for a in terncoordlist])




sample_diameter=100*25.4/300.#

x_pitch__cell_od=112*25.4/300.

y_pitch__cell_pitch=128*25.4/300.


xsub, ysub=150., 100.
xvals=numpy.arange(14)*x_pitch__cell_od
xvals+=(150.-(xvals.max()-xvals.min()))/2.
yvals=numpy.arange(9)*y_pitch__cell_pitch
yvals+=(100.-(yvals.max()-yvals.min()))/2.
#xyf=numpy.array([[xv, yv] for yv in yvals[::-1] for xv in xvals])
xyf=numpy.array([[xv, yv] for xv in xvals for yv in yvals[::-1]])


xyfid=numpy.array([[]])
xypureref=[]
xyspecref=[]


#dfid=22*sc
xyfid=[]#numpy.array([[-dfid, 0], [dfid, 0], [0, dfid], [-7*sc, -21*sc]])
#xyfid=numpy.array([(0, y) for y in [-dfid, dfid]]+[(x, 0) for x in [-dfid, dfid]])

intervs=8
binarylist_compslist=[]
for i, j in [(0, 1), (0, 2), (1, 2), (1, 0), (2, 0), (2, 1), (0, 1), (0, 2), (1, 2), (1, 0), (2, 0), (2, 1)]:
    tc=numpy.zeros((intervs+1, 4), dtype='float64')
    tc[:, j]=1.*numpy.arange(intervs+1)/intervs
    tc[:, i]=1.-tc[:, j]
    binarylist_compslist+=[list(tc)]


comps1=[(1., 0., 0., 0.), (0., 1., 0., 0.), (0., 0., 1., 0.)]


compnone=[0., 0., 0., 0.]
colnone=[1., 1., 1.]
spaces=[0]*999
compsf=[]
colsf=[]
codef=[]
num_code_segment=12+3+3#12 for the binary lines and then 3 repeats of elemtnals in 2 different columns
comps1=numpy.array(comps1)
for sp, cd, compsx in zip(spaces, numpy.arange(num_code_segment, dtype='int32')*100, binarylist_compslist+[comps1, comps1, comps1]+[comps1, comps1, comps1]):
    compsf+=list(compsx)+[compnone]*sp
    colsf+=list(rgb_comp(compsx))+[colnone]*sp
    codef+=[cd]*len(compsx)+[4]*sp
    print len(compsf)


pylab.figure()

comps=compsf[:len(xyf)]
cols=colsf[:len(xyf)]
code=codef[:len(xyf)]

cols=numpy.array(cols)
code=numpy.array(code)
xy=xyf

print len(comps), len(xy)

#temp=numpy.zeros(16)
#temp[8]=1.
#comps8pure=numpy.array([temp[i:i+8] for i in [0, 0, 0, 0, 0, 0, 0, 0, 8, 7, 6, 5]])
#comps8pureinspec=numpy.array([temp[i:i+8] for i in [0, 8, 0, 7, 0, 6, 0, 5]])
#codeinspec=[1, 2, 1, 2, 1, 2, 1, 2]
#colinspec=rgb_comp(comps8pureinspec[:, :4])
#colinpure=rgb_comp(comps8pure[:, :4])
#codeinpure=[4, 4, 4, 4, 4, 4, 4, 4, 2, 2, 2, 2]
#
#comps8pure=numpy.concatenate([comps8pure])
#codepure=numpy.concatenate([codeinpure])
#colpure=numpy.concatenate([colinpure])
#
#    
#rgb_comp(comps1)
#sortmetricspec=numpy.array([x*100-y for x, y in xyspecref])
#sortindsspec=numpy.argsort(sortmetricspec)
#xyspecref=xyspecref[sortindsspec]
#comps8spec=[]
#codespec=[]
#colspec=[]
#jshift=0
#for i in range(len(xyspecref)):
##    if i in [29, 68]:
##        jshift+=1
#    j=(i-jshift)%len(comps8pureinspec)
#    comps8spec+=[comps8pureinspec[j]]
#    codespec+=[codeinspec[j]]
#    colspec+=[colinspec[j]]

temp=numpy.zeros(4)
comps8=numpy.array([numpy.concatenate([c, temp]) for c in comps])
temp=numpy.zeros(8)
#comps8spec=numpy.array([temp for q in xyspecref])
xyall=numpy.concatenate([xy])
compall=numpy.concatenate([comps8])
colall=numpy.concatenate([cols])
codeall=numpy.concatenate([code])
#xyall=numpy.concatenate([xy, xyspecref])
#compall=numpy.concatenate([comps8, comps8spec])
#colall=numpy.concatenate([cols, colspec])
#codeall=numpy.concatenate([code, codespec])
sortmetric=numpy.array([-y*1000+x for x, y in xyall])
sortinds=numpy.argsort(sortmetric)
xyallsort=xyall[sortinds]
codeallsort=codeall[sortinds]
compallsort=compall[sortinds]
colallsort=colall[sortinds]


startsmp=1

intfmt=lambda x:'%d' %x
floatarrfmt=lambda x:', '.join(['%.3f' %xx for xx in x])
linestr=lambda smp, xy, cmp, cd:', '.join((intfmt(smp), floatarrfmt(xy), floatarrfmt([sample_diameter, sample_diameter]), floatarrfmt(cmp), intfmt(cd)))
datastr='\n'.join([linestr(i+startsmp, xy, cmp, cd) for i, (xy, cmp, cd) in enumerate(zip(xyallsort, compallsort, codeallsort))])
fidstr=', '.join(['(%.3f, %.3f)' %tuple(xyv) for xyv in xyfid])

a='% Xfiducial, Yfiducial='
b=' mm'
c='% Sample, x(mm), y(mm), dx(mm), dy(mm), A(fraction), B(fraction), C(fraction), D(fraction), E(fraction), F(fraction), G(fraction), H(fraction), code(0=sample; 1=spectral reference; 2=ABCD control; 3=EFGH control; 4=half thickness; 5=doublethickness; 10=empty)'
mainstr='%s%s%s\n%s\n%s' %(a, fidstr, b, c, datastr)

fn=r'D:\Google Drive\Documents\caltechwork\platemaps\201701co2rr_v1\co2rr_10x14_v1'


f=open(fn+'.txt', mode='w')
f.write(mainstr)
f.close()


#marks=['s', 's', 's', 'o', 'v', '^', '','','','','.']
def marks(cd):
    return 'o'
#    dup=cd//100
#    cd2=cd%100
#    if cd>0 and cd<5:
#        return ['', 's', 's', 'o', '.'][cd]
#    return (['s']*6+['^', '>', 'v', '<', 's'])[dup]


print set(codeallsort)
for x, y, col, cd in zip(xyallsort.T[0],xyallsort.T[1], colallsort, codeallsort):

    if cd in [4]:
        pylab.scatter([x], [y],color='k',s=2,marker=marks(cd), edgecolor='k')
    elif cd in [1]:
        pylab.scatter([x], [y],color='w',s=2,marker=marks(cd), edgecolor='k')
    else:
        pylab.scatter([x], [y],color=col,s=500,marker=marks(cd), edgecolor='none')

#pylab.scatter(xypureref.T[0],xypureref.T[1],color='w', edgecolor='r',s=10,marker='s', lw=1)
if len(xyfid)>0:
    pylab.plot(xyfid.T[0],xyfid.T[1],'k+', ms=6)
pylab.xlim(0, 150)
pylab.ylim(0, 100)
pylab.gca().set_aspect(1)

lablist=['%d:%d' %(cd, (codeallsort==cd).sum()) for cd in [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1, 2, 3, 4]]
pylab.title(','.join(lablist[:6])+'\n'+','.join(lablist[6:]))


pylab.savefig(fn+'.png', dpi=300)


pylab.show()
