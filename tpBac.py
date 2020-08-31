#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys
sys.path.append("sys")
sys.path.append("bac")
import infem
import infemGUI
from baseThreads import *

import time

#déclaration des sémaphores: valeur init, info pour le debug
semaphore1 = infem.Semaphore(3,"info sur le sémaphore 1")

def ferryRun(self):
    """ fonction principale du bac. Les methodes principales sont:
        - self.traverser()
        - self.revenir()
    """
    while True:
        time.sleep(1)

def carRun(self):
    """ fonction principale de chaque voiture. Les méthodes principales sont:
        - self.avancer()
        - self.embarquer()
        - self.debarquer()
    """
    while True:
        self.avancer()
        time.sleep(1)

#associe les fonctions aux methodes de classes (ne pas modifier)
ferry.run = ferryRun
car.run = carRun

#main…
if __name__ == '__main__':
    from bacGUI import MainWindow
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_() #event loop
