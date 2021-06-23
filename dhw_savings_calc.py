# This Python file uses the following encoding: utf-8                                                                                             
import math                                                                                               
#                                                                                               
# - - - - - - C O N S T A N T S - - - - -                                                                                               
#                                                                                               
# Strings                                                                                               
#                                                                                               
deErrMsg = "\nData Entry Error\n"                                                                                               
#                                                                                               
# Fuel Type Menu Limits                                                                                               
#                                                                                               
lowestMenu = 1                                                                                               
highestMenu = 3                                                                                               
#                                                                                               
# Water Temperature Limits in degF                                                                                               
#                                                                                               
lowerCWT = 33  # Don't let it freeze                                                                                               
upperCWT = 79                                                                                               
lowerHWT = 80                                                                                               
upperHWT = 211 # Don't let it boil                                                                                               
#                                                                                               
# Shower Time Limits in minutes                                                                                               
#                                                                                               
minShwrTime = 1                                                                                                
maxShwrTime = 60                                                                                                
#                                                                                               
# Showerhead Flow Rate Limits in GPM (gallons per minute)                                                                                               
#                                                                                               
minFlowRate = 1                                                                                               
maxFlowRate = 2.5                                                                                               
#                                                                                               
# Combustion Efficiency Limits in %                                                                                               
#                                                                                               
minEff = 1                                                                                               
maxEff = 100                                                                                               
#                                                                                               
# Conversion Factors                                                                                               
#                                                                                               
BTU2kwh            = 3412                                                                                               
BTU2ccf            = 103700                                                                                               
BTU2GallonsPropane = 91452                                                                                               
#                                                                                              
# The conversion factor for pounds of propane is affected by                                                                                              
# the density of propane.  The density of propane is affected                                                                                              
# by the ambient temperature.                                                                                              
#                                                                                                                                                              
# The density of liquid propane at 25°C (77°F) is 0.493 g/cm3,                                                                                                   
# which is equivalent to 4.11 pounds per U.S. liquid gallon.                                                                                                   
# or 493 g/L. Propane expands at 1.5% per 10°F.  Thus, liquid                                                                                                   
# propane has a density of approximately 4.2 pounds per gallon                                                                                                 
# 504 g/L) at 60°F (15.6°C).                                                                                                                                     
# -- Wikipedia  https://en.wikipedia.org/wiki/Propane                                                                                                          
#                                                                                                                                                               
# Fuel Prices                                                                                               
#                                                                                               
priceElectric = 0.13 # per kWh                                                                                               
priceNatGas   = 1.18 # per ccf                                                                                               
pricePropane  = 2.66 # per gallon                                                                                               
#                                                                                               
# - - - - - - - - - - D A T A   E N T R Y - - - - - - - - - -                                                                                               
#                                                                                               
print("\n")                                                                                               
print("Domestic Hot Water Savings Calculator")                                                                                               
print("Written by, Clifford A. Chipman, EMIT")                                                                                               
print("February 2, 2021")                                                                                               
print("in Python3 for z/OS, Windows, & Linux")                                                                                               
#                                                                                               
coldWaterTemperature = 0                                   
#                               
initFuelType = 0                                   
initHotWaterTemperature = 0                                   
initFlowRate = 0                                  
initShwrTime = 0                                 
initCombEff = 0                                
#                               
newFuelType = 0                              
newHotWaterTemperature = 0                             
newFlowRate = 0                            
newShwrTime = 0                           
newCombEff = 0                          
#                                   
# def CWTempDataEntry():                                                                                         
coldWaterTemperature = 0                                                                                               
while (coldWaterTemperature < lowerCWT or coldWaterTemperature > upperCWT):                                                                                               
          print("\r")                                                                                           
          print("Water Temperature Limits: {0} - {1} degF".format(lowerCWT,upperCWT))                                                                                           
          userInput = input("Enter cold water temperature (in degF): ")                                                                                                       
#                                                                                               
# Check for valid user input                                                                                               
          try:                                                                                           
              coldWaterTemperature = float(userInput)                                                                                                  
          except:                                                                                           
              print(deErrMsg)                                                                                                       
              coldWaterTemperature = 0                                                                                           
#                        
#   return coldWaterTemperature                         
#                                                                                            
# def initFuelDataEntry():                                                                                        
initFuelType = 0                                                                                               
while (initFuelType < lowestMenu or initFuelType > highestMenu):                                                                                               
          print("\r")                                                                                           
          print("1........Electric    @${0} per kWh".format(priceElectric))                                                                                     
          print("2........Natural Gas @${0} per ccf".format(priceNatGas))                                                                                     
          print("3........Propane     @${0} per gallon".format(pricePropane))                                                                                     
