from PyQt5.QtWidgets import *
from PyQt5.QtCore    import *
from PyQt5.QtGui     import *
import random

class QDrawing(QWidget):
    
    repaintSignal = pyqtSignal()
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.setSizePolicy(QSizePolicy.MinimumExpanding,
                QSizePolicy.MinimumExpanding)
        self.ferryPos = 0 #0 to 1
        self.carPos = [0]*10 #0 to 1
        self.carState = ['drive']*10 #drive, load, ferry, unload
        self.repaintSignal.connect(self.repaint)
        self.pixOrig = []
        files = []
        for i in range(6):
            files.append('bac/icons/voiture{0}.png'.format(i+1))
        for i in range(10):
            idx = random.randint(0,len(files)-1)
            self.pixOrig.append(QPixmap(files[idx]))

    def sizeHint(self):
        return QSize(40,140)

    def paintEvent(self,e):
        painter = QPainter(self)
        brush = QBrush()
        width = painter.device().width()
        height = painter.device().height()
        riverWidth = .3*width
        ferryWidth = .12*width
        groundFirstPartWidth = .56*width
        carWidth = ferryWidth*0.9
        pix = []
        for i in range(10):
            pix.append(self.pixOrig[i].scaledToWidth(int(carWidth),Qt.SmoothTransformation))
        #background
        colorGround = QColor('#a77844')
        colorWater  = QColor('#0f03ff')
        colorFerry  = QColor('#919191')
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(colorGround)
        rectG = QRect(0, 0, width, height)
        painter.fillRect(rectG, brush)
        brush.setColor(colorWater)
        rectW = QRect(int(groundFirstPartWidth), 0, int(riverWidth), int(height))
        painter.fillRect(rectW, brush)
        #ferry
        ferryPixelPos = groundFirstPartWidth+(riverWidth-ferryWidth)*self.ferryPos
        ferry = QRect(int(ferryPixelPos), 0, int(ferryWidth), int(height))
        brush.setColor(colorFerry)
        painter.fillRect(ferry, brush)
        #car
        carPosInFerry = ferryPixelPos+.1*carWidth
        carPosUnloaded = groundFirstPartWidth+(riverWidth-ferryWidth) +.1*carWidth
        for i in range(10):
            if self.carState[i] == 'drive': 
                painter.drawPixmap(int(self.carPos[i]*(groundFirstPartWidth-carWidth)),int(i*height/10.),pix[i])
            elif self.carState[i] == 'load': #offset in ferry: .1*carWidth
                painter.drawPixmap(int(groundFirstPartWidth+carWidth*(self.carPos[i]*1.1-1)),int(i*height/10.),pix[i])
            elif self.carState[i] == 'ferry':
                painter.drawPixmap(int(carPosInFerry),int(i*height/10.),pix[i])
            elif self.carState[i] == 'unload':
                painter.drawPixmap(int(carPosUnloaded + 1.2*carWidth*self.carPos[i]),int(i*height/10.),pix[i])
            else:
                raise Exception('internal error car state in QDrawing')

    def setFerryPos(self,pos):
        """ Update the Ferry position on gui. Position, should be set between 0.0 and 1.0
        This function may be called by another thread (non gui) """
        if pos < 0.0:
            self.ferryPos = 0.0
        elif pos > 1.0:
            self.ferryPos = 1.0
        else:
            self.ferryPos = pos
        #update graphic now.
        self.repaintSignal.emit()
        
    def setDrivePos(self,pos,i):
        """ Update the car position on gui during driving part. 
        Position, should be set between 0.0 and 1.0.
        This function may be called by another thread (non gui) """
        self.carState[i] = 'drive'
        x = pos
        if x < 0.0:
            x = 0.0
        elif x > 1.0:
            x = 1.0
        self.carPos[i] = x
        #update graphic now.
        self.repaintSignal.emit()

    def setLoadPos(self,pos,i):
        """ Update the car position on gui during loading part.
        Position, should be set between 0.0 and 1.0.
        This function may be called by another thread (non gui) """
        self.carState[i] = 'load'
        x = pos
        if x < 0.0:
            x = 0.0
        elif x > 1.0:
            x = 1.0
        self.carPos[i] = x
        #update graphic now.
        self.repaintSignal.emit()

    def setLoaded(self,i):
        """ Update the car position on gui. Change car state.
        This function may be called by another thread (non gui) """
        self.carState[i] = 'ferry'

    def setUnloadPos(self,pos,i):
        """ Update the car position on gui during unloading part.
        Position, should be set between 0.0 and 1.0.
        This function may be called by another thread (non gui) """
        self.carState[i] = 'unload'
        x = pos
        if x < 0.0:
            x = 0.0
        elif x > 1.0:
            x = 1.0
        self.carPos[i] = x
        #update graphic now.
        self.repaintSignal.emit()


