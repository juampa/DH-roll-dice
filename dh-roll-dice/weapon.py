# coding=UTF-8
class Weapon:

	"""
	name : nombre del arma
	damage: danio del arma (incluye bonificacion por fuerza.
	penetration : >= 0
	properties: cualidades extra del arma.

	"""
	def __init__(self, name, damage, penetration=0, properties=[]):
		
		self.name = name
		self.damage = damage
		self.penetration = penetration
		self.properties = properties

	""" 
		return true / false if the weapon has the property.
	"""
	def __getattr__(self, name):
		return name in self.properties

	def parryBonus(self):
		bonificador = 0 
		
		if self.EQUILIBRADA:
			bonificador += 10

		if self.DESEQUILIBRADA:
			bonificador -= 10
		
		if self.DEFENSIVA:
			bonificador += 15
		
		return bonificador

	def attackBonus(self):

		bonificador = 0 ;

		if self.MEJORCALIDAD:
			bonificador += 10
		if self.DEFENSIVA:
			bonificador -= 10

		return bonificador

	def distanceBonus(distance):

		alcance = self.ALCANCE 

		if alcance:
			if distance <= 3:
				# Corto
				return 30

			if distance < (alcance / 2):
				# Corto
				return 10
			if distance > (alcance * 2) and distance < (alcance * 3):
				# Largo alcance
				return -10
			if distance > (alcance * 3) and distance < (alcance * 4):
				# Extremo alcance
				return -30
			if distance > (alcance * 4):
				# Maximo alcance (fallo automatico)
				return -100

		return 0 

	def damageBonus(self):

		bonificador = 0 
		if self.MEJORCALIDAD:
			bonificador += 1
		return bonificador

	def __str__(self):
		return "%s %s" % (self.name, self.damage)

if __name__ == '__main__':

	try:
		w = {
			'name' : 'espadaEnergia', 
			'damage': '1D10+5', 
			'properties' : [ 'EQUILIBRADA' ] 
			}

		weapon = Weapon(w['name'], '1D10+2', 0,  w['properties'])


		print weapon.name, weapon.parryBonus(), weapon.attackBonus()
	except Exception as exception:
		print exception