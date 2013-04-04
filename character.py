# coding=UTF-8

from weapon import Weapon
import darkheresy

class Character:

	def __init__(self, name, weapon, properties={}):
		self.name = name
		self.weapon = weapon
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

			# Devolvemos localizacion (el reverse de la tirada) y daño
			print diceRoll
			return str(diceRoll)[::-1], damage
		else:
			return None

	def parry(self):
		bonificador = 0 ;
		if self.weapon.EQUILIBRADA:
			bonificador = bonificador + 10
		return darkheresy.D100() <= (self.armascc + bonificador)
	

	def initiative( self ):
		return darkheresy.D10() + (self.agility/10)	

	def sufferDamage(self, localization, damage):

		# Descontamos armadura y bonificacion por resistencia.
		# TODO Mirar la localizacion.
		damage = damage - self.armour
		damage = damage - (self.toughness/10)

		self.wounds = self.wounds - damage

		return damage

	def isDead(self):
		return self.wounds > 0

	def isAlive(self):
		return not self.isDead()

	def bonifAgilidad(self):
		return self.agility / 10

if __name__ == '__main__':
	try:

		pj = {
		'name' : 'Kratos',
		'wounds' : 13,
		'agility' : 31,
		'toughness' : 35,
		'armour' : 3,
		'armascc' : 50
		}

		weapon = {
					'name' : 'sierra', 
					'damage': '1D10+2', 
					'properties' : 	{ 'DESGARRADORA' : True, 'EQUILIBRADA' : True  , 'MEJORCALIDAD' : True } 
				}

		w = Weapon('sierra', weapon)	

		a = Character(pj['name'], w,  pj)


		print a.name, a.weapon.damage
		print a.attack()

		a.isAlive()
	except Exception as exception:
		print exception