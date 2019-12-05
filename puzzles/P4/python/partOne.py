import math

inputLow = 136818
inputHigh = 685979

# can do this using recursion and dynamic programming (i.e. caching) for better performance!!
neverDecreasingDigitCache = dict()
def neverDecreasingDigitRec():
	pass

def neverDecreasingDigit(num):
	num = int(num) # type safety - not required in a puzzle
	prev = 9
	while num > 0:
		cur = num % 10
		if cur > prev:
			return False
		prev = cur
		num = num // 10 # integer division, truncate
	return True

def getOrderOfMagnitude(num):
	return int(math.log10(num))

def getDigit(num, idxFromRight):
	return (num % (10 ** (idxFromRight + 1))) // (10 ** (idxFromRight))
	
def hasDoubledDigit(num):
	magnitude = getOrderOfMagnitude(num)
	for idx in range(0, magnitude):
		if getDigit(num, idx) == getDigit(num, idx + 1):
			return True
	return False

print(len([x for x in range(inputLow, inputHigh + 1) if neverDecreasingDigit(x) and hasDoubledDigit(x)]))
	