#         print("4........Return to z/OS")                                                                                           
          userInput = input("Enter initial fuel type: ")                                                                                           
#                                                                                               
# Check for valid user input                                                                                               
          try:                                                                                           
              initFuelType = int(userInput)                                                                                                            
          except:                                                                                           
              print(deErrMsg)                                                                                                       
              initFuelType = 0                                                                                                   
#                        
#   return initFuelType                                 
#                                                                                               
# def initHWTempDataEntry():                                                                                      
initHotWaterTemperature = 0                                                                                               
while (initHotWaterTemperature < lowerHWT or initHotWaterTemperature > upperHWT):                                                                                               
          print("\r")                                                                                           
          print("Water Temperature Limits: {0} - {1} degF".format(lowerHWT,upperHWT))                                                                                           
          userInput = input("Enter initial hot water temperature (in degF): ")                                                                                                           
#                                                                                               
# Check for valid user input                                                                                               
          try:                                                                                           
              initHotWaterTemperature = float(userInput)                                                                                                     
          except:                                                                                           
              print(deErrMsg)                                                                                                       
              initHotWaterTemperature = 0                                                                                           
#                        
#   return initHotWaterTemperature                       
#                                                                                               
# def initFlowRateDataEntry():                                                                                  
initFlowRate = 0                                                                                               
while (initFlowRate < minFlowRate or initFlowRate > maxFlowRate):                                                                                               
          print("\r")                                                                                           
          print("Flow Rate Limits: {0} - {1} GPM".format(minFlowRate,maxFlowRate))                                                                                           
          userInput = input("Enter initial showerhead flow rate (in GPM): ")                                                                                           
#                                                                                               
# Check for valid user input                                                                                               
          initFlowRate = float(userInput)                                                                                           
          try:                                                                                           
              initFlowRate = float(userInput)                                                                                                                
          except:                                                                                           
              print(deErrMsg)                                                                                                       
              initFlowRate = 0                                                                                                      
#                        
#   return initFlowRate                                 
#                                                                                               
# def initShwrTimeDataEntry():                                                                                
initShwrTime = 0                                                                                                
while (initShwrTime < minShwrTime or initShwrTime > maxShwrTime):                                                                                                   
          print("\r")                                                                                           
          print("Daily Shower Time Limits: {0} - {1} minutes".format(minShwrTime,maxShwrTime))                                                                                             
          userInput = input("Enter initial total daily shower time (in minutes): ")                                                                                           
#                                                                                               
# Check for valid user input                                                                                               
          initShwrTime = float(userInput)                                                                                            
          try:                                                                                           
              initShwrTime = float(userInput)                                                                                                                
          except:                                                                                           
              print(deErrMsg)                                                                                                       
              initShwrTime = 0                                                                                                      
#                        
#   return initShwrTime                                 
#                                                                                               
# def initCombEffDataEntry():                                                                            
initCombEff = 0                                                                                               
while (initCombEff < minEff or initCombEff > maxEff):                                                                                               
          print("\r")                                                                                           
          print("Combustion Efficiency Limits: {0} - {1} %".format(minEff,maxEff))                                                                                           
          userInput = input("Enter initial combustion efficiency (in %): ")                                                                                           
#                                                                                               
# Check for valid user input                                                                                               
          initCombEff = float(userInput)                                                                                               
          try:                                                                                           
              initCombEff = float(userInput)                                                                                                                 
          except:                                                                                           
              print(deErrMsg)                                                                                                       
              initCombEff = 0                                                                                                       
#                        
#   return initCombEff                                  
#                                                                                               
# def newFuelDataEntry():                                                                          
newFuelType = 0                                                                                                
while (newFuelType < lowestMenu or newFuelType > highestMenu):                                                                                                 
          print("\r")                                                                                           
          print("1........Electric    @${0} per kWh".format(priceElectric))                                                                          
          print("2........Natural Gas @${0} per ccf".format(priceNatGas))                                                                         
          print("3........Propane     @${0} per gallon".format(pricePropane))                                                                         
#         print("4........Return to z/OS")                                                                                           
          userInput = input("Enter new fuel type: ")                                                                                               
#                                                                                               
# Check for valid user input                                                                                               
          try:                                                                                           
              newFuelType = int(userInput)                                                                                                             
          except:                                                                                           
              print(deErrMsg)                                                                                                       
              newFuelType = 0                                                                                                    
