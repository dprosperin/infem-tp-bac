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
    self.log("ne fait rien…")
    time.sleep(1)

def carRun(self):
    """ fonction principale de chaque voiture. Les méthodes principales sont:
        - self.avancer()
        - self.embarquer()
        - self.debarquer()
    """
    self.avancer()
    self.log("devant l'eau!")
    time.sleep(1)

def terminateCalled(self):
    """ fonction appelée lors d'un clic sur le bouton de terminaison """
    print("L'application doit se terminer correctement")

#associe les fonctions aux methodes de classes (ne pas modifier)
ferry.run = ferryRun
car.run = carRun

#main…
if __name__ == '__main__':
    from bacGUI import MainWindow
    MainWindow.terminateCalled = terminateCalled
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_() #event loop
