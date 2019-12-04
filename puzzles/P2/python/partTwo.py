import re

def readProgram():
	with open("input.txt", "r") as f:
		instructions = [int(x) for x in re.split('[^0-9]+', f.read())]
		return instructions
		
def runProgram(instructions, noun, verb):
	instructions[1] = noun
	instructions[2] = verb

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

for noun in range(0, 100):
	for verb in range(0, 100):
		if runProgram(instructions[:], noun, verb)[0] == 19690720:
			print("Noun is " + str(noun) + ", verb is " + str(verb) + ", 100 * noun + verb is " + str(100 * noun + verb))
			break
