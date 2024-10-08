from threading import Thread, Lock
from random import random, randrange
from time import sleep

class Striscia:
	LUNG=20

	def __init__(self):
		self.Sl=list()
		self.posGatto=randrange(0,self.LUNG-1)
		self.posTopo=randrange(0,self.LUNG-1)
		
		for i in range(0,self.LUNG):
			self.Sl.append( ' ' )
		self.Sl[self.posGatto]="*"
		self.Sl[self.posTopo]="."
		
		self.lock=Lock()
		self.direzGatto=1
		self.fine=False

		
	def stampaStriscia(self):
		self.S="".join(self.Sl)			#joina la nuova stringa alla lista su cui si lavora
		for i in range(len(self.S)):
			print(self.S[i], end='', flush=True)		#printa ogni carattere nella stringa senza andare a capo, altrimenti non si capirebbe
		print('\n')
		return self.fine							#sarà true quando gatto e topo saranno nella stessa posizione


	def muoviGatto(self):
		with self.lock:				#serve per rilasciare il lock dopo aver fatto la return, altrimenti sarebbe impossibile farlo
			if not self.fine:			#se gatto e topo non sono nella stessa posizione...
				
				if self.posGatto + self.direzGatto > self.LUNG-1 or self.posGatto + self.direzGatto < 0:		#controlla che apportando modifiche alla posizione del gatto non si vada fuori dalla stringa
					self.direzGatto=-self.direzGatto				#se succede si inverte la direzione
				self.Sl[self.posGatto]=" "
				
				self.posGatto=self.posGatto + self.direzGatto		#incrementa o decrementa velocemente la posizione del gatto
				
				self.Sl[self.posGatto]="*"

				if  self.posGatto == self.posTopo:
					self.fine = True
		
			return self.fine


	def muoviTopo(self):
		with self.lock:
			if not self.fine:
				pos=randrange(0,3)
				if pos==0:
					if  self.posGatto == self.posTopo:
						self.fine = True
					return self.fine
				
				elif pos==1 and self.posTopo<self.LUNG-1:
					self.Sl[self.posTopo]=" "
					self.posTopo=self.posTopo+1
					self.Sl[self.posTopo]="."
					
					if  self.posGatto == self.posTopo:
						self.fine = True
					return self.fine
				
				elif pos==2 and self.posTopo>0:
					self.Sl[self.posTopo]=" "
					if self.posTopo>0:
						self.posTopo=self.posTopo-1
						self.Sl[self.posTopo]="."
					else:
						return False
					if  self.posGatto == self.posTopo:
						self.fine = True
					return self.fine
			return self.fine



class Display(Thread):
	def __init__(self, S:Striscia):
		super().__init__()
		self.S = S

	def run(self):
		while(not self.S.stampaStriscia()):		
			sleep(0.5)


class Gatto(Thread):
	def __init__(self, S:Striscia):
		super().__init__()
		self.S = S

	def run(self):
		while(not self.S.muoviGatto()):
			sleep(0.5)



class Topo(Thread):
	def __init__(self, S:Striscia):
		super().__init__()
		self.S = S

	def run(self):
		while(not self.S.muoviTopo()):
			sleep(0.5)




St = Striscia()

display = Display(St)
gatto = Gatto(St)
topo = Topo(St)

display.start()
gatto.start()
topo.start()

print("Partiti!")