# coding=UTF-8
class Weapon:

	"""
	name : nombre del arma
	damage: danio del arma (incluye bonificacion por fuerza.
	penetration : >= 0
	properties: cualidades extra del arma.

	"""
	def __init__(self, name, damage, penetration, properties=[]):
		
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

	def damageBonus(self):

		bonificador = 0 
		if self.MEJORCALIDAD:
			bonificador += 1
		return bonificador


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