import re
from collections import deque
from itertools import permutations

def readProgram():
	with open("input.txt", "r") as f:
		instructions = [int(x) for x in re.split('[^0-9\-]+', f.read())]
		return instructions
		
def decomposeInstruction(instruction):
	opCode = instruction % 100
	paramModes = ((instruction // 100) % 10, (instruction // 1000) % 10, (instruction // 10000) % 10)
	return (opCode, paramModes)

def getParamValue(instructions, paramPos, paramMode):
	if paramMode == 0: # address
		return instructions[paramPos]
	elif paramMode == 1: # immediate
		return paramPos

def runProgram(instructions, userInput = None, outputBuffer = None, noun = None, verb = None):
	
	if noun != None:
		instructions[1] = noun
	if verb != None:
		instructions[2] = verb

	programCounter = 0
	while programCounter < len(instructions):
		opCode, paramModes = decomposeInstruction(instructions[programCounter])
		if opCode == 99:
			break
		else:
			# maybe 0 is not the most appropriate value in this case - ideally a "nullable" object would be better to store these values to detect using a non-existant parameter
			leftValPos =  instructions[programCounter + 1] if programCounter + 1 < len(instructions) else 0
			rightValPos = instructions[programCounter + 2] if programCounter + 2 < len(instructions) else 0
			outputPos = instructions[programCounter + 3] if programCounter + 3 < len(instructions) else 0
			
			if opCode == 1: # add
				instructions[outputPos] = getParamValue(instructions, leftValPos, paramModes[0]) + getParamValue(instructions, rightValPos, paramModes[1])
				programCounter += 4
			elif opCode == 2: # multiply
				instructions[outputPos] = getParamValue(instructions, leftValPos, paramModes[0]) * getParamValue(instructions, rightValPos, paramModes[1])
				programCounter += 4
			elif opCode == 3: # input (read int)
				instructions[leftValPos] = userInput.popleft()
				programCounter += 2
			elif opCode == 4: # output (print)
				if outputBuffer != None:
					outputBuffer.append(getParamValue(instructions, leftValPos, paramModes[0]))
				programCounter += 2
			elif opCode == 5: # jump if true
				if getParamValue(instructions, leftValPos, paramModes[0]) != 0:
					programCounter = getParamValue(instructions, rightValPos, paramModes[1])
				else:
					programCounter += 3
			elif opCode == 6: # jump if false
				if getParamValue(instructions, leftValPos, paramModes[0]) == 0:
					programCounter = getParamValue(instructions, rightValPos, paramModes[1])
				else:
					programCounter += 3
			elif opCode == 7: # less than
				if getParamValue(instructions, leftValPos, paramModes[0]) < getParamValue(instructions, rightValPos, paramModes[1]):
					instructions[outputPos] = 1
				else:
					instructions[outputPos] = 0
				programCounter += 4
			elif opCode == 8: # equality
				if getParamValue(instructions, leftValPos, paramModes[0]) == getParamValue(instructions, rightValPos, paramModes[1]):
					instructions[outputPos] = 1 
				else:
					instructions[outputPos] = 0
				programCounter += 4
			else:
				raise Exception("Unknown opcode " + str(opCode) + " at position " + str(programCounter))

	return instructions

instructions = readProgram()

maxSignal = None
maxSignalPhaseSettings = None
for phaseSettingCombo in permutations([0, 1, 2, 3, 4], 5):
	inputSignal = 0
	for phaseSetting in phaseSettingCombo:
		outputBuffer = deque()
		runProgram(instructions[:], deque([phaseSetting, inputSignal]), outputBuffer)
		inputSignal = outputBuffer.popleft()
		
	if maxSignal == None or inputSignal > maxSignal:
		maxSignal = inputSignal
		maxSignalPhaseSettings = phaseSettingCombo
		
print(str(maxSignal))
	
