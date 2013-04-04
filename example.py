# coding=UTF-8

import math
from numpy import array
from numpy import nonzero
from random import randrange
from weapon import Weapon
from character import Character
import darkheresy
import copy

ARMAS_CC = 39
NUMREPETICIONES = 10000
DEBUG = False


"""
	name : nombre del arma
	caracteristica : asociada al arma, cuerpo a cuerpo o armas a distancia.
	damage: danio del arma (incluye bonificacion por fuerza.
	properties: cualidades extra del arma.

"""

pjs = [
	{
		'name' : 'Morlok',
		'wounds' : 13,
		'agility' : 31,
		'toughness' : 35,
		'armour' : 3,
		'armascc' : 39
	},
	{
		'name' : 'Kratos',
		'wounds' : 13,
		'agility' : 31,
		'toughness' : 35,
		'armour' : 3,
		'armascc' : 39
	}
]

weapons = [

	{'name' : 'sierra', 
		'damage': '1D10+2', 
		'properties' : 	{ 'DESGARRADORA' : True, 'EQUILIBRADA' : True  , 'MEJORCALIDAD' : True } 
	},
	{'name' : 'espadaEnergia', 
		'damage': '1D10+5', 
		'properties' : { 'EQUILIBRADA' : True  } 
	}
]

def simulaCombate(pj1, pj2):
	# De momento un simple intercambio de golpes rebajando la hasta llegar a 0...

	# Definimos la iniciativa.
	# HAY QUE CONTROLAR EL EMPATE !!! 

	combate = [pj1, pj2]

	# darkheresy.initiativeRoll(combate)
	nohayOrdenDefinido = True

	initiative1 = pj1.initiative()
	initiative2 = pj2.initiative()

	# TODO MEJORAR ESTO...#
 	while( nohayOrdenDefinido ):

		# print initiative1, initiative2
	
		if (initiative1 > initiative2):
			first =  pj1
			last =  pj2
			nohayOrdenDefinido = False

		elif (initiative1 < initiative2):
			first = pj2
			last = pj1
			nohayOrdenDefinido = False
		else:
			# Miramos las bonificaciones de bonifAgilidad.
			first,last = sorted(combate, key=lambda x: x.bonifAgilidad)
			if (first.bonifAgilidad() != last.bonifAgilidad()):
				nohayOrdenDefinido = False
		initiative1 = pj1.initiative()
		initiative2 = pj2.initiative()
	
	narracion = []
	narracion.append("Combat start: %s  VS %s" % (first.name, last.name))
	
	rounds = 0
	while( first.isAlive() and last.isAlive() and rounds < 100):
		
		narracion.append("Turno: %d" % rounds)
		# Ataque 
		location, damage = first.attack()

		if location:

			narracion.append('{0} ha conseguido impactar a {1}'.format(first.name,last.name))
			# Parada
			parry = last.parry()
			# Si no hay parada llega el danio
			if not parry:

				sufferedDamage = last.sufferDamage(location, damage)

				if (sufferedDamage > 0):
					narracion.append('   El ataque ha causado {0} puntos a {1}'.format(sufferedDamage, last.name))
				else:
					narracion.append('   El ataque no ha causado daños')
			else:
				narracion.append('   Pero {0} ha conseguido parar el ataque'.format(last.name))
		else:
			narracion.append('{0} ha fallado el ataque'.format(first.name))	
		
		# Si el 1 sigue en pie seguimos...
		if (last.isAlive() > 0):
			
			# Ataque
			location, damage = last.attack()  
			
			if location:

				narracion.append('{0} ha conseguido impactar a {1}'.format(last.name,first.name))
				# Parada
				parry = last.parry()

				# Si no hay parada llega el danio
				if not parry:

					sufferedDamage = first.sufferDamage(location, damage)

					if (sufferedDamage > 0):
						narracion.append('   El ataque ha causado {0} puntos a {1}'.format(sufferedDamage, first.name))
					else:
						narracion.append('   El ataque no ha causado daños')
				else:
					narracion.append('   Pero {0} ha conseguido parar el ataque'.format(first.name))
			else:
				narracion.append('{0} ha fallado el ataque'.format(last.name))	

		rounds = rounds + 1
	
	if DEBUG:
		print "\n".join(narracion)

	ganador = sorted([first,last], key=lambda k: k.wounds)[1].name
	# print 'Fin del combate: GANADOR', ganador

	return ganador



def simulaArmas():

	print "TOTAL PRUEBAS: ",  NUMREPETICIONES

	result = {}
	for armaItem in testArmas:
		arma = Weapon(armaItem['name'], armaItem)
		tiradas = []
		for i in range(NUMREPETICIONES):
			if darkheresy.attackRoll(arma):
				tiradas.append(darkheresy.weaponRollDamage(arma))
			else:
				tiradas.append(0)
		a = array(tiradas)
		print ""
		print arma.name," ataques acertados: ", len(a[nonzero(a)])
		print "Ataque min/max : " , a.min() , "/", a.max()
		print "Ataque medio (sin ataques nulos) / total: " , round(a[nonzero(a)].mean(),2), "/" , a.mean() 
		print "Ataque desviacion : ", round(a.std(),3)
		result[arma.name] = tiradas
		if DEBUG:
			print tiradas
	print result 

def main():
	tiradas = []

	weapon0 = Weapon(weapons[0]['name'], weapons[0])
	weapon1 = Weapon(weapons[1]['name'], weapons[1])

	for i in range(NUMREPETICIONES):

		pj0 = Character(pjs[0]['name'], weapon0, pjs[0])
		pj1 = Character(pjs[1]['name'], weapon1, pjs[1])

		tiradas.append(simulaCombate(pj0, pj1))

	print "Combates ganados por : %s -> %d" % (pj0.name, tiradas.count(pj0.name))
	print "Combates ganados por : %s -> %d" % (pj1.name, tiradas.count(pj1.name))

if  __name__ =='__main__':
	main()
	#simulaArmas()