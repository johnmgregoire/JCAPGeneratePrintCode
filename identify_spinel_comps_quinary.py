import numpy as np
import itertools as it
import pylab, sys, copy
intervs=12
comps1=[(1.0*b/intervs, 1.0*c/intervs, 1.0*d/intervs, 1.0*(intervs-a-b-c-d)/intervs, 1.0*a/intervs) for a in np.arange(0,intervs+1)[::-1] for b in np.arange(0,intervs+1-a) for c in np.arange(0, intervs+1-a-b) for d in np.arange(0, intervs+1-a-b-c)][::-1]
comps1=np.array(comps1)
ratio_target=2.
ratio_tol=0.005

n=len(comps1[0])

inds=range(n)

inds_comb=[list(s) for i in range(1, n) for s in it.combinations(inds, i)]


numer_calc=lambda c, inds: c[inds].sum()
denom_calc=lambda c, inds: c.sum()-c[inds].sum()

within_tol_calc=lambda c, inds:np.abs(numer_calc(c, inds)/denom_calc(c, inds)-ratio_target)<=ratio_tol

comps=np.array([c for c in comps1 if True in [within_tol_calc(c, inds) for inds in inds_comb]])

print len(comps), len(comps1)


#inds=np.where(comps[:, 2:].sum(axis=1)==0.)[0]
#print comps[inds]

sys.path.append(r'D:\Google Drive\Documents\PythonCode\JCAP\PythonCompositionPlots')
from myquaternaryutility import QuaternaryPlot


from PyQt4.QtCore import *
from PyQt4.QtGui import *
from quaternary_faces_shells import ternaryfaces_shells
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
try:
    from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
except ImportError:
    from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class plotwidget(FigureCanvas):
    def __init__(self, parent, width=12, height=6, dpi=72, projection3d=False):

        #plotdata can be 2d array for image plot or list of 2 1d arrays for x-y plot or 2d array for image plot or list of lists of 2 1D arrays
        self.projection3d=projection3d
        self.fig=Figure(figsize=(width, height), dpi=dpi)
        if projection3d:
            self.axes=self.fig.add_subplot(111, navigate=True, projection='3d')
        else:
            self.axes=self.fig.add_subplot(111, navigate=True)

        self.axes.hold(True)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        #self.parent=parent
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        #NavigationToolbar(self, parent)
        NavigationToolbar(self, self)

        self.mpl_connect('button_press_event', self.myclick)
        self.clicklist=[]
        self.cbax=None
    

    def myclick(self, event):
        if not (event.xdata is None or event.ydata is None):
            arrayxy=[event.xdata, event.ydata]
            print 'clicked on image: array indeces ', arrayxy, ' using button', event.button
            self.clicklist+=[arrayxy]
            self.emit(SIGNAL("genericclickonplot"), [event.xdata, event.ydata, event.button, event.inaxes])

class dialog(QDialog):
    def __init__(self, comps, parent=None, title='', folderpath=None):
        super(dialog, self).__init__(parent)

        
        plotw=plotwidget(self)
        
        ax=plotw.axes
        

        inds=np.where(comps[:, -1]==0.)[0]
        comps=comps[inds, :-1]
        #print comps.shape
        stpquat=QuaternaryPlot(ax)
        ax.cla()
        cols=stpquat.rgb_comp(comps)
        #stpquat.scatter(comps, c=cols, s=100, edgecolors='none')
        #stpquat.label()

        self.tf=ternaryfaces_shells(ax, nintervals=intervs)
        self.tf.label()
        self.tf.scatter(comps, cols, skipinds=[0, 1, 2, 3], s='patch')
        
        #only select comps
        plotw2=plotwidget(self, projection3d=True)
        
        
        ax=plotw2.axes
        #unary
        
        stpquat=QuaternaryPlot(ax)

        stpquat.scatter(comps, c=cols, s=100, edgecolors='none')
        stpquat.label()

        
        QObject.connect(plotw, SIGNAL("genericclickonplot"), self.plotclick)
        QObject.connect(plotw2, SIGNAL("genericclickonplot"), self.plotclick)
        
        mainlayout=QGridLayout()
        mainlayout.addWidget(plotw, 0, 0)
        mainlayout.addWidget(plotw2, 1, 0)

        
        self.setLayout(mainlayout)
    
    def plotclick(self, coords_button_ax):
        xc, yc, button, ax=coords_button_ax
        print self.tf.toComp(xc, yc)
        
class MainMenu(QMainWindow):
    def __init__(self):
        super(MainMenu, self).__init__(None)
        
        x=dialog(comps)
        x.exec_()
        
mainapp=QApplication(sys.argv)
form=MainMenu()
form.show()
form.setFocus()
mainapp.exec_()
