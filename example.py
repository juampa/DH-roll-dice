# coding=UTF-8

import math
from numpy import array
from numpy import nonzero
from random import randrange
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
		'weapon' : 
				{	
					'name' : 'espadaEnergia', 
					'caracteristica' : 39, 
					'damage': '1D10+5', 
					'properties' : { 'EQUILIBRADA' : True  }
				},
		'wounds' : 13,
		'agility' : 39,
		'toughness' : 35,
		'armour' : 4
	},
	{
		'name' : 'Kratos',
		'weapon' : 
				{
					'name' : 'sierra', 
					'caracteristica' : 39, 
					'damage': '1D10+2', 
					'properties' : 	{ 'DESGARRADORA' : True, 'EQUILIBRADA' : True  , 'MEJORCALIDAD' : True } 
				},
		'wounds' : 13,
		'agility' : 31,
		'toughness' : 35,
		'armour' : 3
	}
]

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

def simulaCombate(pj1, pj2):
	# De momento un simple intercambio de golpes rebajando la hasta llegar a 0...

	# Definimos la iniciativa.
	# HAY QUE CONTROLAR EL EMPATE !!! 

	combate = [pj1, pj2]

	darkheresy.initiativeRolls(combate)


	initiative1 = darkheresy.initiativeRoll(pj1)
	initiative2 = darkheresy.initiativeRoll(pj2) 
	
	if (initiative1 > initiative2):
		first = copy.deepcopy(pj1)
		last = copy.deepcopy(pj2)
	else:
		first = copy.deepcopy(pj2)
		last = copy.deepcopy(pj1)

	
	narracion = []
	narracion.append("Combat start: %s  VS %s" % (first['name'] , last['name']))
	
	rounds = 0
	while( first['wounds'] > 0 and last['wounds'] > 0 and rounds < 100):
		
		narracion.append("Turno: %d" % rounds)
		# Ataque 
		atack = darkheresy.attackRoll(first['weapon'])

		if atack:

			narracion.append('{0} ha conseguido impactar a {1}'.format(first['name'],last['name']))
			# Parada
			parry = darkheresy.parryRoll(last['weapon'])
			# Si no hay parada llega el danio
			if not parry:
				damage = darkheresy.damageRoll(first, last)
				last['wounds'] = last['wounds'] - damage
				if (damage > 0):
					narracion.append('   El ataque ha causado {0} puntos a {1} y su salud baja a {2}'.format(damage, last['name'], last['wounds']))
				else:
					narracion.append('   El ataque no ha causado daños')
			else:
				narracion.append('   Pero {0} ha conseguido parar el ataque'.format(last['name']))
		else:
			narracion.append('{0} ha fallado el ataque'.format(first['name']))	
		# Si el 1 sigue en pie seguimos...
		if (last['wounds'] > 0):
			# Ataque 
			atack = darkheresy.attackRoll(last['weapon'])

			if atack:

				narracion.append('{0} ha conseguido impactar a {1}'.format(last['name'],first['name']))

				# Parada
				parry = darkheresy.parryRoll(first['weapon'])
				# Si no hay parada llega el danio
				if not parry:
					damage = darkheresy.damageRoll(last,first)
					first['wounds'] = first['wounds'] - damage
					if (damage > 0):
						narracion.append('   El ataque ha causado {0} puntos a {1} y su salud baja a {2}'.format(damage, first['name'], first['wounds']))
					else:
						narracion.append('   El ataque no ha causado daños')
				else:
					narracion.append('   Pero {0} ha conseguido parar el ataque'.format(first['name']))
			else:
				narracion.append('{0} ha fallado el ataque'.format(last['name']))

		rounds = rounds + 1
	
	if DEBUG:
		print "\n".join(narracion)

	ganador = sorted([first,last], key=lambda k: k['wounds'])[1]['name']
	# print 'Fin del combate: GANADOR', ganador

	return ganador



def simulaArmas():

	print "TOTAL PRUEBAS: ",  NUMREPETICIONES

	result = {}
	for arma in testArmas:
		tiradas = []
		for i in range(NUMREPETICIONES):
			if darkheresy.atackRoll(arma):
				tiradas.append(darkheresy.weaponRollDamage(arma))
			else:
				tiradas.append(0)
		a = array(tiradas)
		print ""
		print arma['name']," ataques acertados: ", len(a[nonzero(a)])
		print "Ataque min/max : " , a.min() , "/", a.max()
		print "Ataque medio (sin ataques nulos) / total: " , round(a[nonzero(a)].mean(),2), "/" , a.mean() 
		print "Ataque desviacion : ", round(a.std(),3)
		result[arma['name']] = tiradas
		if DEBUG:
			print tiradas
	print result 

def main():
	tiradas = []
	for i in range(NUMREPETICIONES):
		tiradas.append(simulaCombate(pjs[0], pjs[1]))

	print "Combates ganados por : %s -> %d" % (pjs[0]['name'], tiradas.count(pjs[0]['name']))
	print "Combates ganados por : %s -> %d" % (pjs[1]['name'], tiradas.count(pjs[1]['name']))

if  __name__ =='__main__':
	main()