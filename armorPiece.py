class ArmorPiece:

	def __init__(self, name, type, protection, weight, localizations, properties={}):
		self.name = name
		self.type = type
		self.protection = protection
		self.weight = weight
		self.localizations = localizations.split(",")
		self.properties = properties

	def __getattr__(self, name):
		if name in self.properties:
			return self.properties[name]
		else:
			return None #raise AttributeError("I dont have the property %s" % name)
		#return None
			# raise AttributeError('this weapon dont have the property %s' % name)

	def armourBonus(self):
		bonificador = self.protection
		# Esto hay que hacerlo solo en el primer turno
		# No se como representarlo...

		if self.BUENACALIDAD:
			bonificador += 1
		if self.MEJORCALIDAD:
			bonificador += 1
		return bonificador

	def agilityBonus(self):
		bonificador = 0
		if self.MALACALIDAD:
			bonificador -= 10 
		return bonificador


if __name__ == '__main__':
	
	piece = ArmorPiece("cuero de pandillero", "primitivo", 1, 6, "brazos,cuerpo,piernas")

	print piece.armourBonus(), piece.localizations