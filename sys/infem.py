#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys
import threading
import time
from infemGUI import *

#We should have a global lock, for the ou2Semaphore implementation
__synchro__ = threading.Condition()

class Semaphore():
    def __init__(self,value,name=None):
        if value < 0:
            raise ValueError('A semaphore should NOT be initialized with a negative value.')
        self.value = value
        self.name = name
        if sModel:
            sModel.addSemaphore(name,value)
        pass

    def acquire(self):
        """ acquire the semaphore.
        if the value is > 0, it decrements the semaphore value and returns
        otherwise, it blocks until value get > 0
        """
        with __synchro__:
            while self.value <= 0:
                if sModel:
                    sModel.addWaitingThread(self.name,threading.currentThread().name)
                __synchro__.wait()
            self.value -=1
            if sModel:
                sModel.update(self.name,self.value)

    def P(self):
        """ same as 'acquire'. wrapper for historical reasons """
        self.acquire()

    def release(self):
        """ release the semaphore.
        the value is incremented and a waiting threads can be woken up. Non blocking call.
        """
        with __synchro__:
            #notify all so that they are blocked again and we can deduce
            #the list of waiting threads.
            if sModel:
                sModel.clearWaitingThread((self.name,self.value))
            __synchro__.notify_all() 
            self.value +=1

    def V(self):
        """ same as 'release'. wrapper for historical reasons """
        self.release()

def ou2Semaphore(s1,s2,timeout=None):
    """ Wait for the first available semaphore between 2. If the 2 are available, s1 is chosen.
    returns 1 if s1 is chosen, 2 if s2. This is a blocking call.
    """
    if not isinstance(s1,Semaphore) or not isinstance(s2,Semaphore):
        raise Exception('Input is not a semaphore in ou2Semaphore')
    result = 0
    with __synchro__:
        #one already available
        if s1.value > 0:
            result = 1
            s1.value -=1
            if sModel:
                sModel.update(s1.name,s1.value)
        elif s2.value > 0:
            result = 2
            s2.value -=1
            if sModel:
                sModel.update(s2.name,s2.value)

        while result == 0: # we will block
            if sModel:
                threadName = threading.currentThread().name
                sModel.addWaitingThread(s1.name,threadName)
                sModel.addWaitingThread(s2.name,threadName)
            noTimeout = __synchro__.wait(timeout)
            if noTimeout:
                if s1.value > 0:
                    result = 1
                    s1.value -=1
                    if sModel:
                        sModel.update(s1.name,s1.value)
                        sModel.removeWaitingThread(s2.name,threading.currentThread().name)
                elif s2.value > 0:
                    result = 2
                    s2.value -=1
                    if sModel:
                        sModel.removeWaitingThread(s1.name,threading.currentThread().name)
                        sModel.update(s2.name,s2.value)
            else: #timeout
                result = 3 #timeout
    return result

