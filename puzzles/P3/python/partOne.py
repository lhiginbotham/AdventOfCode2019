from itertools import combinations

collinearCounts  = True

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		
	def strRep(self):
		return "(" + str(self.x) + ", " + str(self.y) + ")"

# in this grid, can only be horizontal or vertical line
class WireSegment:
	def __init__(self, start, end):
		self.start = start
		self.end = end
		self.orientation = ("h" if self.start.y == self.end.y else "y")
		
	def sortPointsX(self):
		if self.start.x <= self.end.x:
			return (self.start, self.end)
		return (self.end, self.start)

	def sortPointsY(self):
		if self.start.y <= self.end.y:
			return (self.start, self.end)
		return (self.end, self.start)
	
	def strRep(self):
		return self.start.strRep() + " to " + self.end.strRep() 
	
	# will return more than one point if collinear
	def intersectionPoints(self, otherWireSegment):
		global collinearCounts
		
		xSortSelf = self.sortPointsX()
		ySortSelf = self.sortPointsY()
		xSortOther = otherWireSegment.sortPointsX()
		ySortOther = otherWireSegment.sortPointsY()
	
		if self.orientation == "h":
			if otherWireSegment.orientation == "h":
				if ySortOther[0].y != ySortSelf[0].y:
					# not collinear
					return []
				else:
					# collinear
					if collinearCounts:
						xPosSelf = range(xSortSelf[0].x, xSortSelf[1].x + 1)
						xPosOther = range(xSortOther[0].x, xSortOther[1].x + 1)
						xIntersection = [x for x in xPosSelf if x in xPosOther]
						return [Point(x, ySortSelf[0].y) for x in xIntersection if not(x == 0 and ySortSelf[0].y == 0)]
					return []
			else:
				# possibly one point of intersection
				intersectPoint = Point(xSortOther[0].x, xSortSelf[0].y)
				if intersectPoint.x in range(xSortSelf[0].x, xSortSelf[1].x + 1) and intersectPoint.y in range(ySortOther[0].y, ySortOther[1].y + 1):
					if intersectPoint.x == 0 and intersectPoint.y == 0:
						return [] # SPECIAL CASE: origin does not count!
					return [intersectPoint]
				else:
					return []
				
		else:
			if otherWireSegment.orientation == "v":
				if ySortOther[0].y != ySortSelf[0].y:
					# not collinear
					return []
				else:
					# collinear
					if collinearCounts:
						yPosSelf = range(ySortSelf[0].y, ySortSelf[1].y + 1)
						yPosOther = range(ySortOther[0].y, ySortOther[1].y + 1)
						yIntersection = [y for y in yPosSelf if y in yPosOther]
						return [Point(xSortSelf[0].x, y) for y in yIntersection if not(xSortSelf[0].x == 0 and y == 0)]
					return []
			else:
				# possibly one point of intersection
				intersectPoint = Point(xSortSelf[0].x, xSortOther[0].y)
				if intersectPoint.x in range(xSortOther[0].x, xSortOther[1].x + 1) and intersectPoint.y in range(ySortSelf[0].y, ySortSelf[1].y + 1):
					if intersectPoint.x == 0 and intersectPoint.y == 0:
						return [] # SPECIAL CASE: origin does not count!
					return [intersectPoint]
				else:
					return []
			
		
class Wire:
	def __init__(self, segments):
		self.segments = segments
		
	def intersectionPoints(self, otherWire):
		intersectionPoints = []
		for segment in self.segments:
			for otherSegment in otherWire.segments:
				intersectionPoints.extend(segment.intersectionPoints(otherSegment))
		return intersectionPoints
	

def readWires():
	wires = []
	with open("input.txt", "r") as f:
		for line in f:
			measurements = line.split(",")
			segments = []
			cur = Point(0, 0)
			last = Point(0, 0)
			for instruction in measurements:
				dir = instruction[0]
				val = int(instruction[1:])
				if dir == "R":
					cur.x += val
				elif dir == "L":
					cur.x -= val
				elif dir == "U":
					cur.y += val
				elif dir == "D":
					cur.y -= val
				else:
					raise Exception("Direction " + dir + " not recognized.")
				segments.append(WireSegment(Point(last.x, last.y), Point(cur.x, cur.y))) # if I did WireSegment(last, cur), would last and cur pass by reference or by value?
				last.x = cur.x # more uncertainty regarding ref vs val in Python (last = cur, valid or not?)
				last.y = cur.y
			wires.append(Wire(segments))
	return wires

def getIntersectionPointsOfWires(wires):
	intersectionPoints = []
	for wireCombo in combinations(wires, 2):
		intersectionPoints.extend(wireCombo[0].intersectionPoints(wireCombo[1]))
	return intersectionPoints
	
def manhattanDistance(pointOne, pointTwo):
	return abs(pointOne.x - pointTwo.x) + abs(pointOne.y - pointTwo.y)
	
def getClosestPointDistance(origin, pointCloud):
	if len(pointCloud) > 0:
		bestDistance = manhattanDistance(origin, pointCloud[0])
		for idx in range(1, len(pointCloud)):
			bestDistance = min(bestDistance, manhattanDistance(origin, pointCloud[idx]))
			if bestDistance == 66:
				print("(" + str(pointCloud[idx].x) + ", " + str(pointCloud[idx].y) + ")")
		return bestDistance
	else:
		return 0
	

print(getClosestPointDistance(Point(0, 0), getIntersectionPointsOfWires(readWires())))

