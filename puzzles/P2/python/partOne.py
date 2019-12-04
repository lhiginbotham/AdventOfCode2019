import re

def readProgram():
	with open("input.txt", "r") as f:
		instructions = [int(x) for x in re.split('[^0-9]+', f.read())]
		return instructions
		
def runProgram(instructions):
	programCounter = 0
	while programCounter < len(instructions):
		currentInstruction = instructions[programCounter]
		if currentInstruction == 99:
			break
		else:
			leftValPos = instructions[programCounter + 1]
			rightValPos = instructions[programCounter + 2]
			outputPos = instructions[programCounter + 3]
			if currentInstruction == 1:
				instructions[outputPos] = instructions[leftValPos] + instructions[rightValPos]
			elif currentInstruction == 2:
				instructions[outputPos] = instructions[leftValPos] * instructions[rightValPos]
			else:
				print("Unknown opcode " + str(currentInstruction) + " at position " + str(programCounter))
				break	
		programCounter += 4
	return instructions

instructions = readProgram()

# as per part one's instructions, first modify the program state
instructions[1] = 12
instructions[2] = 2

finalState = runProgram(instructions[:])

print("Value at position 0: " + str(finalState[0]))