# coding=UTF-8
from weapon import Weapon
import random
import re
import logging

random.seed()

EXPAND = True

# ROLL DICE FUNCTIONS
def D100():
	return (random.randrange(100) + 1)

def D10():
	return (random.randrange(10) + 1)

def D5():
	return (random.randrange(5) + 1)

def parse_input(in_string):
    """
    Extract roll parameters from a string.

    Returns a tuple (r, k, mod) where
      r:    number of dice to roll
      k:    type of dice to roll
      mod:  static bonus/penalty to roll
    """
    regex = re.compile(r'''
        (\d+)D(\d+)             # dice to roll and type
        (\s*[+-]\s*\d+)?        # optional modifier
        \s*$                    # and nothing else
        ''', re.VERBOSE)

    m = regex.match(in_string)
    if not m:
        return

    p = m.groups()

    r, k = int(p[0]), int(p[1])
    mod = 0 if not p[2] else int(p[2])

    return r, k, mod

def rawRollDamage( func, character ):
	tirada = func()
	if (tirada == 10) and EXPAND:
		extra = 0
		while(attackRoll( character )):
			tirada = func()
			extra = extra + tirada
			if (tirada != 10):
				break
		tirada = tirada + extra
	return tirada


def weaponDamage(character):

	r,k,bonificador = parse_input(character.weapon.damage)

	func = None
	if k == 10:
		func = D10
	if k == 5:
		func = D5

	rolls = []
	for i in range(r):
		rolls.append(rawRollDamage(func, character))

	
	# Si el weapon es desgarradora tiro un dado mas
	if character.weapon.DESGARRADORA:
		rolls.append(rawRollDamage(func, character))
	
	# Algunas armas tienen bonificadores al danio.
	bonificador += character.weapon.damageBonus()
	
	# Ordenamos de mayor a menor		
	rolls.sort(reverse=True)

	# Nos quedamos con las r primeras y las sumamos...
	return sum(rolls[:r]) + bonificador

def location(n=45):

	# pongo el 45 pq especifica que los ataques
	# q no digan nada van al pecho.

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
	return locName

def attackRoll( character ):
	
	# En funcion del arma 
	bonificador = character.weapon.attackBonus()
	
	result = D100() 

	return result if (result <= (character.armascc + bonificador)) else None

def simulaCombate(pj1, pj2):
	# De momento un simple intercambio de golpes rebajando la hasta llegar a 0...

	# Definimos la iniciativa.
	combate = [pj1, pj2]

	# darkheresy.initiativeRoll(combate)
	nohayOrdenDefinido = True

	initiative1 = pj1.initiative()
	initiative2 = pj2.initiative()

	# TODO MEJORAR ESTO...#
 	while( nohayOrdenDefinido ):

		# print initiative1, initiative2
	
		if (initiative1 > initiative2):
			first =  pj1
			last =  pj2
			nohayOrdenDefinido = False

		elif (initiative1 < initiative2):
			first = pj2
			last = pj1
			nohayOrdenDefinido = False
		else:
			# Miramos las bonificaciones de bonifAgilidad.
			first,last = sorted(combate, key=lambda x: x.bonifAgilidad)
			if (first.bonifAgilidad() != last.bonifAgilidad()):
				nohayOrdenDefinido = False
		initiative1 = pj1.initiative()
		initiative2 = pj2.initiative()
	
	logging.debug("Combat start: %s  VS %s" % (first.name, last.name))
	
	#print "Combat start: %s  VS %s" % (first.name, last.name)
	rounds = 0
	while( first.isAlive() and last.isAlive() and rounds < 100):
		
		logging.debug("Turno: %d" % rounds)
		# Ataque 
		location, damage = first.attack()

		# si hay localizacion y last no para hay un ataque exitoso.
		if location and not last.parry():
			last.sufferDamage(location, damage, first.weapon)
		
		# Si el 1 sigue en pie seguimos...
		if (last.isAlive() > 0):
			
			# Ataque
			location, damage = last.attack()  
			
			if location and not first.parry():

				sufferedDamage = first.sufferDamage(location, damage, last.weapon)
	
		rounds = rounds + 1
	
	ganador = sorted([first,last], key=lambda k: k.wounds)[1].name
	# print 'Fin del combate: GANADOR', ganador

	return ganador



if __name__ == "__main__":
	pattern = '3D10-5'
	print pattern, "->", parse_input(pattern)