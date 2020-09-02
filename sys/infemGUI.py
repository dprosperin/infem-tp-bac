#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

import threading
from PyQt5.QtCore import *
from PyQt5.QtGui import QColor

class SemaphoreModel(QAbstractTableModel):
    """ Set the Semaphore state, for interaction with the gui:
    - semaphore name
    - semaphore value
    - waiting list

    """
    updateColumnWidth = pyqtSignal()
    def __init__(self,*args,todos=None,**kwargs):
        super(SemaphoreModel,self).__init__(*args,**kwargs)
        self.semaphores = []      #tuple: name - value - threads
        self.waitingThreads = {}  #name => waiting threads
        self.semaphoreNames = {}  #name => index
        self.mutex = threading.Semaphore(1) #internal protection
        #self.headerName = ['name','value','waiting threads']
        self.headerName = ['nom','valeur',"liste d'attente"]

    def data(self,index,role): #index: row,column
        #print('data required '+str(index.row())+','+str(index.column()))
        if role == Qt.DisplayRole:
            with self.mutex:
                data = self.semaphores[index.row()]
                return data[index.column()]
        if role == Qt.ForegroundRole:
            if self.semaphores[index.row()][2]: #Are there waiting threads?
                return QColor('red')
            return QColor('black')
            

    def addSemaphore(self,name,value):
        #print('add the semaphore '+str(name))
        with self.mutex:
            self.semaphoreNames[name] = len(self.semaphores)
            self.semaphores.append((name,value,None))
            self.waitingThreads[name] = set()
        self.updateColumnWidth.emit()
        self.layoutChanged.emit()

    def rowCount(self,index):
        return len(self.semaphores)

    def columnCount(self,index):
        return 3

    def update(self,sem):
        with self.mutex:
            idx = self.semaphoreNames[sem.name]
            self.semaphores[idx] = (sem.name,sem.value,self.semaphores[idx][2])
        self.dataChanged.emit(self.index(idx,0),self.index(idx,2))

    def removeWaitingThread(self,sem,threadName):
        with self.mutex:
            idx = self.semaphoreNames[sem.name]
            self.waitingThreads[sem.name].remove(threadName)
            threads = ' - '.join(self.waitingThreads[sem.name])
            self.semaphores[idx] = (sem.name,-len(self.waitingThreads[sem.name]),threads)
        self.dataChanged.emit(self.index(idx,0),self.index(idx,2))

    def addWaitingThread(self,sem,threadName):
        with self.mutex:
            idx = self.semaphoreNames[sem.name]
            self.waitingThreads[sem.name].add(threadName)
            threads = ' - '.join(self.waitingThreads[sem.name])
            self.semaphores[idx] = (sem.name,-len(self.waitingThreads[sem.name]),threads)
        self.dataChanged.emit(self.index(idx,0),self.index(idx,2))

    def clearWaitingThread(self,sem):
        with self.mutex:
            idx = self.semaphoreNames[sem.name]
            self.waitingThreads[sem.name].clear()
            self.semaphores[idx] = (sem.name,sem.value,None)
        self.dataChanged.emit(self.index(idx,0),self.index(idx,2))

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self.headerName[section])

sModel = SemaphoreModel()
