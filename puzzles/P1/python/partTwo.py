from math import floor

def moduleToFuel(moduleSize):
	return floor(moduleSize / 3.0) - 2
	
def recursiveCalcTotalFuel(initialFuel):
	if initialFuel <= 0:
		return 0
	return initialFuel + recursiveCalcTotalFuel(max(floor(initialFuel / 3.0) - 2, 0))

with open("input.txt", "r") as inputFile:
	fuel_req_sum = 0
	for line in inputFile:
		moduleMass = int(line.strip())
		fuel_req_sum += recursiveCalcTotalFuel(moduleToFuel(moduleMass))
	print(fuel_req_sum)