from random import random

array = []

#Aggiungere all'array 100 numeri random compresi tra 0 e 100

for i in range(100):      
	array.append(random()*100)

#Stampare gli elementi dell'array
for a in  array:
	print(a)

#Trovare il valore massimo dell'array
curMax = array[0]
for i in range(0, len(array)-1):    		
	if array[i+1] > curMax:       
		curMax = array[i+1]