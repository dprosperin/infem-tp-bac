#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

import threading
import time
import sys 

from debugEvents import *

sys.path.append("../sys")
import infem
import infemGUI
import random

from fysom import Fysom,FysomError #sudo pip3 install fysom

class ferry(threading.Thread):
    """ classe du thread de gestion du Bac 
        La fonction principale 'run' doit être definie dans le tp
    """
    fsmString = {'atStart': 'au départ',
                 'crossing': 'en traversée', 
                 'atEnd': "à l'arrivée",
                 'returning': 'en retour'}
    def __init__(self,qdrawing,debugEventModel=None):
        threading.Thread.__init__(self,name='ferry',daemon=True)
        self.drawing = qdrawing
        self.debugEventModel = debugEventModel

        self.fsm = Fysom (initial='atStart',
                          events = [('crosses','atStart','crossing'),
                                    ('arrivesAtEnd','crossing','atEnd'),
                                    ('comesBack','atEnd','returning'),
                                    ('arrivesAtStart','returning','atStart')
                                    ])
    
    def check(self,cond,info,msgIfOk=True):
        """ basic verification (assert(cond)). 
        If the condition is not ok, report the pb and ends the thread.
        info is an extra information (char string)
        """
        if not cond:
            msg = "erreur '"+info+"': bac dans l'état '"+ferry.fsmString[self.fsm.current]
            if self.debugEventModel:
                self.debugEventModel.addEv(1,msg)
            print(msg)
            sys.exit(1)
        else:
            if self.debugEventModel and msgIfOk:
                self.debugEventModel.addEv(0,'ferry: : '+info)

    def log(self,txt):
        if self.debugEventModel:
            if isinstance(txt,str):
                self.debugEventModel.addEv(2,txt)
            else:
                self.debugEventModel.addEv(1,'bad argument when calling log')

    def traverser(self):
        self.check(self.fsm.isstate('atStart'),'traverser')
        try:
            self.fsm.crosses()
            for i in range(40):
                time.sleep(.05)
                self.drawing.setFerryPos(i/40.)
            self.fsm.arrivesAtEnd()
        except FysomError:
            self.check(True,'ordre incorrect des étapes')

    def revenir(self):
        self.check(self.fsm.isstate('atEnd'),'revenir')
        try:
            self.fsm.comesBack()
            for i in range(40):
                time.sleep(.03)
                self.drawing.setFerryPos(1-i/40.)
            self.fsm.arrivesAtStart()
        except FysomError:
            self.check(True,'ordre incorrect des étapes')

class car(threading.Thread):
    """ classe des threads de gestion des voitures
        La fonction principale 'run' doit être definie dans le tp
    """
    fsmString = {'atStart': 'au départ',
                 'driving': 'en route', 
                 'waitingForFerry': 'en attente du bac',
                 'loading': 'en chargement',
                 'inFerry': 'dans le bac',
                 'unloading': 'en déchargement du ferry'}
    def __init__(self,qdrawing,carId,ferry,debugEventModel=None):
        threading.Thread.__init__(self,name='car '+str(carId),daemon=True)
        self.drawing = qdrawing
        self.carId = carId
        self.ferry = ferry #to check states and report any error only!
        self.debugEventModel = debugEventModel
        random.seed()
        self.fsm = Fysom (initial='atStart',
                          events = [('drive','atStart','driving'),
                                    ('arrive','driving','waitingForFerry'),
                                    ('load','waitingForFerry','loading'),
                                    ('loadComplete','loading','inFerry'),
                                    ('unloading','inFerry','unloading'),
                                    ('unloadComplete','unloading','atStart')
                                    ])

    def check(self,cond,info,msgIfOk=True):
        """ basic verification (assert(cond)).
        If the condition is not ok, report the pb and ends the thread.
        info is an extra information (char string)
        """
        if not cond:
            msg = "erreur '"+info+"': voiture "+str(self.carId) +" dans l'état '"+car.fsmString[self.fsm.current]+"' et bac dans l'état '"+self.ferry.fsmString[self.ferry.fsm.current]+"'"
            if self.debugEventModel:
                self.debugEventModel.addEv(1,msg)
            print(msg)
            sys.exit(1)
        else:
            if self.debugEventModel and msgIfOk:
                self.debugEventModel.addEv(0,'voiture '+str(self.carId)+': '+info)

    def log(self,txt):
        if self.debugEventModel:
            if isinstance(txt,str):
                self.debugEventModel.addEv(2,txt)
            else:
                self.debugEventModel.addEv(1,'bad argument when calling log')

    def avancer(self):
        #drive
        self.check(self.fsm.isstate('atStart'),'avancer')
        try:
            self.fsm.drive()
            speed = random.random()/5+0.05
            for i in range(70):
                time.sleep(speed)
                self.drawing.setDrivePos(i/70.,self.carId)
            self.fsm.arrive()
        except FysomError:
            self.check(True,'ordre incorrect des étapes')

    def embarquer(self):
        self.check(self.fsm.isstate('waitingForFerry') and self.ferry.fsm.isstate('atStart'),'embarquer')
        try:
            self.fsm.load()
            for i in range(20):
                time.sleep(.03)
                self.drawing.setLoadPos(i/19.,self.carId)
                self.check(self.ferry.fsm.isstate('atStart'),'embarquer',msgIfOk=False)
            self.drawing.setLoaded(self.carId)
            self.fsm.loadComplete()
        except FysomError:
            self.check(True,'ordre incorrect des étapes')

    def debarquer(self):
        self.check(self.fsm.isstate('inFerry') and self.ferry.fsm.isstate('atEnd'),'debarquer')
        try:
            self.fsm.unloading()
            for i in range(20):
                time.sleep(.03)
                self.drawing.setUnloadPos(i/19.,self.carId)
                self.check(self.ferry.fsm.isstate('atEnd'),'debarquer',msgIfOk=False)
            self.fsm.unloadComplete()
        except FysomError:
            self.check(True,'ordre incorrect des étapes')

class mainThread(threading.Thread):
    """ Main thread that starts all the threads (car/ferry) and checks for correct termination.
    """
    def __init__(self,label,qdrawing,debugEventModel=None):
        threading.Thread.__init__(self,name='main',daemon=True)
        self.ferryThread = ferry(qdrawing,debugEventModel)
        self.label = label
        self.carThreads = [None] * 10
        for i in range(10): 
            self.carThreads[i] = car(qdrawing,i,self.ferryThread,debugEventModel)

    def run(self):
        #run
        for c in self.carThreads:
            c.start()
        self.ferryThread.start()
        #wait for termination
        for c in self.carThreads:
            c.join()
        self.ferryThread.join()
        self.label.setText("Ok!")
        
