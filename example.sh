#!/usr/bin/python
import math
from numpy import array
from numpy import nonzero
from random import randrange
import darkheresy

ARMAS_CC = 39
NUMREPETICIONES = 10
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
		'agility' : 31
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
		'agility' : 39
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
	initiative_sorted_pjs = sorted([pj1,pj2], key=lambda k: darkheresy.initiativeRoll(k)) 

	first = initiative_sorted_pjs[0]
	last = initiative_sorted_pjs[1]

	# print first.keys()
	# print last.keys()

	print "Combat start", first['wounds'] , last['wounds']

	rounds = 0
	while( first['wounds'] > 0 and last['wounds'] > 0 and rounds < 100):
		
		print "Turno: ", rounds
		# Ataque 
		atack = darkheresy.attackRoll(first['weapon'])

		if atack:

			print '{0} ha conseguido impactar a {1}'.format(first['name'],last['name'])
			# Parada
			parry = darkheresy.parryRoll(last['weapon'])
			# Si no hay parada llega el danio
			if not parry:
				damage = darkheresy.damageRoll(first['weapon'])
				last['wounds'] = last['wounds'] - damage
				print 'El ataque ha causado {0} puntos a {1} y su salud baja a {2}'.format(damage, last['name'], last['wounds'])
			else:
				print '   Pero {0} ha conseguido parar el ataque'.format(last['name'])
		else:
			print '{0} ha fallado el ataque'.format(first['name'])	
		# Si el 1 sigue en pie seguimos...
		if (last['wounds'] > 0):
			# Ataque 
			atack = darkheresy.attackRoll(last['weapon'])

			if atack:

				print '{0} ha conseguido impactar a {1}'.format(last['name'],first['name'])

				# Parada
				parry = darkheresy.parryRoll(first['weapon'])
				# Si no hay parada llega el danio
				if not parry:
					damage = darkheresy.damageRoll(last['weapon'])
					first['wounds'] = first['wounds'] - damage
					print 'El ataque ha causado {0} puntos a {1} y su salud baja a {2}'.format(damage, first['name'], first['wounds'])
				else:
					print '   Pero {0} ha conseguido parar el ataque'.format(first['name'])
			else:
				print '{0} ha fallado el ataque'.format(last['name'])

		rounds = rounds + 1
	
	print 'Fin del combate: GANADOR', sorted(initiative_sorted_pjs, key=lambda k: k['wounds'])[1]['name']




def main():

	print "TOTAL PRUEBAS: ",  NUMREPETICIONES

	result = {}
	for arma in testArmas:
		tiradas = []
		for i in range(NUMREPETICIONES):
			if darkheresy.atackRoll(arma):
				tiradas.append(darkheresy.damageRoll(arma))
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

if  __name__ =='__main__':
	simulaCombate(pjs[0], pjs[1])