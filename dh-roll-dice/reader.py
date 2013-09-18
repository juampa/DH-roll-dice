import yaml
import sys
import logging

from weapon import Weapon
from armour import Armour
from armorPiece import ArmorPiece
from character import Character


def weaponParser(w):
	return Weapon(w['name'], w['damage'], w['penetration'],  w['properties'])

def armorParser(yamlarmourPieces):
	pieces = []
	for piece in yamlarmourPieces:
		pieces.append(
			ArmorPiece(piece['name'], piece['category'], piece['protection'], piece['weight'], piece['locations']))

	return Armour(pieces)

def characterParser(yamlcharacter):

	return Character(yamlcharacter['name'], None, None, yamlcharacter )

def parseFile(file):

	try:
		characterYaml = yaml.load(file)['character']

		if characterYaml:
			# Weapon parser
			weapon = weaponParser(characterYaml['weapon'])

			# Armor
			armor = armorParser(characterYaml['armor'])
	
			# Character
			character = characterParser(characterYaml['personal'])

			character.armour = armor
			character.weapon = weapon

			return character
		else:
			logging.error("Error en el fichero yaml")
			return None

	except Exception, e:
		logging.error(e)
		raise e
	