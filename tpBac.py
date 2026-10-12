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
s5_arret          = infem.Semaphore(0,"arret")

def ferryRun(self):
    """ fonction principale du bac. Les methodes principales sont:
        - self.traverser()
        - self.revenir()
    """
    # s5_arret.plusUn()
    isRunning = True
    while isRunning :
        # initialise a moins -4 le ferry
        for i in range(4):
            #s2_depart_ferry.moinsUn()     
            departOuArret = infem.ou2Semaphore(s5_arret,s2_depart_ferry) 

            if departOuArret == 1:
                self.log("annulation depart : 1")
                s5_arret.plusUn()
                isRunning = False

            elif departOuArret == 2:
                self.log("depart du ferry: 2")

                self.traverser()
                self.log("arrivé du ferry")

                # reset à 0 pour le débrquement
                for i in range(4):
                    s3_debarquement_voiture.plusUn()

                for i in range(4):
                    #s4_revenir_ferry.moinsUn()
                    revenirOuArret = infem.ou2Semaphore(s5_arret,s4_revenir_ferry) 

                    if departOuArret == 1:
                        self.log("annulation revenir : 1")
                        s5_arret.plusUn()
                        isRunning = False

                    if departOuArret == 2:
                        self.log("retour du ferry: 2")
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
    isRunning = True
    while isRunning :
        self.avancer() 
        
        #faire avancer les voiture
        # Laisse passé sur le ferry les 4 première voiture
        # s1_attente_4_voiture.moinsUn()
        attenteVoitureOuArret = infem.ou2Semaphore(s5_arret,s1_attente_4_voiture)

        if attenteVoitureOuArret == 1:
            self.log("arret de l'embarquement : 1")
            s5_arret.plusUn()
            isRunning = False
            
        elif attenteVoitureOuArret == 2:
                self.embarquer()
                self.log("+ 1 vehicule embarqué : 2")
                # Incrémente pour démarer le ferry
                s2_depart_ferry.plusUn()
        
                # attend que le ferry est reset à 0 pour débarquer
                #s3_debarquement_voiture.moinsUn()
                descendreVoitureOuArret = infem.ou2Semaphore(s3_debarquement_voiture,s5_arret)

                if descendreVoitureOuArret == 1:
                        self.debarquer()
                        self.log("Débarquement " + self.name)
                        # Incrémente pour faire revenir le ferry quand les véhicule on débarquer tah 45
                        s4_revenir_ferry.plusUn()

                elif  descendreVoitureOuArret == 2:
                        self.log("arret du debarquement : 2")
                        s5_arret.plusUn()
                        isRunning = False


def terminateCalled(self):
    """ fonction appelée lors d'un clic sur le bouton de terminaison """
    print("L'application doit se terminer correctement")
    s5_arret.plusUn()
    

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
