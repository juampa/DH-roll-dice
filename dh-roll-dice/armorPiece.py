class ArmorPiece:

	def __init__(self, name, category, protection, weight, localizations, properties=[]):
		self.name = name
		self.category = category
		self.protection = protection
		self.weight = weight
		self.localizations = localizations.split(",")
		self.properties = properties

	def __getattr__(self, name):
		return name in self.properties

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

	def __str__(self):
		return "%s %s %d" % (self.name, self.category, self.protection)

	def __repr__(self):
		return self.__str__()
		