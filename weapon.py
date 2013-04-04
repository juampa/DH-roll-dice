# coding=UTF-8
class Weapon:

	def __init__(self, name, properties={}):
		
		self.name = name
		self.properties = properties

	def __getattr__(self, name):
		if name in self.properties:
			return self.properties[name]
		else:
			return None
			# raise AttributeError('this weapon dont have the property %s' % name)

if __name__ == '__main__':

	try:
		w = {
			'name' : 'sierra', 
			'caracteristica' : 39, 
			'damage': '1D10+2', 
			'properties' : 	{ 'DESGARRADORA' : True, 'EQUILIBRADA' : True  , 'MEJORCALIDAD' : True } 
			}

		weapon = Weapon(w['name'], w)

		print weapon.name, weapon.damage
	except Exception as exception:
		print exception