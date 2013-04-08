# coding=UTF-8

from random import randrange
from weapon import Weapon
from character import Character
from armorPiece import ArmorPiece
from armour import Armour
import darkheresy


NUMREPETICIONES = 500
DEBUG = False



def simulaCombate(pj1, pj2):
	# De momento un simple intercambio de golpes rebajando la hasta llegar a 0...

	# Definimos la iniciativa.
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
	
	#print "Combat start: %s  VS %s" % (first.name, last.name)
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

				sufferedDamage = last.sufferDamage(location, damage, first.weapon)

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

					sufferedDamage = first.sufferDamage(location, damage, last.weapon)

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


pjs = [
	{
		'wounds' : 13,
		'agility' : 31,
		'toughness' : 35,
		'armascc' : 39
	},
	{
		'wounds' : 13,
		'agility' : 31,
		'toughness' : 35,
		'armascc' : 39
	}
]



def main():
	tiradas = []

	piece1 = ArmorPiece("caparazonArbites", "caparazon", 5, 15, "arms,chest,legs", [ ])
	piece2 = ArmorPiece("pieles de animales",  "primitivo", 2, 10, "arms,chest,legs", [ 'PRIMITIVA' ])

	armour1 = Armour([piece1])
	armour2 = Armour([piece2])
	
	weapon0 = Weapon('sierra', '1D10+2', 2, [ 'DESGARRADORA', 'EQUILIBRADA' ] )
	weapon1 = Weapon('espadaEnergia', '1D10+5', 6, [ 'EQUILIBRADA' ] )

	for i in range(NUMREPETICIONES):

		pj0 = Character('Morlok', weapon0, armour1, pjs[0])
		pj1 = Character('Kratos', weapon1, armour2, pjs[1])

		tiradas.append(simulaCombate(pj0, pj1))

	print "Combates ganados por : %s -> %d" % (pj0.name, tiradas.count(pj0.name))
	print "Combates ganados por : %s -> %d" % (pj1.name, tiradas.count(pj1.name))

if  __name__ =='__main__':
	main()
