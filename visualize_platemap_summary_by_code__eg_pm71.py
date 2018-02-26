import numpy, pylab
import numpy as np

import matplotlib.cm as cm
import matplotlib.colors as colors
from readplatemap import readsingleplatemaptxt
from visualize_alloy_platemaps__eg_pm71__userparams import userinputd
path_pm=r'J:\hte_jcap_app_proto\map\0072-04-0100-mp.txt'
#path_pm=r'D:\Google Drive\Documents\CaltechWork\platemaps\201608alloy\0071-04-0100-mp_Iremovedfixed.txt'


#This lets you visualize the printing for 4 channels that includes A, B and 2 other channels of your choosing
#The intention is for channel A to contain off-stoichiometric version of the target phase (elements 1 and 2) and channel B contains the under-represented element (element 2) and elements 3 and 4 are alloying elements
#concentration can be in any units as long as all values areconsistent
#userinputd={\
#'element_1': 'V', \
#'element_2': 'Cu', \
#'element_3': 'Fe', \
#'element_4': 'W', \
#'channel_element3': 'E', \
#'channel_element4': 'H', \
#'conc_el1_in_inkA': .57*.3, \
#'conc_el2_in_inkA': .43*.3, \
#'conc_el2_in_inkB': .4, \
#'conc_el3': .03, \
#'conc_el4': .03, \
#'only_codes_with_alloys': True, \
#}

m_a=np.array([userinputd['conc_el1_in_inkA'], userinputd['conc_el2_in_inkA'], 0., 0.])

m_b=np.array([0., userinputd['conc_el2_in_inkB'], 0, 0])

m_c=np.array([0, 0, userinputd['conc_el3'], 0.])
m_d=np.array([0, 0, 0., userinputd['conc_el3']])

M=np.array([m_a, m_b, m_c, m_d])



dlist=readsingleplatemaptxt(path_pm,  returnfiducials=False)


allchans=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
#ignorechans=[]#set(allchans).difference(set(chans))


dlist=[d for d in dlist if (d['code']%100)==0]

codeset=set([d['code'] for d in dlist])
codesetlist=sorted(list(codeset))


for d in dlist:
    d['chanwts']=np.array([d[k] for k in allchans])
#    mol_comps_chanwts(d)
#    bin_frac_a_in_phase(d)
    d['numnonzerowts']=(d['chanwts'][2:]>0.).sum(dtype='int32')
    d['m']=['^','s','o'][d['numnonzerowts']]

pylab.figure('code_sampl_guide', figsize=(13, 8))

ax_pm=pylab.subplot(111)
pylab.subplots_adjust(left=.03, right=1, bottom=.03, top=.95)
ax_pm.set_aspect(1)
pylab.title('triangle,square,circle are 0-,1-,2-element alloys\ncolor gives code\nc<code>s<min sample_no><alloyels> for each code')


numcodes=len(codeset)

norm=colors.Normalize(vmin=0, vmax=numcodes-1, clip=False)
sm=cm.ScalarMappable(norm=norm, cmap='Set1')
codeinds=np.arange(numcodes)
sm.set_array(codeinds)
cols=numpy.float32(map(sm.to_rgba, codeinds))[:, :3]#ignore alpha
ticklabels=[]
for col, cod in zip(cols, codesetlist):
    x, y=np.array([[d['x'], d['y']] for d in dlist if d['code']==cod]).T
    marr=[d['m'] for d in dlist if d['code']==cod]
    smps=[d['Sample'] for d in dlist if d['code']==cod]
    alloyellsused_temp=[chan if d[chan]>0. else ''  for d in dlist if d['code']==cod for count, chan in enumerate(allchans[2:]) ]
    alloyellsused=sorted(list(set(alloyellsused_temp)))
    alloyels=''.join(alloyellsused)
    ticklabels+=['%d(%s)' %(cod, alloyels)]
    

    #pylab.plot(x, y, 's', c=col, mec='none')
    for xv, yv, m in zip(x, y, marr):
        pylab.plot(xv, yv, m, c=col, mec='none')
    xl=x.min()
    yl=y.max()
    i=np.argmin((x-xl)**2+(y-yl)**2)
    smp=smps[i]
    pylab.text(xl, yl, 'c%ds%d%s' %(cod, smp, alloyels), ha='right', va='center')
    
#    xl=x.max()
#    yl=y.min()
#    i=np.argmin((x-xl)**2+(y-yl)**2)
#    smp=smps[i]
#    pylab.text(xl, yl, '%d' %smp, ha='left', va='center')
#cbax=pylab.gcf().add_axes((.92, .4, .06, .2))
#cbax.cla()
cb=pylab.colorbar(sm)#, cax=cbax)
cb.set_label('code')
cb.set_ticks(codeinds)
cb.set_ticklabels(ticklabels)
pylab.xlim(0, 150)
pylab.ylim(0, 100)

pylab.show()
