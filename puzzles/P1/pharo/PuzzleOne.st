'From Pharo7.0.4 of 13 August 2019 [Build information: Pharo-7.0.4+build.168.sha.ccd1f6489120f58ddeacb2cac77cd3a0f0dcfbe6 (64 Bit)] on 1 December 2019 at 12:30:09.788941 pm'!
Object subclass: #PuzzleOne
	instanceVariableNames: ''
	classVariableNames: ''
	poolDictionaries: ''
	category: 'AdventOfCode'!

!PuzzleOne methodsFor: 'accessing' stamp: 'LoganHiginbotham 12/1/2019 11:39'!
calculateFuelNeeded: aCollectionOfModules considerFuelMass: bIncludeFuelNeededForFuel
	"Takes a collection of modules and calculates the required fuel to ship it in Santa's transport vehicle.  Can include the amount of fuel required to carry the fuel itself."

	| totalFuelReq moduleFuelReq fuelFuelReq |
	totalFuelReq := 0.
	aCollectionOfModules
		do: [ :each | 
			moduleFuelReq := self calculateFuelNeededForMass: each.
			fuelFuelReq := bIncludeFuelNeededForFuel
				ifTrue: [ self recursiveFuelNeededForFuel: moduleFuelReq ]
				ifFalse: [ 0 ].
			totalFuelReq := totalFuelReq + moduleFuelReq + fuelFuelReq ].
	^ totalFuelReq.! !


!PuzzleOne methodsFor: 'as yet unclassified' stamp: 'LoganHiginbotham 12/1/2019 00:40'!
calculateFuelNeededForMass: aMass
	"Tranforms a numerical mass to the amount of fuel needed for Santa's transportation vehicle."

	^ 0 max: (((aMass / 3.0 ) floor) - 2).! !

!PuzzleOne methodsFor: 'as yet unclassified' stamp: 'LoganHiginbotham 12/1/2019 11:34'!
recursiveFuelNeededForFuel: aFuelAmount
	"Recursively calculates the fuel needed to carry a fuel (returned value is aFuelAmount + fuelRequiredToCarryIt"
		
	aFuelAmount <= 0
		ifTrue: [ ^ 0. ]
		ifFalse: [ ^aFuelAmount + (self recursiveFuelNeededForFuel: (self calculateFuelNeededForMass: aFuelAmount)) ].! !
