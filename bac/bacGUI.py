#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys

"""
    pyuic5 bac.ui -o mainwindow.py
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore    import *
from PyQt5.QtGui     import *

import threading
import time

from debugEvents import *
from baseThreads import *
from mainwindow import Ui_mainwindow    #fichier généré

class MainWindow(QMainWindow, Ui_mainwindow):
    """ Application main window
        Build the application and start threads.
    """

    def __init__(self,*args,**kwargs):
        self.nb=0
        super(MainWindow,self).__init__(*args,**kwargs)
        self.setupUi(self)
        #semaphore view
        self.semaphoreView.setModel(infemGUI.sModel)
        infemGUI.sModel.updateColumnWidth.connect(self.semaphoreView.resizeColumnsToContents)
        #event list view
        self.debugEventModel = debugEventModel()
        self.eventListView.setModel(self.debugEventModel)
        #threads
        ferryThread = ferry(self.drawingWidget,self.debugEventModel)
        carThreads = [None] * 10
        for i in range(10): 
            carThreads[i] = car(self.drawingWidget,i,ferryThread,self.debugEventModel)
        for c in carThreads:
            c.start()
        ferryThread.start()

