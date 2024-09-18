from collections import deque
from threading import Condition, Thread, RLock, Event
from random import randint

Nconti = 1000
Contat = 200000

class Transazione:
    def __init__(self, sorg, dest, val):
        self.sorgente = sorg
        self.destinazione = dest
        self.valore = val

class ContoBancario(Thread):
    iter = 0
   
    def __init__(self, id, nome, banca, file):
        super().__init__()
        self.lock = RLock()
        self.file = file
        self.saldo = randint(5000, 12000)
        self.IDConto=id
        self.nome = nome
        self.banca = banca
        self.transazioni = deque(maxlen=50)

    def run(self):
        while self.iter<Contat:
            self.iter+=1
            self.sposta()
        self.file.write(f" ------- {self.getNome()} ha {self.getSaldo()}€\n\n")
            
    def incrementaSaldo(self, N):
        self.saldo+=N

    def decrementaSaldo(self, N):
        self.saldo-=N

    def sposta(self):
        with self.lock:
            A = self.IDConto
            B = A
            while B == A:
                B = randint(0, len(self.banca.ContiBancari)-1)
            N = randint(200, 800)
            if(not self.banca.trasferisci(A, B, N)):
                print(f" ---------------------- {self.getNome()} non ha Fondiiiii!")
                return False
            return True

    def aggiungiTransazione(self, transazione):
        self.transazioni.append(transazione)

    def getSaldo(self):
        return self.saldo

    def getNome(self):
        return self.nome

class Banca:
    ContiBancari = dict()       #dizionario, per ottimizzare la time complexity
    IDConto = 0
    numConti = 0
    
    def __init__(self):
        self

    def creaConto(self, file):
        self.ContiBancari[self.numConti] = ContoBancario(self.IDConto, "Conto_" + str(self.numConti), self, file)
        self.ContiBancari[self.numConti].start()
        self.numConti+=1
        self.IDConto+=1
        
    def trasferisci(self, A, B, N):
        try:
            if self.ContiBancari[A].getSaldo()<=0:
                return False
            if(N>self.ContiBancari[A].getSaldo()):
                return False
            transazione = Transazione(A, B, N)
            self.ContiBancari[A].decrementaSaldo(N)
            self.ContiBancari[A].aggiungiTransazione(transazione)
            self.ContiBancari[B].incrementaSaldo(N)
            self.ContiBancari[B].aggiungiTransazione(transazione)
            print(f" - {self.ContiBancari[A].getNome()} invia {N}€")
            return True
        finally:
            pass
        return False
            
    def getSaldo(self, C):
        try:
            return self.ContiBancari[C].getSaldo()
        finally:
            print("Non Trovato!")

                
if __name__ == "__main__":
    
    saldi = open("saldi.txt", "w")

    # crea
    Credem = Banca()


    while Credem.numConti < Nconti:
        Credem.creaConto(saldi)