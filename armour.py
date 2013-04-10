
from armorPiece import ArmorPiece
import darkheresy
class Armour:

	def __init__(self, pieces=[]):
		self.pieces = pieces


	def protectionByLoc(self, localization):
		n = int(localization)

		locName = darkheresy.location(n)

		# print locName, localization
		# Now we search for locName in
		# armor pieces.
		matches = [x for x in self.pieces if locName in x.localizations]
		if matches:
			totalProperties = []
			for item in matches:
				for property in item.properties:
					totalProperties.append(property) 

		# If two pieces covers the same loc only the highest protecion
		# is returned.
			return max([x.armourBonus() for x in matches]), totalProperties
		else:
			return 0, {}

	""" 
		If any piece of armour is bad quality
		a -10 is return
	"""
	def agilityBonus(self):
		bonificador = 0
		for item in self.pieces:
			if item.MALACALIDAD:
				bonificador = -10 
		return bonificador
		
if __name__ == '__main__':

	piece1 = ArmorPiece("cuero de pandillero", "primitivo", 1, 6, "arms,chest,legs", [ 'PRIMITIVA' ])
	piece2 = ArmorPiece("pieles de animales",  "primitivo", 2, 10, "chest", [ 'PRIMITIVA' ])
	piece3 = ArmorPiece("armadura de placas feudal", "primitivo", 5, 22, "head,arms,chest,legs", [ 'PRIMITIVA' ])

	armour = Armour([piece1, piece2, piece3])

	print armour.protectionByLoc('7')

	