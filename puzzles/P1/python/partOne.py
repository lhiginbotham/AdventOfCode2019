from math import floor

with open("input.txt", "r") as inputFile:
	fuel_req_sum = 0
	for line in inputFile:
		fuel_req_sum += floor(int(line.strip()) / 3.0) - 2
	print(fuel_req_sum)