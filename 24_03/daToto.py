from queue import Queue
from threading import Condition, Thread, RLock
from time import sleep
from random import randint

class Pizzeria:
    def __init__(self,size):
        self.ordini = Queue
        self.pizze = {}
        self.size = size
        self.lock = RLock()

         # Condizione che viene utilizzata per notificare i thread che attendono che la coda non sia piÃ¹ tutta piena
        self.conditionTuttoPieno = Condition(self.lock)

        # Condizione che viene utilizzata per notificare i thread che attendono che la coda non sia piÃ¹ tutta vuota
        self.conditionTuttoVuoto = Condition(self.lock)

    def putOrdine(self,codP, quan):
        with self.lock:
            #
            # Se non ci sono slot liberi, il thread che invoca il metodo put viene bloccato
            #
            while len(self.ordini) == self.size:
                self.conditionTuttoPieno.wait()
            #
            # Questo if serve per evitare notify ridondanti
            # Non ci possono essere consumatori in attesa a meno che, un attimo prima della append(t) la coda non fosse totalmente vuota
            # Se non ci sono consumatori in attesa, non c'Ã¨ bisogno di notificare nessuno
            # Il codice Ã¨ corretto anche senza questo if, ma ci saranno notify anche quando non necessari
            #
            if len(self.ordini) == 0:
                self.conditionTuttoVuoto.notify()
            order = {codP, quan}
            
            self.ordini.append(order)
            return order

    def getOrdine(self):
        with self.lock:
            #
            # Se non ci sono elementi da estrarre, il thread che invoca il metodo get viene bloccato
            #
            while len(self.ordini) == 0:
                self.conditionTuttoVuoto.wait()
            #
            # Questo if serve per evitare notify ridondanti
            # Non ci possono essere produttori in attesa a meno che, un attimo prima della pop(0) la coda non fosse totalmente piena
            # Se non ci sono produttori in attesa, non c'Ã¨ bisogno di notificare nessuno
            # Il codice Ã¨ corretto anche senza questo if, ma ci saranno notify anche quando non necessari
            #
            if len(self.ordini) == self.size:
                self.conditionTuttoPieno.notify()
            return self.ordini.get()

    def putPizze(self,t,id):
        with self.lock:
            #
            # Se non ci sono slot liberi, il thread che invoca il metodo put viene bloccato
            #
            while len(self.ordini) == self.size:
                self.conditionTuttoPieno.wait()
            #
            # Questo if serve per evitare notify ridondanti
            # Non ci possono essere consumatori in attesa a meno che, un attimo prima della append(t) la coda non fosse totalmente vuota
            # Se non ci sono consumatori in attesa, non c'Ã¨ bisogno di notificare nessuno
            # Il codice Ã¨ corretto anche senza questo if, ma ci saranno notify anche quando non necessari
            #
            if len(self.pizze) == 0:
                self.conditionTuttoVuoto.notify()
            self.pizze[id] = t

    def getPizze(self, id):
        with self.lock:
            #
            # Se non ci sono elementi da estrarre, il thread che invoca il metodo get viene bloccato
            #
            while len(self.ordini) == 0:
                self.conditionTuttoVuoto.wait()
            #
            # Questo if serve per evitare notify ridondanti
            # Non ci possono essere produttori in attesa a meno che, un attimo prima della pop(0) la coda non fosse totalmente piena
            # Se non ci sono produttori in attesa, non c'Ã¨ bisogno di notificare nessuno
            # Il codice Ã¨ corretto anche senza questo if, ma ci saranno notify anche quando non necessari
            #
            if len(self.pizze) == self.size:
                self.conditionTuttoPieno.notify()
            pizze = [self.pizze[id]]
            del(self.pizze[id])
            return pizze

class Pizzaiolo(Thread):

    ordine = []

    def __init__(self,P,nome):
        super().__init__()
        self.pizzeria = P
        self.nome = nome
        
    def run(self):
        disponibilità = 200
        while disponibilità > 0:
            disponibilità -= 1
            self.prelievaOrdine

    def prelievaOrdine(self):
        self.ordine = self.pizzeria.getOrdine
        attesa = 2*self.ordine[1]
        self.elaboraOrdine(attesa)

    def elaboraOrdine(self,attesa):
        sleep(attesa)
        self.ordinePronto

    def ordinePronto(self):
        self.pizzeria.putPizze(self.ordine[0])
        


class Cliente(Thread):
    id = 0

    def __init__(self,P,nome):
        super().__init__()
        self.pizzeria = P
        self.nome = nome

    def run(self):
        disponibilità = 200
        while disponibilità > 0:
            disponibilità -= 1
            self.creaOrdine

    def creaOrdine(self):
        cod = randint(0,4)
        quan = randint(1,15)
        id += 1 
        self.pizzeria.putOrdine(cod, quan, id)
        self.aspetta(quan,id)
        
    def aspetta(self,attesa, idd):
        sleep(2*attesa)
        self.richiamaOrdine(idd)

    def richiamaOrdine(self, idd):
        self.pizzeria.getPizze(idd)
        

if __name__ == "__main__":
    
    # crea una coda di dimensione 10
    daToto = Pizzeria(10)

    #
    # Crea 10 pizzaioli e 10 Clienti e li avvia
    #
    for c in range(0,10):
        newPizzaiolo = Pizzaiolo(daToto,f"Pizzaiolo-{c}")
        newPizzaiolo.start()
    
    for c in range(0,10):
        newCliente = Cliente(daToto,f"Cliente-{c}")
        newCliente.start()