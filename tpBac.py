#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys
sys.path.append("sys")
sys.path.append("bac")
import infem
import infemGUI
from baseThreads import *

import time
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

#déclaration des sémaphores: valeur init, info pour le debug
s1_attente_4_voiture = infem.Semaphore(4,"Embarquement véhicules")
s2_depart_ferry = infem.Semaphore(0,"Départ ferry")
s3_debarquement_voiture = infem.Semaphore(0, "Débarquement véhicules")
s4_revenir_ferry  = infem.Semaphore(0,"revenir ferry")


def ferryRun(self):
    """ fonction principale du bac. Les methodes principales sont:
        - self.traverser()
        - self.revenir()
    """
    while True :
        # initialise a moins -4 le ferry
        for i in range(4):
            s2_depart_ferry.moinsUn()

        self.traverser()
        self.log("arrivé")

        # reset à 0 pour le débrquement
        for i in range(4):
            s3_debarquement_voiture.plusUn()

        for i in range(4):
            s4_revenir_ferry.moinsUn()

        self.revenir()

        for i in range(4):
            s1_attente_4_voiture.plusUn()

        self.log('fin')

def carRun(self):
    """ fonction principale de chaque voiture. Les méthodes principales sont:
        - self.avancer()
        - self.embarquer()
        - self.debarquer()
    """
    while True :
        self.avancer() #faire avancer les voiture
        # Laisse passé sur le ferry les 4 première voiture
        s1_attente_4_voiture.moinsUn()
        self.embarquer()
        self.log("4 véhicules embarqués")
        # Incrémente pour démarer le ferry
        s2_depart_ferry.plusUn()

        # attend que le ferry est reset à 0 pour débarquer
        s3_debarquement_voiture.moinsUn()
        self.debarquer()
        self.log("Débarquement " + self.name)

        # Incrémente pour faire revenir le ferry quand les véhicule on débarquer tah 45
        s4_revenir_ferry.plusUn()



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
