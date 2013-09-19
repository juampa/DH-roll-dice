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
		self.actualWounds = properties['wounds']

	def __getattr__(self, name):
	
		if name in self.properties:
			return self.properties[name]
		else:
			raise AttributeError("I dont have the property %s" % name)


	def initiative(self):
		return darkheresy.D10() + (self.agility/10)	


	def attack(self):
		diceRoll = self.attackRoll()
		# Si hemos impactado ya calculamos el danio.
		if diceRoll:
			damage =  self.weaponDamage()

			# sumamos la bonificacion de fuerza del personaje
			damage += (self.strength / 10)
			
			# Devolvemos localizacion (el reverse de la tirada) y daño
			if diceRoll >= 10:
				location = str(diceRoll)[::-1]
			else:
				location = ('0' + str(diceRoll))[::-1]

			logging.debug("%s impacta en %s y puede causar %d puntos de daño " % (self.name, Armour.describelocation(int(location)), damage))

			return location, damage
		else:
			logging.debug("%s falla el ataque" % (self.name))
			return None,None

	def attackRoll( self, distance=-1 ):
	
		# En funcion del arma 
		bonificador = self.weapon.attackBonus()

		# Calculamos el bonificador por distancia
		# si es necesario.
		if distance >= 0:
			bonificador += self.weapon.distanceBonus(distance)
		result = darkheresy.D100() 
		return result if (result <= (self.ballisticskill + bonificador)) else None


	def parry(self):
		
		bonificador = self.weapon.parryBonus()
		
		if darkheresy.D100() <= (self.ballisticskill + bonificador):
			logging.debug('%s para el ataque' % self.name)
			return True
		else:
			logging.debug('%s no consigue parar el ataque' % self.name)
			return False
	

	def weaponDamage(self):

		r,k,bonificador = darkheresy.parse_input(self.weapon.damage)

		func = None
		if k == 10:
			func = darkheresy.D10
		if k == 5:
			func = darkheresy.D5

		rolls = []
		for i in range(r):
			rolls.append(self.rawRollDamage(func))

		# Si el weapon es desgarradora tiro un dado mas
		if self.weapon.DESGARRADORA:
			rolls.append(self.rawRollDamage(func))
		
		# Algunas armas tienen bonificadores al danio.
		bonificador += self.weapon.damageBonus()
		
		# Ordenamos de mayor a menor		
		rolls.sort(reverse=True)

		# Nos quedamos con las r primeras y las sumamos...
		return sum(rolls[:r]) + bonificador

	""" 
		"The Emperor is looking you" DHrule
	"""
	def rawRollDamage( self, func ):
		tirada = func()
		if (tirada == 10) and darkheresy.EXPAND:
			extra = 0
			while(self.attackRoll( )):
				tirada = func()
				extra = extra + tirada
				if (tirada != 10):
					break
			tirada = tirada + extra
		return tirada

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
		sufferedDamage = damage - increase_armour

		if sufferedDamage > 0:
			self.actualWounds -= sufferedDamage
			logging.debug("%s sufre %d puntos tras absorver %d" % (self.name, sufferedDamage, increase_armour))
			logging.debug("%s su salud es ahora %d" % (self.name, self.actualWounds))
		else:
			logging.debug("%s ha absorvido todo el daño del ataque" % self.name)
		

		return sufferedDamage

	def isDead(self):
		return self.actualWounds < 0

	def isAlive(self):
		return not self.isDead()

	def bonifAgilidad(self):
		return (self.agility - self.armour.agilityBonus()) / 10

	def reset(self):
		self.actualWounds = self.properties['wounds']

	def __str__(self):
		return "%s %s %s %s" % (self.name, self.wounds, self.armour, self.weapon)

	def __repr__(self):
		return self.__str__()


	