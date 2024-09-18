

import math
import multiprocessing
from threading import Condition, Lock, Thread
import time


class Barrier:

    def __init__(self,n):

        self.soglia = n
        self.threadArrivati = 0
        self.lock = Lock()
        self.condition = Condition(self.lock)

    def wait(self):
        with self.lock:
            self.threadArrivati += 1

            if self.threadArrivati == self.soglia:
                self.condition.notifyAll()

            while self.threadArrivati < self.soglia:
                self.condition.wait()

class ExtendedBarrier(Barrier):
    def __init__(self, soglia):
        self.soglia = soglia
        self.threadArrivati = 0
        self.lock = Lock()
        self.condizione = Condition(self.lock)

    def finito(self):
        super.threadArrivati+=1
        self.condition.notifyAll()

    def aspettaEbasta(self):
        with self.lock:
            while self.threadArrivati < self.soglia:
                self.condition.wait()

    def wait(self):
        finito()
        aspettaEbasta()


class DoppiaBarriera:

    def __init__(self, n0, n1):
        self.barriera0 = ExtendedBarrier(n0)
        self.barriera1 = ExtendedBarrier(n1)
        self.lock = threading.Lock()

    def finito(self, numSoglia):
        if numSoglia == 0:
            self.barriera0.finito()
        elif numSoglia == 1:
            self.barriera1.finito()

    def aspettaEbasta(self, numSoglia):
        if numSoglia == 0:
            self.barriera0.aspettaEbasta()
        elif numSoglia == 1:
            self.barriera1.aspettaEbasta()

    def wait(self, numSoglia):
        self.finito(numSoglia)
        self.aspettaEbasta(numSoglia)

    def waitAll(self):
        with self.lock:
            self.finito(0)
            self.finito(1)
            self.aspettaEbasta(0)
            self.aspettaEbasta(1)
