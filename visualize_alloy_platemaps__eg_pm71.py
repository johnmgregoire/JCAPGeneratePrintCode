import numpy, pylab
import numpy as np

import matplotlib.cm as cm
import matplotlib.colors as colors
from readplatemap import readsingleplatemaptxt
from visualize_alloy_platemaps__eg_pm71__userparams import userinputd
path_pm=r'J:\hte_jcap_app_proto\map\0072-04-0100-mp.txt'


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

def calc_frac_a_bin_vals(ab_mols_A, ab_mols_B, chanwtsarr=np.array([[.45, 0], [.55, .05], [.5,.1]])):
    fracalist=[]
    for wtA, wtB in chanwtsarr:
        amt_ab=ab_mols_A*wtA+ab_mols_B*wtB
        fraca=amt_ab[0]/amt_ab.sum()
        fracalist+=[fraca]
    return fracalist
frac_a_in_phase__binvals=calc_frac_a_bin_vals(m_a[:2], m_b[:2])
frac_a_in_phase__bincols=['r', 'g', 'b']

dlist=readsingleplatemaptxt(path_pm,  returnfiducials=False)

chans=['A','B']+[userinputd[k] for k in ['channel_element3','channel_element4']]
allchans=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
ignorechans=set(allchans).difference(set(chans))


#if not 'code' in dlist[0].keys():#this is to fix temporary error in the J platemap where the code is called "I"
#    for d in dlist:
#        d['code']=d['I']

dlist=[d for d in dlist if d['code']%100==0 and not (False in [d[k]==0. for k in ignorechans])]

if userinputd['only_codes_with_alloys']:
    codeset=set([d['code'] for d in dlist if d[chans[2]]>0. or d[chans[3]]>0.])
    dlist=[d for d in dlist if d['code'] in codeset]
else:
    codeset=set([d['code'] for d in dlist])
codesetlist=sorted(list(codeset))



def mol_comps_chanwts(d, chanwts=None):
    if chanwts is None:
        chanwts=d['chanwts']
    else:
        chanwts=np.array(chanwts)
        d={}
        d['chanwts']=chanwts
    mol_els=(M*chanwts[:, np.newaxis]).sum(axis=0)
    comp_els=mol_els/mol_els.sum()
    d.update(totmols=mol_els.sum(), comp=comp_els, frac_a_in_phase=comp_els[0]/comp_els[:2].sum(), alloy_loading_frac=comp_els[2:].sum()/comp_els.sum(), frac_c_in_alloy=comp_els[2]/comp_els[2:].sum(), totprintvol=chanwts.sum(),chanwts=chanwts,chanwts8=np.array(list(chanwts)+[0,0,0,0]))
    return d
def bin_frac_a_in_phase(d):
    i=np.argmin((d['frac_a_in_phase']-frac_a_in_phase__binvals)**2)
    d.update(frac_a_in_phase_binval=frac_a_in_phase__binvals[i], frac_a_in_phase_bincol=frac_a_in_phase__bincols[i])


for d in dlist:
    d['chanwts']=np.array([d[k] for k in chans])
    mol_comps_chanwts(d)
    bin_frac_a_in_phase(d)
    d['numzerowts_outof2']=(d['chanwts'][2:]==0.).sum(dtype='int32')
    d['m']=['o','s','^', '^'][d['numzerowts_outof2']]
lab_frac_c_in_alloy='frac %s in alloy (%s/(%s+%s))' %(userinputd['element_3'], userinputd['element_3'], userinputd['element_3'], userinputd['element_4'])
lab_alloy_loading_frac='tot alloy loading (%s+%s)/(%s+%s+%s+%s)'  %(userinputd['element_3'], userinputd['element_4'], userinputd['element_1'], userinputd['element_2'], userinputd['element_3'], userinputd['element_4'])
lab_frac_a_in_phase='frac %s in target (%s/(%s+%s))' %(userinputd['element_1'], userinputd['element_1'], userinputd['element_1'], userinputd['element_2'])
lab_totmols='total moles of metal'
lab_totprintvol='total volume from channels A-H (if each use same drop size)'

pylab.figure('alloy_comp_load')
ax_alloy_comp_load=pylab.subplot(111)
pylab.xlabel(lab_frac_c_in_alloy)
pylab.ylabel(lab_alloy_loading_frac)

