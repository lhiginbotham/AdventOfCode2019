# '.' = empty, '#' = asteroid
# window coordinate system - top-left is 0,0, increase as you go down-right
# asteroids are exactly in the center of the marked position.  if asteroid is in (0,0) on the map, they are truly in (0.5, 0.5)

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
m = dict()
for idx in range(len(asteroids)):
	slopeSet = set()
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
		if curAsteroid == (1,2):
			print("other = %s, rise = %d, run = %d" % (str(curOtherAsteroid), rise, run)) 
		if run == 0 and rise >= 0:
			hasUp = True
		elif run == 0 and rise < 0:
			hasDown = True
		elif rise == 0 and run >= 0:
			hasRight = True
		elif rise == 0 and run < 0:
			hasLeft = True
		else:
			slopeSet.add((rise / run, rise > 0, run > 0))

	if (curAsteroid == (1,2)):
		print(slopeSet)
	m[idx] = slopeSet
	count = len(slopeSet)
	if hasUp:
		if (curAsteroid == (1,2)):
			print("has up")
		count += 1
	if hasDown:
		if (curAsteroid == (1,2)):
			print("has down")
		count += 1
	if hasLeft:
		if (curAsteroid == (1,2)):
			print("has left")
		count += 1
	if hasRight:
		if (curAsteroid == (1,2)):
			print("has right")
		count += 1
	if bestAsteroid == None or bestCount < count:
		bestAsteroid = curAsteroid
		bestCount = count
		
print(bestAsteroid)
print(bestCount)