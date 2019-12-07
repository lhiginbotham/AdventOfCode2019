class Node:
	def __init__(self, name):
		self.name = name
		self.parent = None
		self.children = set()
		self.distanceFromRoot = -1
		
	def addChild(self, child):
		if child != None:
			self.children.add(child)
			
	def assignParent(self, parent):
		self.parent = parent
		
	def getDistanceFromRoot(self):
		if self.parent == None:
			# this is the root!
			return 0
		elif self.distanceFromRoot == -1:
			# calculate it recursively
			self.distanceFromRoot = 1 + self.parent.getDistanceFromRoot()
		
		return self.distanceFromRoot
		
	def getAncestorList(self):
		ancestors = []
		par = self.parent
		distance = 0
		while par != None:
			ancestors.append((par.name, distance))
			par = par.parent
			distance += 1
		print(ancestors)
		return ancestors
			

def readOrbitalMap():
	with open("input.txt", "r") as f:
		massNameToNode = dict()
		for line in f:
			entities = line.strip().split(")")
			for idx in range(0, len(entities) - 1):
				parent = entities[idx]
				child = entities[idx + 1]
				parNode = massNameToNode.get(parent, None)
				childNode = massNameToNode.get(child, None)
				if parNode == None:
					parNode = Node(parent)
					massNameToNode[parent] = parNode
				if childNode == None:
					childNode = Node(child)
					massNameToNode[child] = childNode
				parNode.addChild(childNode)
				childNode.assignParent(parNode)
		return massNameToNode
		
def countLinks(massNameToNode):
	links = 0
	for key in massNameToNode:
		mass = massNameToNode[key]
		links += mass.getDistanceFromRoot()
	return links
	
def binarySearch(collection, key):
	idx = bisect_left(collection, key)
	if idx != len(collection) and collection[idx] == key:
		return idx
	else:
		return -1

def FIND_SANTA(massNameToNode): # !!! !!!WE ARE COMING, SANTA!!! !!!
	me = massNameToNode['YOU']
	Santa = massNameToNode['SAN']
	
	myPlanetOrbitList = me.getAncestorList()
	myPlanetOrbitMap = {key: value for (key, value) in myPlanetOrbitList}
	SantasPlanetOrbitList = Santa.getAncestorList()
	SantasPlanetOrbitMap = {key: value for (key, value) in SantasPlanetOrbitList}
	
	myPlanetSet = set([x[0] for x in myPlanetOrbitList])
	SantasPlanetSet = set([x[0] for x in SantasPlanetOrbitList])
	commonSet = myPlanetSet.intersection(SantasPlanetSet)
	
	lowestDistancePlanet = None
	distance = 0
	for x in commonSet:
		if lowestDistancePlanet == None:
			lowestDistancePlanet = x
			distance = myPlanetOrbitMap[x] + SantasPlanetOrbitMap[x]
			continue
		
		candidateDistance = myPlanetOrbitMap[x] + SantasPlanetOrbitMap[x]
		if candidateDistance < distance:
			lowestDistancePlanet = x
			distance = candidateDistance
			
	print(lowestDistancePlanet)
	return distance
	
print(FIND_SANTA(readOrbitalMap()))