from collections import deque
from itertools import permutations

class ProgramProcess():
	PROCESS_STATUS_READY = 0
	PROCESS_STATUS_TERMINATED = 1
	PROCESS_STATUS_WAITING_FOR_IO = 2

	def __init__(self, state, inputBuffer, outputBuffer):
		self.state = state
		self.status = ProgramProcess.PROCESS_STATUS_READY
		self.inputBuffer = inputBuffer
		self.outputBuffer = outputBuffer
		self.programCounter = 0
		self.halt = None

class ProgramHalt():
	# halt types
	HALT_TERMINATED = 0
	HALT_SYSCALL = 1
	
	# syscalls
	SYSCALL_INPUT = 0 # haltParams[1] will be the place to write the input in the state
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
	opCode = instruction % 100
	paramModes = ((instruction // 100) % 10, (instruction // 1000) % 10, (instruction // 10000) % 10)
	return (opCode, paramModes)

def getParamValue(instructions, paramPos, paramMode):
	if paramMode == 0: # address
		return instructions[paramPos]
	elif paramMode == 1: # immediate
		return paramPos
		
def processSyscall(programHalt):
	method = programHalt.haltParams[0]
	if method == ProgramHalt.SYSCALL_INPUT:
		if len(proc.inputBuffer) > 0:
			writeAddress = programHalt.haltParams[1]
			programHalt.proc.state[writeAddress] = proc.inputBuffer.popleft()
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
#		proc.state[1] = noun
#	if verb != None:
#		proc.state[2] = verb

	while proc.programCounter < len(proc.state):
		opCode, paramModes = decomposeInstruction(proc.state[proc.programCounter])
		if opCode == 99:
			break
		else:
			# maybe 0 is not the most appropriate value in this case - ideally a "nullable" object would be better to store these values to detect using a non-existant parameter
			leftValPos =  proc.state[proc.programCounter + 1] if proc.programCounter + 1 < len(proc.state) else 0
			rightValPos = proc.state[proc.programCounter + 2] if proc.programCounter + 2 < len(proc.state) else 0
			outputPos = proc.state[proc.programCounter + 3] if proc.programCounter + 3 < len(proc.state) else 0
			
			if opCode == 1: # add
				proc.state[outputPos] = getParamValue(proc.state, leftValPos, paramModes[0]) + getParamValue(proc.state, rightValPos, paramModes[1])
				proc.programCounter += 4
			elif opCode == 2: # multiply
				proc.state[outputPos] = getParamValue(proc.state, leftValPos, paramModes[0]) * getParamValue(proc.state, rightValPos, paramModes[1])
				proc.programCounter += 4
			elif opCode == 3: # input (read int)
				proc.programCounter += 2
				proc.halt = ProgramHalt(proc, ProgramHalt.HALT_SYSCALL, [ProgramHalt.SYSCALL_INPUT, leftValPos])
				return proc.halt
			elif opCode == 4: # output (print)
				proc.programCounter += 2
				proc.halt = ProgramHalt(proc, ProgramHalt.HALT_SYSCALL, [ProgramHalt.SYSCALL_OUTPUT, getParamValue(proc.state, leftValPos, paramModes[0])])
				return proc.halt
			elif opCode == 5: # jump if true
				if getParamValue(proc.state, leftValPos, paramModes[0]) != 0:
					proc.programCounter = getParamValue(proc.state, rightValPos, paramModes[1])
				else:
					proc.programCounter += 3
			elif opCode == 6: # jump if false
				if getParamValue(proc.state, leftValPos, paramModes[0]) == 0:
					proc.programCounter = getParamValue(proc.state, rightValPos, paramModes[1])
				else:
					proc.programCounter += 3
			elif opCode == 7: # less than
				if getParamValue(proc.state, leftValPos, paramModes[0]) < getParamValue(proc.state, rightValPos, paramModes[1]):
					proc.state[outputPos] = 1
				else:
					proc.state[outputPos] = 0
				proc.programCounter += 4
			elif opCode == 8: # equality
				if getParamValue(proc.state, leftValPos, paramModes[0]) == getParamValue(proc.state, rightValPos, paramModes[1]):
					proc.state[outputPos] = 1 
				else:
					proc.state[outputPos] = 0
				proc.programCounter += 4
			else:
				raise Exception("Unknown opcode " + str(opCode) + " at position " + str(proc.programCounter))

	proc.halt = ProgramHalt(proc, ProgramHalt.HALT_TERMINATED, [])
	return proc.halt

instructions = readProgram()

maxSignal = None
maxSignalPhaseSettings = None
for phaseSettingCombo in permutations(range(5, 10), 5):
	processes = []
	for phaseSetting in phaseSettingCombo:
		inputBuffer = None
		if len(processes) != 0:
			inputBuffer = processes[-1].outputBuffer
			inputBuffer.appendleft(phaseSetting)
		processes.append(ProgramProcess(instructions[:], inputBuffer, deque()))
		
	# connect first and last process
	processes[0].inputBuffer = processes[-1].outputBuffer
	# put initial phase setting and initial signal into the first amplifier
	processes[0].inputBuffer.append(phaseSettingCombo[0])
	processes[0].inputBuffer.append(0)
	
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
		
	inputSignal = processes[-1].outputBuffer.pop()	
	if maxSignal == None or inputSignal > maxSignal:
		maxSignal = inputSignal
		maxSignalPhaseSettings = phaseSettingCombo
		
print(str(maxSignal))
	