#                        
#   return newFuelType                                  
#                                                                                               
# def newHWTempDataEntry():                                                                      
newHotWaterTemperature = 0                                                                                                
while (newHotWaterTemperature < lowerHWT or newHotWaterTemperature > upperHWT):                                                                                                 
          print("\r")                                                                                           
          print("Water Temperature Limits: {0} - {1} degF".format(lowerHWT,upperHWT))                                                                                           
          userInput = input("Enter new hot water temperature (in degF): ")                                                                                                               
#                                                                                               
# Check for valid user input                                                                                               
          try:                                                                                           
              newHotWaterTemperature = float(userInput)                                                                                                      
          except:                                                                                           
              print(deErrMsg)                                                                                                       
              newHotWaterTemperature = 0                                                                                            
#                        
#   return newHotWaterTemperature                       
#                                                                                               
# def newFlowRateDataEntry():                                                                    
newFlowRate = 0                                                                                                
while (newFlowRate < minFlowRate or newFlowRate > maxFlowRate):                                                                                                 
          print("\r")                                                                                           
          print("Flow Rate Limits: {0} - {1} GPM".format(minFlowRate,maxFlowRate))                                                                                           
          userInput = input("Enter new showerhead flow rate (in GPM): ")                                                                                               
#                                                                                               
# Check for valid user input                                                                                               
          newFlowRate = float(userInput)                                                                                            
          try:                                                                                           
              newFlowRate = float(userInput)                                                                                                                 
          except:                                                                                           
              print(deErrMsg)                                                                                                       
              newFlowRate = 0                                                                                                       
#                        
#   return newFlowRate                                  
#                                                                                               
# def newShwrTimeDataEntry():                                                                  
newShwrTime = 0                                                                                                 
while (newShwrTime < minShwrTime or newShwrTime > maxShwrTime):                                                                                                     
          print("\r")                                                                                           
          print("Daily Shower Time Limits: {0} - {1} minutes".format(minShwrTime,maxShwrTime))                                                                                             
          userInput = input("Enter new total daily shower time (in minutes): ")                                                                                               
#                                                                                               
# Check for valid user input                                                                                               
          newShwrTime = float(userInput)                                                                                             
          try:                                                                                           
              newShwrTime = float(userInput)                                                                                                                 
          except:                                                                                           
              print(deErrMsg)                                                                                                       
              newShwrTime = 0                                                                                                       
#                        
#   return newShwrTime                                  
#                                                                                               
# def newCombEffDataEntry():                                                              
newCombEff = 0                                                                                                
while (newCombEff < minEff or newCombEff > maxEff):                                                                                                 
          print("\r")                                                                                           
          print("Combustion Efficiency Limits: {0} - {1} %".format(minEff,maxEff))                                                                                           
          userInput = input("Enter new combustion efficiency (in %): ")                                                                                               
#                                                                                               
# Check for valid user input                                                                                               
          newCombEff = float(userInput)                                                                                                
          try:                                                                                           
              newCombEff = float(userInput)                                                                                                                  
          except:                                                                                           
              print(deErrMsg)                                                                                                       
              newCombEff = 0                                                                                                        
#                        
#   return newCombEff                                   
#                                                                                               
# - - D O M E S T I C   H O T   W A T E R   S A V I N G S - -                                                                                               
#                                                                                               
# Call data entry functions                                                              
#                                                              
# CWTempDataEntry()                                                           
#                                                       
# initFuelDataEntry()                                                          
# initHWTempDataEntry()                                                         
# initFlowRateDataEntry()                                                        
# initShwrTimeDataEntry()                                                       
# initCombEffDataEntry()                                                      
#                                                      
# newFuelDataEntry()                                                   
# newHWTempDataEntry()                                                  
# newFlowRateDataEntry()                                                 
# newShwrTimeDataEntry()                                                
# newCombEffDataEntry()                                               
#                                                           
# Calculate initial energy consumption & display report for user                                                                                               
#                                                                                               
print("\r")                                                
print("Cold Water Inlet Temperature: {0} degF".format(coldWaterTemperature))                                                
print("\r")                                                
print("Initial Hot Water Temperature: {0} degF".format(initHotWaterTemperature))                                                
print("Initial Flow Rate: {0} GPM".format(initFlowRate))                                                
print("Initial Shower Time: {0} minutes".format(initShwrTime))                                                
print("Initial Combustion Efficiency: {0}%".format(initCombEff))                                              
#                                               
initCombEff = initCombEff / 100                                                                                               
initUsage = initFlowRate * initShwrTime                                                                                                                  
#                                             
print("\r")                                                                                               
print("Initial Water Consumption: {0} gallons".format(initUsage))                                             
#                                            
initEnergy = 8.33 * initUsage * (initHotWaterTemperature - coldWaterTemperature) / initCombEff                                                                                                    
#                                                                                               
print("Initial Energy Consumption: {0:.1f} BTUs".format(initEnergy))                                                                                                   
#                                                                                               
# Apply energy unit conversions                                                                                               
#                                                                                               
if (initFuelType == 1):                                                                                               
   initfuelUnit  = "kWh"                                                                                           
   initconvUnit  = BTU2kwh                                                                                           
   initfuelPrice = priceElectric                                                                                           
