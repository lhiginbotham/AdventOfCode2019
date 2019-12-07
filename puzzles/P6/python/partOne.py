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
		
print(countLinks(readOrbitalMap()));