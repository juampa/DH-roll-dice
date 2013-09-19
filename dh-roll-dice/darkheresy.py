# coding=UTF-8
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



def defineInitiative(pj1, pj2) :

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
			first, last = sorted(combate, key=lambda x: x.bonifAgilidad)
			if (first.bonifAgilidad() != last.bonifAgilidad()):
				nohayOrdenDefinido = False
		initiative1 = pj1.initiative()
		initiative2 = pj2.initiative()

	return first, last



def simulaRangeCombat(pj1, pj2, props={}):
	
	# Definimos la iniciativa.
	first, last = defineInitiative(pj1, pj2)
	
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
		if last.isAlive():
			
			# Ataque
			location, damage = last.attack()  
			
			if location and not first.parry():

				sufferedDamage = first.sufferDamage(location, damage, last.weapon)
	
		rounds = rounds + 1
	
	ganador = sorted([first,last], key=lambda k: k.actualWounds)[1].name
	# print 'Fin del combate: GANADOR', ganador

	return ganador
