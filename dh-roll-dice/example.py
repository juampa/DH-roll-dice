# coding=UTF-8
import logging
import argparse
from random import randrange
from weapon import Weapon
from character import Character
from armorPiece import ArmorPiece
from armour import Armour
import darkheresy
import reader

def simula(file1, file2, repeticiones=1):

	#Logging config.
	level = logging.DEBUG if repeticiones == 1 else logging.INFO
	logging.basicConfig(format='%(levelname)s: %(message)s', level=level)

	resultado = []

	pj0 = reader.parseFile(file1)
	pj1 = reader.parseFile(file2)

	for i in range(repeticiones):

		resultado.append(darkheresy.simulaRangeCombat(pj0, pj1))
		pj0.reset()
		pj1.reset()

	for name in (pj0.name, pj1.name):
		logging.info( "Combates ganados por : %s -> %d" % ( name , resultado.count(name)))
	

if __name__ == "__main__":
    
	parser = argparse.ArgumentParser()

	parser.add_argument('player1', type=file)
	parser.add_argument('player2', type=file)
	parser.add_argument('reps', type=int)

	args = parser.parse_args()

	simula(args.player1, args.player2, args.reps)