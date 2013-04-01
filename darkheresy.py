
import random
import re

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

def rawRollDamage( func, weapon ):
	tirada = func()
	if (tirada == 10) and EXPAND:
		extra = 0
		while(atackRoll(weapon)):
			tirada = func()
			extra = extra + tirada
			if (tirada != 10):
				break
		tirada = tirada + extra
	return tirada


def damage(weapon):

	r,k,bonificador = parse_input(weapon['damage'])

	func = None
	if k == 10:
		func = D10
	if k == 5:
		func = D5

	rolls = []
	for i in range(r):
		rolls.append(rawRollDamage(func, weapon))

	# Si el weapon es desgarradora tiro un dado mas
	if 'properties' in weapon:
		if 'DESGARRADORA' in weapon['properties']:
			rolls.append(rawRollDamage(func, weapon))
		if 'MEJORCALIDAD' in weapon['properties']:
			bonificador = bonificador + 1
	# Ordenamos de mayor a menor		
	rolls.sort(reverse=True)

	# Nos quedamos con las r primeras y las sumamos...
	return sum(rolls[:r]) + bonificador


def atackRoll( weapon ):
	bonificador = 0 ;
	if 'properties' in weapon:
		if 'MEJORCALIDAD' in weapon['properties']:
			bonificador = bonificador + 10
		if 'DEFENSIVA' in weapon['properties']:
			bonificador = bonificador - 10
	return D100() <= (weapon['caracteristica'] + bonificador)



if __name__ == "__main__":
	pattern = '3D10-5'
	print pattern, "->", parse_input(pattern)