/* REXX */
/*    D O M E S T I C   H O T   W A T E R   S A V I N G S   C A L C   */
clrscn
say 'Domestic Hot Water Savings Calculator'
say 'Written by Clifford A. Chipman, EMIT on'
say 'February 3, 2021'
say 'in z/OS REXX'
call setConstants
call CWTempDataEntry
call initFuelDataEntry
call initHWTempDataEntry
call initFlowRateDataEntry
call initShwrTimeDataEntry
call initCombEffDataEntry
call newFuelDataEntry
call newHWTempDataEntry
call newFlowRateDataEntry
call newShwrTimeDataEntry
call newCombEffDataEntry
/*                                                                    */
/* Calculate initial energy consumption & display report for user     */
/*                                                                    */
say 'Cold Water Inlet Temperature: 'CWTemp' degF'
say ' '
say 'Initial Hot Water Temperature: 'initHWTemp' degF'
say 'Initial Flow Rate: 'initFlowRate' GPM'
say 'Initial Shower Time: 'initShwrTime' minutes'
say 'Initial Combustion Efficiency: 'initCombEff'%'
initCombEff = initCombEff / 100
initUsage = initFlowRate * initShwrTime
say 'Initial Water Consumption: 'initUsage' gallons'
initEnergy = 8.33 * initUsage * (initHWTemp - CWTemp) / initCombEff
say 'Initial Energy Consumption: 'initEnergy' BTUs'
/*                                                                    */
/* Convert BTUs to fuel unit, calculate fuel consumption, & fuel cost */
/*                                                                    */
initFuelConsumed = initEnergy / initConvUnit
initFuelCost = initFuelConsumed * initFuelPrice
/*                                                                    */
say 'Initial Fuel Consumption: 'initFuelConsumed' 'initFuelUnit
say 'Initial Fuel Price: $'initFuelPrice' per 'initFuelUnit
say 'Initial Fuel Cost: $'initFuelCost
/*                                                                    */
/* Calculate new energy consumption & display report for user         */
/*                                                                    */
say ' '
say 'New Hot Water Temperature: 'newHWTemp' degF'
say 'New Flow Rate: 'newFlowRate' GPM'
say 'New Shower Time: 'newShwrTime' minutes'
say 'New Combustion Efficiency: 'newCombEff'%'
newCombEff = newCombEff / 100
newUsage = newFlowRate * newShwrTime
say 'New Water Consumption: 'newUsage' gallons'
newEnergy = 8.33 * newUsage * (newHWTemp - CWTemp) / newCombEff
say 'New Energy Consumption: 'newEnergy' BTUs'
/*                                                                    */
/* Convert BTUs to fuel unit, calculate fuel consumption, & fuel cost */
/*                                                                    */
newFuelConsumed = newEnergy / newConvUnit
newFuelCost = newFuelConsumed * newFuelPrice
/*                                                                    */
say 'New Fuel Consumption: 'newFuelConsumed' 'newFuelUnit
say 'New Fuel Price: $'newFuelPrice' per 'newFuelUnit
say 'New Fuel Cost: $'NewFuelCost
/*                                                                    */
/* Calculate savings & display report for user                        */
/*                                                                    */
say ' '
waterSaved = initUsage - newUsage
say 'Water Saved: 'waterSaved' gallons'
energySaved = initEnergy - newEnergy
say 'Energy Saved: 'energySaved' BTUs'
/*                                                                    */
/* if initFuel = newFuel calculate & display fuel savings             */
if initFuel = newFuel then
   do
      fuelSaved = initFuelConsumed - newFuelConsumed
      say 'Fuel Saved: 'fuelSaved' 'initFuelUnit
   end
