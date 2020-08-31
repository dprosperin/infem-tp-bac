from PyQt5.QtWidgets import *
from PyQt5.QtCore    import *
from PyQt5.QtGui     import *

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
        self.pixOrig = QPixmap('bac/voiture.png')

    def sizeHint(self):
        return QSize(40,140)

    def paintEvent(self,e):
        painter = QPainter(self)
        brush = QBrush()
        width = painter.device().width()
        height = painter.device().height()
        riverWidth = .3*width
        ferryWidth = .12*width
        groundFirstPartWidth = .6*width
        carWidth = ferryWidth*0.9
        pix = self.pixOrig.scaledToWidth(carWidth,Qt.SmoothTransformation)
        #background
        colorGround = QColor('#a77844')
        colorWater  = QColor('#0f03ff')
        colorFerry  = QColor('#919191')
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(colorGround)
        rectG = QRect(0, 0, width, height)
        painter.fillRect(rectG, brush)
        brush.setColor(colorWater)
        rectW = QRect(groundFirstPartWidth, 0, riverWidth, height)
        painter.fillRect(rectW, brush)
        #ferry
        ferryPixelPos = groundFirstPartWidth+(riverWidth-ferryWidth)*self.ferryPos
        ferry = QRect(ferryPixelPos, 0, ferryWidth, height)
        brush.setColor(colorFerry)
        painter.fillRect(ferry, brush)
        #car
        carPosInFerry = ferryPixelPos+.1*carWidth
        for i in range(10):
            if self.carState[i] == 'drive': 
                painter.drawPixmap(self.carPos[i]*(groundFirstPartWidth-carWidth),i*height/10.,pix)
            elif self.carState[i] == 'load': #offset in ferry: .1*carWidth
                painter.drawPixmap(groundFirstPartWidth+carWidth*(self.carPos[i]*1.1-1),i*height/10.,pix)
            elif self.carState[i] == 'ferry':
                painter.drawPixmap(carPosInFerry,i*height/10.,pix)
            elif self.carState[i] == 'unload':
                painter.drawPixmap(carPosInFerry + 1.2*carWidth*self.carPos[i],i*height/10.,pix)
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
        """ Update the car position on gui during loading part.
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


