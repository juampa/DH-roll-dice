# coding=UTF-8
from armorPiece import ArmorPiece
import darkheresy
import logging
class Armour:

	@classmethod
	def describelocation(cls, n=45):

		# pongo el 45 pq especifica que los ataques
		# q no digan nada van al pecho.

		locName = 'UNKNOWN'
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
		return locName

	def __init__(self, pieces=[]):
		self.pieces = pieces


	def protectionByLoc(self, localization):
		
		location_number = int(localization)

		logging.debug("Location_number is %d " % (location_number))

		locName = Armour.describelocation(location_number)

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
	
	def __str__(self):
		return "Armadura: %s" % (self.pieces)

	def __repr__(self):
		return self.__str__()


	