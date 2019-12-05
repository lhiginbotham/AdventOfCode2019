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
	
def hasExactlyDoubledDigit(num): # digit does not count if it is actually part of a larger group!
	magnitude = getOrderOfMagnitude(num)
	idx = 0
	while idx < magnitude:
		offset = 1 # idx + offset will point to the first digit that is not part of the group (offset is the group size)
		while offset + idx <= magnitude and getDigit(num, idx) == getDigit(num, idx + offset):
			offset += 1
		if offset == 2:
			return True
		idx += offset
	return False

print(len([x for x in range(inputLow, inputHigh + 1) if neverDecreasingDigit(x) and hasExactlyDoubledDigit(x)]))
