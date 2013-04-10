# coding=UTF-8
import logging
from random import randrange
from weapon import Weapon
from character import Character
from armorPiece import ArmorPiece
from armour import Armour
import darkheresy


pjs = [
	{
		'wounds' : 13,
		'agility' : 31,
		'toughness' : 35,
		'strength' : 30,
		'armascc' : 39
	},
	{
		'wounds' : 13,
		'agility' : 31,
		'toughness' : 35,
		'strength' : 30,
		'armascc' : 39
	}
]

def main(repeticiones=1):

	#Logging config.
	level = logging.DEBUG if repeticiones == 1 else logging.INFO
	logging.basicConfig(format='%(levelname)s: %(message)s', level=level)

	tiradas = []

	piece1 = ArmorPiece("caparazonArbites", "caparazon", 5, 15, "arms,chest,legs")
	piece2 = ArmorPiece("pieles de animales",  "primitivo", 2, 10, "arms,chest,legs", [ 'PRIMITIVA' ])

	armour1 = Armour([piece1])
	armour2 = Armour([piece2])
	
	weapon0 = Weapon('sierra', '1D10+2', 2, [ 'DESGARRADORA', 'EQUILIBRADA' ] )
	weapon1 = Weapon('espadaEnergia', '1D10+5', 6, [ 'EQUILIBRADA' ] )

	for i in range(repeticiones):

		pj0 = Character('Morlok', weapon0, armour1, pjs[0])
		pj1 = Character('Kratos', weapon1, armour2, pjs[1])

		tiradas.append(darkheresy.simulaCombate(pj0, pj1))

	print "Combates ganados por : %s -> %d" % (pj0.name, tiradas.count(pj0.name))
	print "Combates ganados por : %s -> %d" % (pj1.name, tiradas.count(pj1.name))

if  __name__ =='__main__':
	main(5000)
