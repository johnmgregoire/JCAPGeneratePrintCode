import numpy,pylab

def rgb_comp(terncoordlist):
    cmy_cmyk=lambda a:a[:3]*(1.-a[3])+a[3]
    rgb_cmy=lambda a:1.-a
    rgb_cmyk=lambda a:rgb_cmy(cmy_cmyk(a))

    return numpy.array([rgb_cmyk(numpy.array(a)) for a in terncoordlist])
        


sc=2.032
xa=numpy.array([0, 1, 2, 3.5, 5, 6.5, 8.5])
ya=numpy.array([0, 2, 4, 6, 8])

quaddata=([(numpy.array((x, y)), ((j+1)*.2, 0, 0, 0, 0, 0, 0, 0), 0) for j, y in enumerate(ya) for i, x in enumerate(xa)])




circ=pylab.Circle((0.,0.),radius=50,edgecolor='k',lw=1,facecolor='none')
ax=pylab.subplot(111)
ax.add_patch(circ)
pylab.plot([-16.25, 16.24], [-47.29, -47.29], 'k-', lw=1)

shift=10

alldata=[]
for flx in [-1, 1]:
    for fly in [-1, 1]:
        alldata+=[(numpy.array([(xy[0]*sc+shift)*flx, (xy[1]*sc+shift)*fly]), cmp, cd) for i, (xy, cmp, cd) in enumerate(quaddata)]

xy=numpy.array([t[0] for t in alldata])
pylab.scatter(xy.T[0]*flx,xy.T[1]*fly,c='b',s=10,marker='s')

pylab.xlim(-50,50)
pylab.ylim(-50,50)
ax.set_aspect(1)

pylab.title(`len(xy)`+' samples')



intfmt=lambda x:'%d' %x
floatarrfmt=lambda x:', '.join(['%.3f' %xx for xx in x])
linestr=lambda smp, xy, cmp, cd:', '.join((intfmt(smp), floatarrfmt(xy), floatarrfmt([1.016, 1.016]), floatarrfmt(cmp), intfmt(cd)))
datastr='\n'.join([linestr(i+1, xy, cmp, cd) for i, (xy, cmp, cd) in enumerate(alldata)])
fidstr=''

a='% Xfiducial, Yfiducial='
b=' mm'
c='% Sample, x(mm), y(mm), dx(mm), dy(mm), A(fraction), B(fraction), C(fraction), D(fraction), E(fraction), F(fraction), G(fraction), H(fraction), code(0=sample; 1=spectral reference; 2=ABCD control; 3=EFGH control)'
mainstr='%s%s%s\n%s\n%s' %(a, fidstr, b, c, datastr)

f=open('C:/Users/Gregoire/Documents/CaltechWork/platemaps/adhesionstudy/adhesionstudy_5thickness7repeats_4inquadrant.txt', mode='w')
f.write(mainstr)
f.close()


pylab.show()