else nop
/*                                                                    */
costSaved = initFuelCost - newFuelCost
say 'Cost Saved: $'costSaved
/*                                                                    */
exit 0
/*                                                                    */
/* * * * * * * * * * * *  E N D    P R O G R A M  * * * * * * * * * * */
/*                                                                    */
/*                           Subroutines                              */
fuelMenu:
say ' '
say '1...Electric    @$'priceElectric' per kWh'
say '2...Natural Gas @$'priceNatGas' per ccf'
say '3...Propane     @$'pricePropane' per gallon'
return
/*                                                                    */
initFuelElectric:
initFuelUnit  = 'kWh'
initConvUnit  = btu2kwh
initFuelPrice = priceElectric
return
/*                                                                    */
initFuelNatGas:
initFuelUnit  = 'ccf'
initConvUnit  = btu2ccf
initFuelPrice = priceNatGas
return
/*                                                                    */
initFuelPropane:
initFuelUnit  = 'gallons'
initConvUnit  = btu2gal
initFuelPrice = pricePropane
return
/*                                                                    */
newFuelElectric:
newFuelUnit  = 'kWh'
newConvUnit  = btu2kwh
newFuelPrice = priceElectric
return
/*                                                                    */
newFuelNatGas:
newFuelUnit  = 'ccf'
newConvUnit  = btu2ccf
newFuelPrice = priceNatGas
return
/*                                                                    */
newFuelPropane:
newFuelUnit  = 'gallons'
newConvUnit  = btu2gal
newFuelPrice = pricePropane
return
setConstants:
/*                                                                    */
/*                           Constants                                */
/*                                                                    */
/* Water Temperature Limits in degF                                   */
lowerCWTemp =  33
upperCWTemp =  79
lowerHWTemp =  80
upperHWTemp = 211
/*                                                                    */
/* Showerhead Flow Rate Limits in GPM                                 */
minFlowRate = 1
maxFlowRate = 2.5
/*                                                                    */
/* Shower Time Limits in minutes                                      */
minShwrTime =  1
maxShwrTime = 60
/*                                                                    */
/* Combustion Efficiency Limits in %                                  */
minEff =   1
maxEff = 100
/*                                                                    */
/* Conversion Factors                                                 */
btu2kwh     = 3412
btu2ccf     = 103700
btu2gallons = 91452
/*                                                                    */
/* Fuel Prices                                                        */
priceElectric = 0.13
priceNatGas   = 1.18
pricePropane  = 2.66
return
/*                                                                    */
/*                          Data Entry                                */
/*                                                                    */
CWTempDataEntry:
do until CWTemp >= lowerCWTemp & CWTemp <= upperCWTemp
   say ' '
   say 'Enter cold water temperature in degF'
   say '('lowerCWTemp'-'upperCWTemp')'
   parse pull CWTemp
end
return
/*                                                                    */
initFuelDataEntry:
clrscn
do until initFuel = 1 | initFuel = 2 | initFuel = 3
   call fuelMenu
   say 'Enter initial fuel'
   parse pull initFuel
   select
         when initFuel = 1 then call initFuelElectric
         when initFuel = 2 then call initFuelNatGas
         when initFuel = 3 then call initFuelPropane
         otherwise nop
   end
end
/* say initfuelUnit  */
/* say initconvUnit  */
/* say initfuelPrice */
return
/*                                                                    */
initHWTempDataEntry:
clrscn
do until initHWTemp >= lowerHWTemp & initHWTemp <= upperHWTemp
   say ' '
   say 'Enter initial hot water temperature in degF'
   say '('lowerHWTemp'-'upperHWTemp')'
   parse pull initHWTemp
end
return
/*                                                                    */
initFlowRateDataEntry:
clrscn
do until initFlowRate >= minFlowRate & initFlowRate <= maxFlowRate
   say ' '
   say 'Enter initial flow rate in GPM'
   say '('minFlowRate'-'maxFlowRate')'
   parse pull initFlowRate
end
return
/*                                                               */
initShwrTimeDataEntry:
clrscn
do until initShwrTime >= minShwrTime & initShwrTime <= maxShwrTime
   say ' '
   say 'Enter initial shower time in minutes'
   say '('minShwrTime'-'maxShwrTime')'
   parse pull initShwrTime
end
return
/*                                                               */
initCombEffDataEntry:
clrscn
do until initCombEff >= minEff & initCombEff <= maxEff
   say ' '
   say 'Enter initial combustion efficiency in %'
   say '('minEff'-'maxEff')'
   parse pull initCombEff
end
return
/*                                                               */
newFuelDataEntry:
clrscn
do until newFuel = 1 | newFuel = 2 | newFuel = 3
   call fuelMenu
   say 'Enter new fuel'
   parse pull newFuel
   select
         when newFuel = 1 then call newFuelElectric
         when newFuel = 2 then call newFuelNatGas
         when newFuel = 3 then call newFuelPropane
         otherwise nop
   end
end
/* say newfuelUnit  */
/* say newconvUnit  */
/* say newfuelPrice */
return
/*                                                               */
newHWTempDataEntry:
clrscn
do until newHWTemp >= lowerHWTemp & newHWTemp <= upperHWTemp
   say ' '
   say 'Enter new hot water temperature in degF'
   say '('lowerHWTemp'-'upperHWTemp')'
   parse pull newHWTemp
end
return
/*                                                               */
newFlowRateDataEntry:
clrscn
do until newFlowRate >= minFlowRate & newFlowRate <= maxFlowRate
   say ' '
   say 'Enter new flow rate in GPM'
   say '('minFlowRate'-'maxFlowRate')'
   parse pull newFlowRate
end
return
/*                                                               */
newShwrTimeDataEntry:
clrscn
do until newShwrTime >= minShwrTime & newShwrTime <= maxShwrTime
   say ' '
   say 'Enter new shower time in minutes'
   say '('minShwrTime'-'maxShwrTime')'
   parse pull newShwrTime
end
return
/*                                                               */
newCombEffDataEntry:
clrscn
do until newCombEff >= minEff & newCombEff <= maxEff
   say ' '
   say 'Enter new combustion efficiency in %'
   say '('minEff'-'maxEff')'
   parse pull newCombEff
end
return
