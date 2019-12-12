WIDTH = 25
HEIGHT = 6

class Layer:
	def __init__(self, imageStr):
		self.digitCount = Layer.parseImgStrDigitCount(imageStr)
		self.imageStr = imageStr
		
	def parseImgStrDigitCount(str):
		digitCount = dict()
		for x in str:
			xNum = int(x)
			if xNum not in digitCount:
				digitCount[xNum] = 1
			else:
				digitCount[xNum] = digitCount[xNum] + 1
		return digitCount
		
def readImageGetLeastZeros(width, height):
	with open("input.txt", "r") as f:
		imageStr = f.read()
		size = len(imageStr)
		pos = 0
		layers = []
		leastZerosLayer = None
		leastZerosCount = None
		while pos < size:
			layer = Layer(imageStr[pos : pos + (width * height)])
			layers.append(layer)
			if (leastZerosLayer != None and layer.digitCount[0] < leastZerosCount) or leastZerosLayer == None:
				leastZerosLayer = layer
				leastZerosCount = layer.digitCount[0]
			pos = pos + (width * height)
		return leastZerosLayer
		
leastZerosLayer = readImageGetLeastZeros(WIDTH, HEIGHT)
print(leastZerosLayer.digitCount[1] * leastZerosLayer.digitCount[2])