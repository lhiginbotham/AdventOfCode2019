from collections import deque
from itertools import permutations

class ProgramProcess():
	PROCESS_STATUS_READY = 0
	PROCESS_STATUS_TERMINATED = 1
	PROCESS_STATUS_WAITING_FOR_IO = 2
	
	PAGE_SIZE = 512

	def populateMemMap(self, state):
		virtualMemoryMap = dict()
		numPagesNeeded = len(state) // ProgramProcess.PAGE_SIZE + 1
		for i in range(0, numPagesNeeded):
			virtualMemoryMap[i] = [0] * ProgramProcess.PAGE_SIZE
			page = virtualMemoryMap[i]
			for idx in range(0, ProgramProcess.PAGE_SIZE):
				offset = i * ProgramProcess.PAGE_SIZE + idx
				if offset >= len(state):
					break
				page[idx] = state[idx + i * ProgramProcess.PAGE_SIZE]
				
		return virtualMemoryMap


	def __init__(self, state, inputBuffer, outputBuffer):
		self.status = ProgramProcess.PROCESS_STATUS_READY
		self.inputBuffer = inputBuffer
		self.outputBuffer = outputBuffer
		self.programCounter = 0
		self.relativeBaseAddr = 0
		self.halt = None
		
		self.virtualMemoryMap = self.populateMemMap(state)
		
	
	def readMemory(self, location):
		idx = location // ProgramProcess.PAGE_SIZE
		memLoc = location % ProgramProcess.PAGE_SIZE
		if idx < 0:
			raise Exception("Negative memory address is illegal!  Terminating...")
			
		if idx not in self.virtualMemoryMap:
			self.virtualMemoryMap[idx] = [0] * ProgramProcess.PAGE_SIZE
		return self.virtualMemoryMap[idx][memLoc]
			
	def writeMemory(self, location, value):
		idx = location // ProgramProcess.PAGE_SIZE
		memLoc = location % ProgramProcess.PAGE_SIZE
		
		#print("Writing %d to idx = %d, loc = %d" % (value, idx, memLoc))
		
		if idx not in self.virtualMemoryMap:
			self.virtualMemoryMap[idx] = [0] * ProgramProcess.PAGE_SIZE
		self.virtualMemoryMap[idx][memLoc] = value

class ProgramHalt():
	# halt types
	HALT_TERMINATED = 0
	HALT_SYSCALL = 1
	
	# syscalls
	SYSCALL_INPUT = 0 # haltParams[1] will be the place to write the input in memory
	SYSCALL_OUTPUT = 1

	def __init__(self, proc, haltType, haltParams):
		self.proc = proc
		self.haltType = haltType
		self.haltParams = haltParams

def readProgram():
	with open("input.txt", "r") as f:
		instructions = [int(x) for x in f.read().split(',')]
		return instructions
		
