| pzOne aCollectionOfModules workingDir fuelForModules fuelForModulesAndFuel |
pzOne := PuzzleOne new.
workingDir := FileSystem disk workingDirectory.
aCollectionOfModules := OrderedCollection new.
(workingDir / 'input.txt') readStreamDo: 
	[:stream |
		[ stream atEnd ] whileFalse: [ 
			aCollectionOfModules add: stream nextLine asInteger.
		] 
	].

fuelForModules := pzOne calculateFuelNeeded: aCollectionOfModules considerFuelMass: false.
Transcript show: 'Answer for part one: ', (fuelForModules asString); cr.

fuelForModulesAndFuel := pzOne calculateFuelNeeded: aCollectionOfModules considerFuelMass: true.
Transcript show: 'Answer for part two: ', ((fuelForModulesAndFuel -  fuelForModules) asString); cr.
