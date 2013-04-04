# coding=UTF-8
class Weapon:

	def __init__(self, name, properties={}):
		
		self.name = name
		self.properties = properties

	def __getattr__(self, name):
		if name in self.properties:
			return self.properties[name]
		else:
			if name in self.properties['properties']:
				return self.properties['properties'][name]
		return None
			# raise AttributeError('this weapon dont have the property %s' % name)

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
			'name' : 'sierra', 
			'caracteristica' : 39, 
			'damage': '1D10+2', 
			'properties' : 	{ 'DESGARRADORA' : True, 'EQUILIBRADA' : True  , 'MEJORCALIDAD' : True } 
			}

		weapon = Weapon(w['name'], w)

		print weapon.name, weapon.parryBonus(), weapon.attackBonus()
	except Exception as exception:
		print exception