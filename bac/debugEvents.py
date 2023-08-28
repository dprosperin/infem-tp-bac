#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

import threading
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

pb  = QImage('bac/icons/cross.png').scaled(16,16,Qt.KeepAspectRatio)
log = QImage('bac/icons/arrow-000.png').scaled(16,16,Qt.KeepAspectRatio)

class debugEventModel(QAbstractListModel):
    signalAddEv = pyqtSignal(int,str)
    signalScroll = pyqtSignal()

    def __init__(self,*args,debugEvent=None,**kwargs):
        super(debugEventModel,self).__init__(*args,**kwargs)
        self.debugEvent = debugEvent or []
        self.signalAddEv.connect(self.addEvGUIThread)

    def data(self,index,role): #index: row,column
        status, text = self.debugEvent[index.row()]
        if role == Qt.DisplayRole:
            return text
        if role == Qt.ToolTipRole:
            return text
        if role == Qt.DecorationRole:
            if status==1: #error
                return pb
            if status==2: #log
                return log

    def rowCount(self,index):
        return len(self.debugEvent)

    def addEv(self,error,text):
        self.signalAddEv.emit(error,text)

    @pyqtSlot(int,str)
    def addEvGUIThread(self,error,text):
        assert threading.current_thread() is threading.main_thread()
        index = QModelIndex()
        n = self.rowCount(index)
        self.beginInsertRows(index,n,n)
        self.debugEvent.append((error,text))
        self.endInsertRows()
        self.signalScroll.emit()
