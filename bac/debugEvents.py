#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

pb = QImage('bac/cross.png').scaled(16,16,Qt.KeepAspectRatio)

class debugEventModel(QAbstractListModel):
    def __init__(self,*args,debugEvent=None,**kwargs):
        super(debugEventModel,self).__init__(*args,**kwargs)
        self.debugEvent = debugEvent or []

    def data(self,index,role): #index: row,column
        status, text = self.debugEvent[index.row()]
        if role == Qt.DisplayRole:
            return text
        if role == Qt.ToolTipRole:
            return 'tooltip:'+text
        if role == Qt.DecorationRole:
            if status:
                return pb

    def rowCount(self,index):
        return len(self.debugEvent)

    def addEv(self,error,text):
        index = QModelIndex()
        n = self.rowCount(index)
        self.beginInsertRows(index,0,1)
        self.debugEvent.insert(0,(error,text))
        self.endInsertRows()
