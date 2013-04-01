#!/usr/bin/python
import math
from numpy import array
from numpy import nonzero
from random import randrange
import darkheresy

ARMAS_CC = 39
NUMREPETICIONES = 10

print "TOTAL PRUEBAS: ",  NUMREPETICIONES

"""
	name : nombre del arma
	caracteristica : asociada al arma, cuerpo a cuerpo o armas a distancia.
	damage: danio del arma (incluye bonificacion por fuerza.
	properties: cualidades extra del arma.

"""

testArmas = [
	{'name' : 'sierra', 
		'caracteristica' : 39, 
		'damage': '1D10+2', 
		'properties' : 	{ 'DESGARRADORA' : True, 'EQUILIBRADA' : True  , 'MEJORCALIDAD' : True } 
	},
	{'name' : 'espadaEnergia', 
		'caracteristica' : 39, 
		'damage': '1D10+5', 
		'properties' : { 'EQUILIBRADA' : True  } 
	},
	{'name' : 'arma2manos', 
		'caracteristica' : 39, 
		'damage': '2D10' 
	}
]

DEBUG = False
result = {}
for arma in testArmas:
	tiradas = []
	for i in range(NUMREPETICIONES):
		if darkheresy.atackRoll(arma):
			tiradas.append(darkheresy.damage(arma))
		else:
			tiradas.append(0)
	a = array(tiradas)
	print ""
	print arma['name']," ataques acertados: ", len(a[nonzero(a)])
	print "Ataque min/max : " , a.min() , "/", a.max()
	print "Ataque medio (sin zeros) / total: " , round(a[nonzero(a)].mean(),2), "/" , a.mean() 
	print "Ataque desviacion : ", round(a.std(),3)
	result[arma['name']] = tiradas
	if DEBUG:
		print tiradas
print result 