pylab.figure('alloy_comp_totmol')
ax_alloy_comp_totmol=pylab.subplot(111)
pylab.xlabel(lab_frac_c_in_alloy)
pylab.ylabel(lab_totmols)


pylab.figure('alloy_load_totmol')
ax_alloy_load_totmol=pylab.subplot(111)
pylab.xlabel(lab_alloy_loading_frac)
pylab.ylabel(lab_totmols)

pylab.figure('phase_comp_totmol')
ax_phase_comp_totmol=pylab.subplot(111)
pylab.xlabel(lab_frac_a_in_phase)
pylab.ylabel(lab_totmols)

pylab.figure('phase_comp_alloycomp')
ax_phase_comp_alloycomp=pylab.subplot(111)
pylab.xlabel(lab_frac_a_in_phase)
pylab.ylabel(lab_frac_c_in_alloy)

pylab.figure('phase_comp_totprintvol')
ax_phase_comp_totprintvol=pylab.subplot(111)
pylab.xlabel(lab_frac_a_in_phase)
pylab.ylabel(lab_totprintvol)

pylab.figure('code_sampl_guide', figsize=(13, 8))

ax_pm=pylab.subplot(111)
pylab.subplots_adjust(left=.03, right=1, bottom=.03, top=.95)
ax_pm.set_aspect(1)
pylab.title('triangle,square,circle are 0-,1-,2-element alloys\ncolor gives code\nmin,max sample_no list for each code')

for d in dlist:#zip([dlist_no,dlist_un,dlist_bi],['^','s','o']):
    m=d['m']

    ms=5 if m=='^' else 3
    ax_alloy_comp_load.plot([d['frac_c_in_alloy']], d['alloy_loading_frac'], m, c=d['frac_a_in_phase_bincol'],ms=ms)
    ax_alloy_comp_totmol.plot([d['frac_c_in_alloy']], d['totmols'], m, c=d['frac_a_in_phase_bincol'],ms=ms)
    ax_alloy_load_totmol.plot([d['alloy_loading_frac']], d['totmols'], m, c=d['frac_a_in_phase_bincol'],ms=ms)
    ax_phase_comp_totmol.plot([d['frac_a_in_phase']], d['totmols'], m, c=d['frac_a_in_phase_bincol'],ms=ms)
    ax_phase_comp_alloycomp.plot([d['frac_a_in_phase']], d['frac_c_in_alloy'], m, c=d['frac_a_in_phase_bincol'],ms=ms)
    ax_phase_comp_totprintvol.plot([d['frac_a_in_phase']], d['totprintvol'], m, c=d['frac_a_in_phase_bincol'],ms=ms)


pylab.figure('code_sampl_guide')

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
    elschoice=[3 if (d[chans[2]]>0. and d[chans[3]]>0.) else (2 if d[chans[3]]>0. else (1 if d[chans[2]]>0. else 0))  for d in dlist if d['code']==cod]
    alloyels=['no', userinputd['element_3'], userinputd['element_4'], userinputd['element_3']+userinputd['element_4']][max(elschoice)]
    ticklabels+=['%d(%s)' %(cod, alloyels)]
    
    codeset=set([d['code'] for d in dlist if d[chans[2]]>0. and d[chans[3]]>0.])
    #pylab.plot(x, y, 's', c=col, mec='none')
    for xv, yv, m in zip(x, y, marr):
        pylab.plot(xv, yv, m, c=col, mec='none')
    xl=x.min()
    yl=y.max()
    i=np.argmin((x-xl)**2+(y-yl)**2)
    smp=smps[i]
    pylab.text(xl, yl, '%d' %smp, ha='right', va='center')
    
    xl=x.max()
    yl=y.min()
    i=np.argmin((x-xl)**2+(y-yl)**2)
    smp=smps[i]
    pylab.text(xl, yl, '%d' %smp, ha='left', va='center')
#cbax=pylab.gcf().add_axes((.92, .4, .06, .2))
#cbax.cla()
cb=pylab.colorbar(sm)#, cax=cbax)
cb.set_label('code')
cb.set_ticks(codeinds)
cb.set_ticklabels(ticklabels)
pylab.xlim(0, 150)
pylab.ylim(0, 100)

pylab.show()
