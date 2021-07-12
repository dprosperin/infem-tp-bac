#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys

"""
    pyuic5 bac.ui -o mainwindow.py
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore    import *
from PyQt5.QtGui     import *

import time

from debugEvents import *
from baseThreads import mainThread
from mainwindow import Ui_mainwindow    #fichier généré

import infemGUI
class MainWindow(QMainWindow, Ui_mainwindow):
    """ Application main window
        Build the application and start threads.
    """

    def __init__(self,*args,**kwargs):
        self.nb=0
        super(MainWindow,self).__init__(*args,**kwargs)
        self.setupUi(self)
        self.pbTerm.clicked.connect(self.terminateCallback)
        #semaphore view
        self.semaphoreView.setModel(infemGUI.sModel)
        infemGUI.sModel.updateColumnWidth.connect(self.semaphoreView.resizeColumnsToContents)
        infemGUI.sModel.updateColumnWidth.emit() #for semaphore already defined.
        #event list view
        self.debugEventModel = debugEventModel()
        self.eventListView.setModel(self.debugEventModel)
        self.debugEventModel.signalScroll.connect(self.eventListView.scrollToBottom)
        #threads
        appli = mainThread(self.labTerm,self.drawingWidget,self.debugEventModel)
        appli.start()

    def terminateCallback(self):
        self.labTerm.setText('Terminaison en cours…')
        self.terminateCalled()
