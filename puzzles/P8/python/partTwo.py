WIDTH = 25
HEIGHT = 6

IMG = []
for x in range(HEIGHT):
	IMG.append(["'"]*WIDTH)

def codeToChar(x):
	if x == "0":
		return "."
	elif x == "1":
		return "@"
	else:
		return "'"

class Layer:
	def __init__(self, imageStr):
		Layer.applyLayerToImg(imageStr)
		
	def applyLayerToImg(str):
		global IMG, WIDTH
		pos = 0
		for x in str:
			heightIdx = pos // WIDTH 
			widthIdx = pos % WIDTH
			existingPixel = IMG[heightIdx][widthIdx]
			if existingPixel == "'":
				IMG[heightIdx][widthIdx] = codeToChar(x)
			pos += 1
		
def readImage(width, height):
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
			pos += (width * height)
	
def writeImage():
	global IMG
	with open("output.txt", "w") as f: 
		for row in IMG:
			for pixel in row:
				f.write(pixel)
			f.write("\n")
		f.flush()			
			
			
readImage(WIDTH, HEIGHT)
writeImage()
