import threading
import random
import time

class VasettoDiMiele:
    def __init__(self, indice, capacita):
        self.capacita = capacita
        self.miele = capacita
        self.indice = indice
        self.lock = threading.RLock()
        self.condition_aggiungi = threading.Condition(self.lock)
        self.condition_diminuizione = threading.Condition(self.lock)
        self.condition_riempi = threading.Condition(self.lock)

    def totaleMiele(self):
        print(f"il vasetto {self.indice} ha {self.miele} unità")
    
    #
    # Si sblocca solo quando il vasetto Ã¨ totalmente vuoto
    #
    def riempi(self):
        with self.lock:
            print(f"\t\t\t\t{threading.current_thread().name} DEVE RIEMPIRE il vasetto {self.indice}")
            if self.miele==self.capacita:
                self.condition_diminuizione.notify_all()
                return
            if self.miele > 0:
                self.condition_diminuizione.notify_all()
                print(f"Il vasetto {self.indice} ha {self.miele} unità  di miele, aspetto che si svuoti completamente")
            while self.miele > 0:
                self.condition_riempi.wait()
            self.miele = self.capacita
            print(f"{threading.current_thread().name} ha rabboccato il vasetto {self.indice}")

    #
    # Preleva del miele dal vasetto
    #
    def prendi(self, quantita):
        with self.lock:
            print(f"\t\t\t\t{threading.current_thread().name} DEVE PRENDERE {quantita} DAl vasetto {self.indice}")
            if self.miele == 0:
                self.condition_riempi.notify()
                print(f"Il vasetto {self.indice} è vacante")
            if self.miele < quantita:
                self.condition_aggiungi.notify_all()
                print(f"Il vasetto {self.indice} ha {self.miele} unitÃ  di miele, non posso prenderne {quantita}. Aspetto che venga riempito")
            while self.miele < quantita:
                self.condition_diminuizione.wait()
            self.miele -= quantita
            if self.miele==0:
                self.condition_riempi.notify()
            print(f"{threading.current_thread().name} ha preso {quantita} unitÃ  di miele dal vasetto {self.indice}")


    def aggiungi(self, quantita):
        with self.lock:
            print(f"\t\t\t\t{threading.current_thread().name} DEVE AGGIUNGERE {quantita} Al vasetto {self.indice}")
            if self.miele + quantita > self.capacita:
                self.condition_diminuizione.notify_all()
                print(f"Il vasetto {self.indice} ha {self.miele} unità  di miele, aggiungerne {quantita} supererebbe la capacità  massima che è {self.capacita}")
            while self.miele + quantita > self.capacita:
                self.condition_aggiungi.wait()
            self.miele += quantita
            print(f"{threading.current_thread().name} ha aggiunto {quantita} unitÃ  di miele al vasetto {self.indice}")


class OrsettoThread(threading.Thread):
    def __init__(self, name, vasettiMiele):
        threading.Thread.__init__(self)
        self.name = name
        self.vasettiMiele = vasettiMiele
        self.x=0

    def run(self):
        while self.x<5:
            self.x+=1
            time.sleep(0.7)
            vasetto_indice = random.randint(0, len(self.vasettiMiele)-1)
            quantita = random.randint(1,self.vasettiMiele[vasetto_indice].capacita)
            self.vasettiMiele[vasetto_indice].prendi(quantita)
            self.vasettiMiele[vasetto_indice].totaleMiele()

class PapaOrsoThread(threading.Thread):
    def __init__(self, name, vasettiMiele):
        threading.Thread.__init__(self)
        self.name = name
        self.vasettiMiele = vasettiMiele
        self.x=0

    def run(self):
        while self.x<5:
            self.x+=1
            time.sleep(0.7)
            vasetto_indice1 = random.randint(0, len(self.vasettiMiele)-1)
            vasetto_indice2 = random.randint(0, len(self.vasettiMiele)-1)
            while vasetto_indice1 == vasetto_indice2:
                vasetto_indice2 = random.randint(0, len(self.vasettiMiele)-1)
            quantita = random.randint(1, self.vasettiMiele[vasetto_indice1].capacita)
            self.vasettiMiele[vasetto_indice1].prendi(quantita)
            self.vasettiMiele[vasetto_indice2].aggiungi(quantita)
            self.vasettiMiele[vasetto_indice1].totaleMiele()
            self.vasettiMiele[vasetto_indice2].totaleMiele()

class MammaOrsoThread(threading.Thread):
    def __init__(self, name, vasettiMiele):
        threading.Thread.__init__(self)
        self.name = name
        self.vasettiMiele = vasettiMiele
        self.x=0

    def run(self):
        while self.x<5:
            self.x+=1
            time.sleep(0.7)
            vasetto_indice = random.randint(0, len(self.vasettiMiele)-1)
            self.vasettiMiele[vasetto_indice].riempi()
            self.vasettiMiele[vasetto_indice].totaleMiele()


if __name__ == '__main__':
    num_vasetti = 5
    vasetti = [VasettoDiMiele(i,10) for i in range(num_vasetti)]

    orsetti = [OrsettoThread(f"Winnie-{i}", vasetti) for i in range(5)]
    mamme_orse = [MammaOrsoThread(f"Mamma-{i}",vasetti) for i in range(2)]
    papa_orso = [PapaOrsoThread(f"Babbo-{i}", vasetti) for i in range(3)]

 
    for orsetto in orsetti:
        orsetto.start()
 
    for orsa in mamme_orse:
        orsa.start()

    for orso in papa_orso:
        orso.start()
        
    