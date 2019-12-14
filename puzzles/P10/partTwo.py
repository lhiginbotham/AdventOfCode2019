#
#		Note: first off, this code is garbage
#		second off, this code is not correct.
#		Tried the 200th vaporized asteroid, did not work
#		instead, put in the 201st asteroid, and it magically worked
#		Only half-works with the large example, not sure what is wrong in this mess...
#


# '.' = empty, '#' = asteroid
# window coordinate system - top-left is 0,0, increase as you go down-right
# asteroids are exactly in the center of the marked position.  if asteroid is in (0,0) on the map, they are truly in (0.5, 0.5)

import math

def readMap():
	with open("input.txt", "r") as f:
		asteroids = []
		yPos = 0
		for line in f:
			xPos = 0
			for pos in line:
				if pos == '#':
					asteroids.append((xPos, yPos))
				xPos += 1
			yPos += 1
		return asteroids
		
asteroids = readMap()

bestAsteroid = None
bestCount = None
bestMap = None
bestSlopes = None

for idx in range(len(asteroids)):
	slopeSet = set()
	slopeMap = dict() # key : slope info, value : set of coordinates that are along that ray
	curAsteroid = asteroids[idx]
	hasUp = False
	hasDown = False
	hasLeft = False
	hasRight = False
	for idxOther in range(len(asteroids)):
		if idx == idxOther:
			pass
		curOtherAsteroid = asteroids[idxOther]
		rise = (curOtherAsteroid[1] - curAsteroid[1])
		run = (curOtherAsteroid[0] - curAsteroid[0])
		
		slopeInfo = None
		if run == 0 and rise >= 0:
			slopeInfo = (float('Inf'), rise > 0, run > 0)
		elif run == 0 and rise < 0:
			slopeInfo = (float('-Inf'), rise > 0, run > 0)
		elif rise == 0 and run >= 0:
			slopeInfo = (float('0'), rise > 0, run > 0)
		elif rise == 0 and run < 0:
			slopeInfo = (float('0'), rise > 0, run > 0)
		else:
			slopeInfo = (rise / run, rise > 0, run > 0)

		slopeSet.add(slopeInfo)
		if slopeInfo not in slopeMap:
			slopeMap[slopeInfo] = []
		slopeMap[slopeInfo].append(curOtherAsteroid)

	count = len(slopeSet)
	if hasUp:
		count += 1
	if hasDown:
		count += 1
	if hasLeft:
		count += 1
	if hasRight:
		count += 1
	if bestAsteroid == None or bestCount < count:
		bestAsteroid = curAsteroid
		bestCount = count
		bestSlopes = slopeSet
		bestMap = slopeMap

def reconstructVectorFromSlopeInfo(slopeInfo):
	slopeMagnitude = abs(slopeInfo[0])
	risePositive = slopeInfo[1]
	runPositive = slopeInfo[2]
	
	if slopeMagnitude == float('Inf'):
		if slopeInfo[0] == float('Inf'):
			return (0, 1)
		else:
			return (0, -1)
	
	vector = (1, slopeMagnitude)
	if risePositive and runPositive:
		pass
	if risePositive and not runPositive:
		vector = (-1 * vector[0], vector[1])
	if not risePositive and runPositive:
		vector = (vector[0], -1 * vector[1])
	if not risePositive and not runPositive:
		vector = (-1 * vector[0], -1 * vector[1])
	return vector


# now we have the best asteroid's "slope map"
# need to sort slopes based on counter-clockwise rotation and also sort each collection of coordinates
# in order to find the proper order in which a laser will vaporize
angularSortedSlopes = [] # tuple of angle, 
for slopeInfo in bestSlopes:
	vec = reconstructVectorFromSlopeInfo(slopeInfo)
	angle = (math.acos(-vec[1] / (1 * math.sqrt(vec[0]**2 + vec[1]**2)))) # formula implies vector (0, -1) as the start
	if vec[0] < 0:
		angle = 2 * 3.14159265 - angle
		
	asteroidsForSlope = bestMap[slopeInfo]
	asteroidsForSlope = sorted(asteroidsForSlope, key=lambda asteroid: math.sqrt((asteroid[0] - bestAsteroid[0])**2 + (asteroid[1] - bestAsteroid[1])**2))
	bestMap[slopeInfo] = asteroidsForSlope
	
	angularSortedSlopes.append((angle, slopeInfo))
	
angularSortedSlopes.sort(key=lambda x: x[0])

vaporizedCount = 0
vaporizedThisRotation = True
while vaporizedThisRotation and vaporizedCount < 200:
	vaporizedThisRotation = False

	for angleAndSlopeSet in angularSortedSlopes:
		if len(bestMap[angleAndSlopeSet[1]]):

			vaporized = bestMap[angleAndSlopeSet[1]].pop(0)
			vaporizedCount += 1
			if vaporizedCount in [1, 2, 3, 10, 20, 50, 100, 199, 200, 201, 299]:
				print(str(vaporizedCount) + "th: " + str(vaporized))
			vaporizedThisRotation = True
