# coding=UTF-8

from weapon import Weapon

class Character:

	def __init__(self, name, weapon, properties={}):
		self.name = name
		self.weapon = weapon
		self.properties = properties

	def __getattr__(self, name):

		print "pregunto por :" , name
		if name in self.properties:
			return self.properties[name]
		else:
			raise AttributeError('I dont have the property %s' % name)



if __name__ == '__main__':
	try:

		pj = {
		'name' : 'Kratos',
		'wounds' : 13,
		'agility' : 31,
		'toughness' : 35,
		'armour' : 3
		}

		weapon = {
					'name' : 'sierra', 
					'caracteristica' : 39, 
					'damage': '1D10+2', 
					'properties' : 	{ 'DESGARRADORA' : True, 'EQUILIBRADA' : True  , 'MEJORCALIDAD' : True } 
				}

		w = Weapon('sierra', weapon)	

		a = Character(pj['name'], w,  pj)

		print a.name, a.weapon.damage

	except Exception as exception:
		print exception