def decomposeInstruction(instruction):
	#print("instr = " + str(instruction))
	opCode = instruction % 100
	paramModes = ((instruction // 100) % 10, (instruction // 1000) % 10, (instruction // 10000) % 10)
	#print((opCode, paramModes))
	if paramModes[2] == 1:
		raise Exception("Output param MUST not be an immediate, always an address or relative address!! Terminating...")
	return (opCode, paramModes)

def getParamValue(proc, paramPos, paramMode):
	if paramMode == 0: # address
		return proc.readMemory(paramPos)
	elif paramMode == 1: # immediate
		return paramPos
	elif paramMode == 2: # relative
		#print("getParamValue, relBase = %d, paramPos = %d" % (proc.relativeBaseAddr, paramPos))
		return proc.readMemory(proc.relativeBaseAddr + paramPos)
		
def getOutputPos(proc, outputParam, paramMode):
	if paramMode == 0:
		return outputParam
	elif paramMode == 2:
		return proc.relativeBaseAddr + outputParam
		
def processSyscall(programHalt):
	method = programHalt.haltParams[0]
	if method == ProgramHalt.SYSCALL_INPUT:
		if len(proc.inputBuffer) > 0:
			writeAddress = programHalt.haltParams[1]
			programHalt.proc.writeMemory(writeAddress, proc.inputBuffer.popleft())
		else:
			programHalt.proc.status = ProgramProcess.PROCESS_STATUS_WAITING_FOR_IO
	elif method == ProgramHalt.SYSCALL_OUTPUT:
		outputValue = programHalt.haltParams[1]
		programHalt.proc.outputBuffer.append(outputValue)
	else:
		raise Exception("Unknown syscall method: " + str(method))
		
def processHaltedProgram(programHalt):
	if programHalt.haltType == ProgramHalt.HALT_TERMINATED:
		programHalt.proc.status = ProgramProcess.PROCESS_STATUS_TERMINATED
		return True # done with process
	elif programHalt.haltType == ProgramHalt.HALT_SYSCALL:
		processSyscall(programHalt)
		return False # process needs rescheduled
	

def runProgram(proc):
#	I wonder if noun/verb concept will resurface, or if this was just a one time thing?
#	if noun != None:
#		proc.writeMemory(1, noun)
#	if verb != None:
#		proc.writeMemory(2, verb)

	while True:
		opCode, paramModes = decomposeInstruction(proc.readMemory(proc.programCounter))
		if opCode == 99:
			break
		else:
			# maybe 0 is not the most appropriate value in this case - ideally a "nullable" object would be better to store these values to detect using a non-existant parameter
			leftValPos =  proc.readMemory(proc.programCounter + 1)
			rightValPos = proc.readMemory(proc.programCounter + 2)
			outputPos = getOutputPos(proc, proc.readMemory(proc.programCounter + 3), paramModes[2])
			
			
			if opCode == 1: # add
				proc.writeMemory(outputPos, getParamValue(proc, leftValPos, paramModes[0]) + getParamValue(proc, rightValPos, paramModes[1]))
				proc.programCounter += 4
			elif opCode == 2: # multiply
				proc.writeMemory(outputPos, getParamValue(proc, leftValPos, paramModes[0]) * getParamValue(proc, rightValPos, paramModes[1]))
				proc.programCounter += 4
			elif opCode == 3: # input (read int)
				proc.programCounter += 2
				proc.halt = ProgramHalt(proc, ProgramHalt.HALT_SYSCALL, [ProgramHalt.SYSCALL_INPUT, getOutputPos(proc, leftValPos, paramModes[0])])
				return proc.halt
			elif opCode == 4: # output (print)
				proc.programCounter += 2
				proc.halt = ProgramHalt(proc, ProgramHalt.HALT_SYSCALL, [ProgramHalt.SYSCALL_OUTPUT, getParamValue(proc, leftValPos, paramModes[0])])
				return proc.halt
			elif opCode == 5: # jump if true
				if getParamValue(proc, leftValPos, paramModes[0]) != 0:
					proc.programCounter = getParamValue(proc, rightValPos, paramModes[1])
				else:
					proc.programCounter += 3
			elif opCode == 6: # jump if false
				if getParamValue(proc, leftValPos, paramModes[0]) == 0:
					proc.programCounter = getParamValue(proc, rightValPos, paramModes[1])
				else:
					proc.programCounter += 3
			elif opCode == 7: # less than
				if getParamValue(proc, leftValPos, paramModes[0]) < getParamValue(proc, rightValPos, paramModes[1]):
					proc.writeMemory(outputPos, 1)
				else:
					proc.writeMemory(outputPos, 0)
				proc.programCounter += 4
			elif opCode == 8: # equality
				if getParamValue(proc, leftValPos, paramModes[0]) == getParamValue(proc, rightValPos, paramModes[1]):
					proc.writeMemory(outputPos, 1)
				else:
					proc.writeMemory(outputPos, 0)
				proc.programCounter += 4
			elif opCode == 9:
				#print("base before = " + str(proc.relativeBaseAddr))
				proc.relativeBaseAddr += getParamValue(proc, leftValPos, paramModes[0])
				#print("base after = " + str(proc.relativeBaseAddr))
				proc.programCounter += 2
			else:
				raise Exception("Unknown opcode " + str(opCode) + " at position " + str(proc.programCounter))

	proc.halt = ProgramHalt(proc, ProgramHalt.HALT_TERMINATED, [])
	return proc.halt

instructions = readProgram()

processes = []
processes.append(ProgramProcess(instructions[:], deque(), deque()))

# provide proc with input
processes[0].inputBuffer.append(2)

nonTerminatedProcesses = processes
while len(nonTerminatedProcesses) > 0:
	tempNonTerminatedProcesses = []
	for proc in nonTerminatedProcesses:
		if proc.status == ProgramProcess.PROCESS_STATUS_WAITING_FOR_IO:
			proc.status = ProgramProcess.PROCESS_STATUS_READY
			processSyscall(proc.halt)
		
		if proc.status == ProgramProcess.PROCESS_STATUS_WAITING_FOR_IO:
			tempNonTerminatedProcesses.append(proc)
			continue
		elif proc.status == ProgramProcess.PROCESS_STATUS_TERMINATED:
			continue
			
		halt = runProgram(proc)
		if not processHaltedProgram(halt):
			# was just a syscall, not terminated
			tempNonTerminatedProcesses.append(proc)
			
	nonTerminatedProcesses = tempNonTerminatedProcesses

while len(processes[0].outputBuffer):
	print(str(processes[0].outputBuffer.popleft()))
