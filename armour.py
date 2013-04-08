
from armorPiece import ArmorPiece

class Armour:

	def __init__(self, pieces=[]):
		self.pieces = pieces


	def protectionByLoc(self, localization):
		n = int(localization)

		locName = 'DESCONOCIDO'
		if n > 0 and n < 11:
			locName = 'head'
		elif n > 10 and n < 21:
			locName = 'arms'
		elif n > 20 and n < 31:
			locName = 'arms'
		elif n > 30 and n < 71:
			locName = 'chest'
		elif n > 70 and n < 86:
			locName = 'legs'
		elif n > 85 and n < 101:
			locName = 'legs'

		# print locName, localization
		# Now we search for locName in
		# armor pieces.
		matches = [x for x in self.pieces if locName in x.localizations]
		
		if matches:
			totalProperties = {}
			for item in matches:
				totalProperties.update(item.properties)

		# If two pieces covers the same loc only the highest protecion
		# is returned.
			return max([x.armourBonus() for x in matches]), totalProperties
		else:
			return 0, {}

		
if __name__ == '__main__':

	piece1 = ArmorPiece("cuero de pandillero", "primitivo", 1, 6, "arms,chest,legs", { 'PRIMITIVA' : True})
	piece2 = ArmorPiece("pieles de animales",  "primitivo", 2, 10, "chest", { 'PRIMITIVA' : True})
	piece3 = ArmorPiece("armadura de placas feudal", "primitivo", 5, 22, "head,arms,chest,legs", { 'PRIMITIVA' : True})

	armour = Armour([piece1, piece2, piece3])

	print armour.protectionByLoc(7)

	