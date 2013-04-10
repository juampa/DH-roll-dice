# coding=UTF-8

from weapon import Weapon
from armour import Armour
from armorPiece import ArmorPiece
import darkheresy
import logging

class Character:

	def __init__(self, name, weapon, armour, properties={}):
		self.name = name
		self.weapon = weapon
		self.armour = armour
		self.properties = properties

	def __getattr__(self, name):
	
		if name in self.properties:
			return self.properties[name]
		else:
			raise AttributeError("I dont have the property %s" % name)

	def attack(self):
		diceRoll = darkheresy.attackRoll(self)
		# Si hemos impactado ya calculamos el danio.
		if diceRoll:
			damage =  darkheresy.weaponDamage(self)

			# sumamos la bonificacion de fuerza del personaje
			damage += (self.strength / 10)
			
			# Devolvemos localizacion (el reverse de la tirada) y daño
			if diceRoll >= 10:
				location = str(diceRoll)[::-1]
			else:
				location = ('0' + str(diceRoll))[::-1]

			locationName = darkheresy.location(int(location))
			
			logging.debug("%s impacta en %s y puede causar %d puntos de daño " % (self.name, locationName, damage))

			return location, damage
		else:
			logging.debug("%s falla el ataque" % (self.name))
			return None,None

	def parry(self):
		
		bonificador = self.weapon.parryBonus()
		
		if darkheresy.D100() <= (self.armascc + bonificador):
			logging.debug('%s para el ataque' % self.name)
			return True
		else:
			logging.debug('%s no consigue parar el ataque' % self.name)
			return False
	

	def initiative( self ):
		return darkheresy.D10() + (self.agility/10)	

	def sufferDamage(self, localization, damage, enemyWeapon=None):

		# Si el arma enemiga es penetrante hay que restar ese 
		# valor de la armadura.
		armour, props = self.armour.protectionByLoc(localization) 

		if enemyWeapon is not None:
			if enemyWeapon.PRIMITIVA and not 'PRIMITIVA' in props:
				armour *= 2
			if  'PRIMITIVA' in props and not enemyWeapon.PRIMITIVA:
				armour /= 2
			armour -= enemyWeapon.penetration 

		armour = 0 if armour < 0 else armour

		increase_armour = armour + (self.toughness/10)
		# Descontamos armadura y bonificacion por resistencia.
		# TODO Mirar la localizacion.
		sufferedDamage = damage - increase_armour

		if sufferedDamage > 0:
			self.wounds = self.wounds - sufferedDamage
			logging.debug("%s sufre %d puntos tras absorver %d" % (self.name, sufferedDamage, increase_armour))
			logging.debug("%s su salud es ahora %d" % (self.name, self.wounds))
		else:
			logging.debug("%s ha absorvido todo el daño del ataque" % self.name)
		

		return sufferedDamage

	def isDead(self):
		return self.wounds < 0

	def isAlive(self):
		return not self.isDead()

	def bonifAgilidad(self):
		return (self.agility - self.armour.agilityBonus()) / 10

if __name__ == '__main__':

	pj = {
		'name' : 'Kratos',
		'wounds' : 13,
		'agility' : 31,
		'toughness' : 35,
		'strength' : 31,
		'armascc' : 50
		}

	w = {
			'name' : 'espadaEnergia', 
			'damage': '1D10+5', 
			'properties' : [ 'EQUILIBRADA' ] 
			}

	wp = Weapon(w['name'], '1D10+2', 0,  w['properties'])


	piece1 = ArmorPiece("cuero de pandillero", "primitivo", 1, 6, "arms,chest,legs")
	piece2 = ArmorPiece("pieles de animales",  "primitivo", 2, 10, "chest")
	piece3 = ArmorPiece("armadura de placas feudal", "primitivo", 5, 22, "head,arms,chest,legs")

	armour = Armour([piece1, piece2, piece3])
		
		
	a = Character(pj['name'], wp, armour,  pj)

	print a.weapon

	