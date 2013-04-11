# coding=UTF-8
import logging
from copy import deepcopy
from random import randrange
from weapon import Weapon
from character import Character
from armorPiece import ArmorPiece
from armour import Armour
import darkheresy
import reader


def main(file1, file2, repeticiones=1):

	#Logging config.
	level = logging.DEBUG if repeticiones == 1 else logging.INFO
	logging.basicConfig(format='%(levelname)s: %(message)s', level=level)

	resultado = []

	pj0 = reader.parseFile(file1)
	pj1 = reader.parseFile(file2)

	for i in range(repeticiones):

		resultado.append(darkheresy.simulaCombate(pj0, pj1))
		pj0.reset()
		pj1.reset()

	for name in (pj0.name, pj1.name):
		logging.info( "Combates ganados por : %s -> %d" % ( name , resultado.count(name)))
	

if  __name__ =='__main__':

	file1 = 'examples/character1.yaml'
	file2 = 'examples/character2.yaml'

	main(file1, file2, 1000)