elif (initFuelType == 2):                                                                                               
   initfuelUnit  = "ccf"                                                                                           
   initconvUnit  = BTU2ccf                                                                                           
   initfuelPrice = priceNatGas                                                                                           
elif (initFuelType == 3):                                                                                               
   initfuelUnit  = "gallons"                                                                                           
   initconvUnit  = BTU2GallonsPropane                                                                                           
   initfuelPrice = pricePropane                                                                                           
else:                                                                                                                               
   print("Initial Fuel Type Error")                                                                                               
#                                                                                               
initFuelConsumed = initEnergy / initconvUnit                                                                                           
initCost = initFuelConsumed * initfuelPrice                                                                                           
#                                                                                               
print("Initial Fuel Consumption: {0:.1f} {1}".format(initFuelConsumed,initfuelUnit))                                                                                           
print("Initial Fuel Cost: ${0:.2f} @${1} per {2}\n".format(initCost,initfuelPrice,initfuelUnit))                                                                                       
#                                                                                               
# Calculate new energy consumption                                                                                                             
#                                                                                               
print("\r")                                                
print("New Hot Water Temperature: {0} degF".format(newHotWaterTemperature))                                                     
print("New Flow Rate: {0} GPM".format(newFlowRate))                                                     
print("New Shower Time: {0} minutes".format(newShwrTime))                                                     
print("New Combustion Efficiency: {0}%".format(newCombEff))                                                   
#                                               
newCombEff = newCombEff / 100                                                                                                 
newUsage = newFlowRate * newShwrTime                                                                                                                     
print("\r")                                                                                               
print("New Water Consumption: {0} gallons".format(newUsage))                                                  
#    
newEnergy = 8.33 * newUsage * (newHotWaterTemperature - coldWaterTemperature) / newCombEff                                                                                                      
#                                                                                               
print("    New Energy Consumption: {0:.1f} BTUs".format(newEnergy))                                                                                                    
#                                                                                               
# Apply energy unit conversions                                                                                               
#                                                                                               
if (newFuelType == 1):                                                                                               
   newfuelUnit  = "kWh"                                                                                            
   newconvUnit  = BTU2kwh                                                                                            
   newfuelPrice = priceElectric                                                                                            
elif (newFuelType == 2):                                                                                                
   newfuelUnit  = "ccf"                                                                                            
   newconvUnit  = BTU2ccf                                                                                            
   newfuelPrice = priceNatGas                                                                                            
elif (newFuelType == 3):                                                                                                
   newfuelUnit  = "gallons"                                                                                            
   newconvUnit  = BTU2GallonsPropane                                                                                            
   newfuelPrice = pricePropane                                                                                            
else:                                                                                                                               
   print("New Fuel Type Error")                                                                                               
#                                                                                               
newFuelConsumed = newEnergy / newconvUnit                                                                                              
newCost = newFuelConsumed * newfuelPrice                                                                                              
#                                                                                               
print("    New Fuel Consumption: {0:.1f} {1}".format(newFuelConsumed,newfuelUnit))                                                                                              
print("    New Fuel Cost: ${0:.2f} @${1} per {2}\n".format(newCost,initfuelPrice,newfuelUnit))                                                                                        
#                                                                                               
waterSaved = initUsage - newUsage 
energySaved = initEnergy - newEnergy                                                                                               
fuelSaved = initFuelConsumed - newFuelConsumed                                                                                               
costSaved = initCost - newCost                                                                                               
#                                                                                               
print("Water Saved: {0:.1f} gallons".format(waterSaved))
print("Energy Saved: {0:.1f} BTUs".format(energySaved))                                                                                               
#                                                                                               
# Same fuel?                                                                                               
if (initFuelType == newFuelType):                                                                                               
   print("Fuel Saved: {0:.1f} {1}".format(fuelSaved,initfuelUnit))                                                                                           
#                                                                                                                                                         
print("Cost Saved: ${0:.2f}\n".format(costSaved))                                                                                               
