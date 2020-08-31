#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys
import threading
import time
from infemGUI import *

__synchro__ = threading.Condition()

class Semaphore():
    def __init__(self,value,name=None):
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
        __synchro__.acquire() #get the lock
        while self.value <= 0:
            if sModel:
                sModel.addWaitingThread(self,threading.currentThread().name)
            __synchro__.wait()
        self.value -=1
        if sModel:
            sModel.update(self)
        __synchro__.release()

    def P(self):
        """ same as 'acquire'. wrapper for historical reasons """
        self.acquire()

    def release(self):
        """ release the semaphore.
        the value is incremented and a waiting threads can be woken up. Non blocking call.
        """
        __synchro__.acquire() #get the lock
        #notify all so that they are blocked again and we can deduce
        #the list of waiting threads.
        __synchro__.notify_all() 
        self.value +=1
        if sModel:
            sModel.clearWaitingThread(self)
        __synchro__.release()

    def V(self):
        """ same as 'release'. wrapper for historical reasons """
        self.release()

def ou2Semaphore(s1,s2):
    """ Wait for the first available semaphore between 2. If the 2 are available, s1 is chosen.
    returns 1 if s1 is chosen, 2 if s2. This is a blocking call.
    """
    if not isinstance(s1,Semaphore) or not isinstance(s2,Semaphore):
        raise Exception('Input is not a semaphore in ou2Semaphore')
    result = 0
    __synchro__.acquire()

    #one already available
    if s1.value > 0:
        result = 1
        s1.value -=1
    elif s2.value > 0:
        result = 2
        s2.value -=1

    while result == 0: # we will block
        __synchro__.wait()
        if s1.value > 0:
            result = 1
            s1.value -=1
        elif s2.value > 0:
            result = 2
            s2.value -=1
    __synchro__.release()
    return result

