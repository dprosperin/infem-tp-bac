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

    #We use 'update signals' because the modification of the model
    # from another thread is not possible (QObject is not thread safe).
    # so we use an internal signal:
    #  - the thread calls the method (addWaitingThread, …)
    #  - the methods sends a signal to the method that ends with …GUIThread
    #  - … that can perform the update.
    signalAddWaitingThread    = pyqtSignal(str,str)
    signalClearWaitingThread  = pyqtSignal(tuple)
    signalRemoveWaitingThread = pyqtSignal(str,str)
    signalUpdate              = pyqtSignal(str,int)
    signalAddSemaphore        = pyqtSignal(str,int)

    updateColumnWidth = pyqtSignal()
    def __init__(self,*args,todos=None,**kwargs):
        super(SemaphoreModel,self).__init__(*args,**kwargs)
        self.semaphores = []      #tuple: name - value - threads
        self.waitingThreads = {}  #name => waiting threads
        self.semaphoreNames = {}  #name => index
        #self.headerName = ['name','value','waiting threads']
        self.headerName = ['nom','valeur',"liste d'attente"]
        self.signalAddWaitingThread.connect(self.addWaitingThreadGUIThread)
        self.signalClearWaitingThread.connect(self.clearWaitingThreadGUIThread)
        self.signalRemoveWaitingThread.connect(self.removeWaitingThreadGUIThread)
        self.signalUpdate.connect(self.updateGUIThread)
        self.signalAddSemaphore.connect(self.addSemaphoreGUIThread)

    def data(self,index,role): #index: row,column
        assert threading.current_thread() is threading.main_thread()
        #print('data required '+str(index.row())+','+str(index.column()))
        if role == Qt.DisplayRole:
            data = self.semaphores[index.row()]
            return data[index.column()]
        if role == Qt.ForegroundRole:
            if self.semaphores[index.row()][2]: #Are there waiting threads?
                return QColor('red')
            return QColor('black')
            
    def addSemaphore(self,name,value):
        self.signalAddSemaphore.emit(name,value)

    @pyqtSlot(str,int)
    def addSemaphoreGUIThread(self,name,value):
        assert threading.current_thread() is threading.main_thread()
        #print('add the semaphore '+str(name))
        self.semaphoreNames[name] = len(self.semaphores)
        self.semaphores.append((name,value,None))
        self.waitingThreads[name] = set()
        self.updateColumnWidth.emit()
        self.layoutChanged.emit()

    def rowCount(self,index):
        return len(self.semaphores)

    def columnCount(self,index):
        return 3

    def update(self,name,value):
        self.signalUpdate.emit(name,value)

    @pyqtSlot(str,int)
    def updateGUIThread(self,name,value):
        assert threading.current_thread() is threading.main_thread()
        idx = self.semaphoreNames[name]
        self.semaphores[idx] = (name,value,self.semaphores[idx][2])
        self.dataChanged.emit(self.index(idx,0),self.index(idx,2))

    def removeWaitingThread(self,semName,threadName):
        self.signalRemoveWaitingThread.emit(semName,threadName)

    @pyqtSlot(str,str)
    def removeWaitingThreadGUIThread(self,semName,threadName):
        assert threading.current_thread() is threading.main_thread()
        idx = self.semaphoreNames[semName]
        self.waitingThreads[semName].remove(threadName)
        sortedList = sorted(self.waitingThreads[semName])
        threads = ' - '.join(sortedList)
        self.semaphores[idx] = (semName,-len(self.waitingThreads[semName]),threads)
        self.dataChanged.emit(self.index(idx,0),self.index(idx,2))

    def addWaitingThread(self,semName,threadName):
        self.signalAddWaitingThread.emit(semName,threadName)

    @pyqtSlot(str,str)
    def addWaitingThreadGUIThread(self,semName,threadName):
        #should be called from the main thread
        assert threading.current_thread() is threading.main_thread()
        idx = self.semaphoreNames[semName]
        self.waitingThreads[semName].add(threadName)
        sortedList = sorted(self.waitingThreads[semName])
        threads = ' - '.join(sortedList)
        self.semaphores[idx] = (semName,-len(self.waitingThreads[semName]),threads)
        self.dataChanged.emit(self.index(idx,0),self.index(idx,2))

    @pyqtSlot(tuple)
    def clearWaitingThread(self,sem):
        self.signalClearWaitingThread.emit(sem)

    def clearWaitingThreadGUIThread(self,sem):
        assert threading.current_thread() is threading.main_thread()
        name = sem[0]
        value= sem[1]
        idx = self.semaphoreNames[name]
        self.waitingThreads[name].clear()
        self.semaphores[idx] = (name,value,None)
        self.dataChanged.emit(self.index(idx,0),self.index(idx,2))

    def headerData(self, section, orientation, role):
        assert threading.current_thread() is threading.main_thread()
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self.headerName[section])

sModel = SemaphoreModel()
