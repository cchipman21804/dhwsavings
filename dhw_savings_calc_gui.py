# This Python file uses the following encoding: utf-8
from tkinter import *
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
defaultCWT = '65'
upperCWT = 79
#
lowerHWT = 80
defaultHWT = '125'
upperHWT = 211 # Don't let it boil
#
# Shower Time Limits in minutes
#
minShwrTime = 1
defaultShwrTime = '10'
maxShwrTime = 60
#
# Showerhead Flow Rate Limits in GPM (gallons per minute)
#
minFlowRate = 1
maxFlowRate = 2.5
defaultFlowRate = str(maxFlowRate)
#
# Combustion Efficiency Limits in %
#
minEff = 1
defaultEff = '98'
maxEff = 100
#
# Conversion Factors
#
BTU2kwh            = 3412
BTU2ccf            = 103700
BTU2GallonsPropane = 91452
BTU2GallonsOil     = 138500
#
# The conversion factor for pounds of propane is affected by
# the density of propane.  The density of propane is affected
# by the ambient temperature.
#
# The density of liquid propane at 25°C (77°F) is 0.493 g/cm3,
# which is equivalent to 4.11 pounds per U.S. liquid gallon.
# or 493 g/L. Propane expands at 1.5% per 10°F.  Thus, liquid
# propane has a density of approximately 4.2 pounds per gallon
# (504 g/L) at 60°F (15.6°C).
# -- Wikipedia  https://en.wikipedia.org/wiki/Propane
#
# Fuel Prices
#
defaultPriceElectric    = 0.13 # per kWh
defaultPriceNatGas      = 1.18 # per ccf
defaultPricePropane     = 2.66 # per gallon
defaultPriceOil         = 2.86 # per gallon
#
# Initialize calculation variables
orgTempDiff = 0.0
orgWtrUsage = 0.0
orgCombEff = 0.0
orgBTU = 0.0
orgKwh = 0.0
orgElectricCost = 0.0
orgCcf = 0.0
orgGasCost = 0.0
orgGalPropane = 0.0
orgPropaneCost = 0.0
orgGalOil = 0.0
orgOilCost = 0.00
#
newTempDiff = 0.0
newWtrUsage = 0.0
newCombEff = 0.0
newBTU = 0.0
newKwh = 0.0
newElectricCost = 0.0
newCcf = 0.0
newGasCost = 0.0
newGalPropane = 0.0
newPropaneCost = 0.00
newGalOil = 0.0
newOilCost = 0.0
#
waterSavings = 0.0
btuSavings = 0.0
kwhSavings = 0.0
ccfSavings = 0.0
gallonsPropaneSavings = 0.0
gallonsOilSavings = 0.0
#
electricCostSavings = 0.0
gasCostSavings = 0.0
propaneCostSavings = 0.0
oilCostSavings = 0.0

# Application window parameters
#windowWdth = 800
#windowHgt = 600
#
# Grid Rows
headerRow               = 0
coldWtrTempRow          = 1
hotWtrTempRow           = 2
shwrHeadFlowRateRow     = 3
shwrTimeRow             = 4
wtrUsageRow             = 5
combEffRow              = 6
btuRow                  = 7
electricUsageRow        = 8
electricCostRow         = 9
natgasUsageRow          = 11
natgasCostRow           = 12
propaneUsageRow         = 15
propaneCostRow          = 16
oilUsageRow             = 19
oilCostRow              = 20
#
# Grid Columns
fuelsHdrColumn          = 0
fuelPricePrefixColumn   = 1
fuelPriceColumn         = 2
fuelPriceSuffixColumn   = 3
condxLabelColumn        = 4
orgCondxColumn          = 5
orgCondxUnitColumn      = 6
minusColumn             = 7
newCondxColumn          = 8
newCondxUnitColumn      = 9
savingsColumn           = 10

#
# Functions

def arrangeWndwGrid():
#
# Fuels Column Headers
    Label(mainWndw, text = "Fuels", font = "bold").grid(row=headerRow, column = fuelsHdrColumn, columnspan = 3)
    Label(mainWndw, text = "Electricity:").grid(row = electricUsageRow, column = fuelsHdrColumn, sticky = 'w')
    Label(mainWndw, text = "Natural Gas:").grid(row = natgasUsageRow, column = fuelsHdrColumn, sticky = 'w')
    Label(mainWndw, text = "Propane:").grid(row = propaneUsageRow, column = fuelsHdrColumn, sticky = 'w')
    Label(mainWndw, text = "#2 Fuel Oil:").grid(row = oilUsageRow, column = fuelsHdrColumn, sticky = 'w')
#
# Electric Fuel Price
    Label(mainWndw, text = '@$').grid(row = electricUsageRow, column = fuelPricePrefixColumn, sticky = 'e')
    Label(mainWndw, text = 'per kWh').grid(row = electricUsageRow, column = fuelPriceSuffixColumn, sticky = 'w')
#
# Natural Gas Fuel Price
    Label(mainWndw, text = '@$').grid(row = natgasUsageRow, column = fuelPricePrefixColumn, sticky = 'e')
    Label(mainWndw, text = 'per ccf').grid(row = natgasUsageRow, column = fuelPriceSuffixColumn, sticky = 'w')
#
# Propane Fuel Price
    Label(mainWndw, text = '@$').grid(row = propaneUsageRow, column = fuelPricePrefixColumn, sticky = 'e')
    Label(mainWndw, text = 'per gallon').grid(row = propaneUsageRow, column = fuelPriceSuffixColumn, sticky = 'w')
#
# Oil Fuel Prices
    Label(mainWndw, text = '@$').grid(row = oilUsageRow, column = fuelPricePrefixColumn, sticky = 'e')
    Label(mainWndw, text = 'per gallon').grid(row = oilUsageRow, column = fuelPriceSuffixColumn, sticky = 'w')
#
# Original Conditions Column
    Label(mainWndw, text = "|", font = "bold").grid(row = headerRow, column = fuelPriceSuffixColumn)
    Label(mainWndw, text = "Original Conditions", font = "bold").grid(row = headerRow, column = condxLabelColumn, columnspan = 3)
#
    Label(mainWndw, text = "Cold Water Temperature:").grid(row = coldWtrTempRow, column = condxLabelColumn, sticky = 'e')
    Label(mainWndw, text = "degF").grid(row = coldWtrTempRow, column = orgCondxUnitColumn, sticky = 'w')
#
    Label(mainWndw, text = "Hot Water Temperature:").grid(row = hotWtrTempRow, column = condxLabelColumn, sticky = 'e')
    Label(mainWndw, text = "degF").grid(row = hotWtrTempRow, column = orgCondxUnitColumn, sticky = 'w')
#
    Label(mainWndw, text = "Shower Head Flow Rate:").grid(row = shwrHeadFlowRateRow, column = condxLabelColumn, sticky = 'e')
    Label(mainWndw, text = "GPM").grid(row = shwrHeadFlowRateRow, column = orgCondxUnitColumn, sticky = 'w')
#
    Label(mainWndw, text = "Shower Time:").grid(row = shwrTimeRow, column = condxLabelColumn, sticky = 'e')
    Label(mainWndw, text = "minutes").grid(row = shwrTimeRow, column = orgCondxUnitColumn, sticky = 'w')
#
    Label(mainWndw, text = "Water Usage:").grid(row = wtrUsageRow, column = condxLabelColumn, sticky = 'e')
    Label(mainWndw, text = "gallons").grid(row = wtrUsageRow, column = orgCondxUnitColumn, sticky = 'w')
#
    Label(mainWndw, text = "Combustion Efficiency:").grid(row = combEffRow, column = condxLabelColumn, sticky = 'e')
    Label(mainWndw, text = "%").grid(row = combEffRow, column = orgCondxUnitColumn, sticky = 'w')
#
    Label(mainWndw, text = "Heat:").grid(row = btuRow, column = condxLabelColumn, sticky = 'e')
    Label(mainWndw, text = "BTUs").grid(row = btuRow, column = orgCondxUnitColumn, sticky = 'w')
#
# Original Electric Usage & Cost
    Label(mainWndw, text = "equals:").grid(row = electricUsageRow, column = condxLabelColumn, sticky = 'e')
    Label(mainWndw, text = "kWhs").grid(row = electricUsageRow, column = orgCondxUnitColumn, sticky = 'w')
    Label(mainWndw, text = "costs:").grid(row = electricCostRow, column = condxLabelColumn, sticky = 'e')
    Label(mainWndw, text = "per shower").grid(row = electricCostRow, column = orgCondxUnitColumn, sticky = 'w')
#
# Original Natural Gas Usage & Cost
    Label(mainWndw, text = "equals:").grid(row = natgasUsageRow, column = condxLabelColumn, sticky = 'e')
    Label(mainWndw, text = "ccf").grid(row = natgasUsageRow, column = orgCondxUnitColumn, sticky = 'w')
    Label(mainWndw, text = "costs:").grid(row = natgasCostRow, column = condxLabelColumn, sticky = 'e')
    Label(mainWndw, text = "per shower").grid(row = natgasCostRow, column = orgCondxUnitColumn, sticky = 'w')
#
# Original Propane Usage & Cost
    Label(mainWndw, text = "equals:").grid(row = propaneUsageRow, column = condxLabelColumn, sticky = 'e')
    Label(mainWndw, text = "gallons").grid(row = propaneUsageRow, column = orgCondxUnitColumn, sticky = 'w')
    Label(mainWndw, text = "costs:").grid(row = propaneCostRow, column = condxLabelColumn, sticky = 'e')
    Label(mainWndw, text = "per shower").grid(row = propaneCostRow, column = orgCondxUnitColumn, sticky = 'w')
#
# Original Oil Usage & Cost
    Label(mainWndw, text = "equals:").grid(row = oilUsageRow, column = condxLabelColumn, sticky = 'e')
    Label(mainWndw, text = "gallons").grid(row = oilUsageRow, column = orgCondxUnitColumn, sticky = 'w')
    Label(mainWndw, text = "costs:").grid(row = oilCostRow, column = condxLabelColumn, sticky = 'e')
    Label(mainWndw, text = "per shower").grid(row = oilCostRow, column = orgCondxUnitColumn, sticky = 'w')
#
# Minus Column
    Label(mainWndw, text = "|", font = "bold").grid(row = headerRow, column = minusColumn)
    Label(mainWndw, text = "minus").grid(row = wtrUsageRow, column = minusColumn)
    Label(mainWndw, text = "minus").grid(row = btuRow, column = minusColumn)
    Label(mainWndw, text = "minus").grid(row = electricUsageRow, column = minusColumn)
    Label(mainWndw, text = "minus").grid(row = electricCostRow, column = minusColumn)
    Label(mainWndw, text = "minus").grid(row = natgasUsageRow, column = minusColumn)
    Label(mainWndw, text = "minus").grid(row = natgasCostRow, column = minusColumn)
    Label(mainWndw, text = "minus").grid(row = propaneUsageRow, column = minusColumn)
    Label(mainWndw, text = "minus").grid(row = propaneCostRow, column = minusColumn)
    Label(mainWndw, text = "minus").grid(row = oilUsageRow, column = minusColumn)
    Label(mainWndw, text = "minus").grid(row = oilCostRow, column = minusColumn)

#
# New Conditions Column
    Label(mainWndw, text = "New Conditions", font = "bold").grid(row = headerRow, column = newCondxColumn, columnspan = 2)
    Label(mainWndw, text = "degF").grid(row = hotWtrTempRow, column = newCondxUnitColumn, sticky = 'w')
    Label(mainWndw, text = "GPM").grid(row = shwrHeadFlowRateRow, column = newCondxUnitColumn, sticky = 'w')
    Label(mainWndw, text = "minutes").grid(row = shwrTimeRow, column = newCondxUnitColumn, sticky = 'w')
    Label(mainWndw, text = "gallons").grid(row = wtrUsageRow, column = newCondxUnitColumn, sticky = 'w')
    Label(mainWndw, text = "%").grid(row = combEffRow, column = newCondxUnitColumn, sticky = 'w')
    Label(mainWndw, text = "BTUs").grid(row = btuRow, column = newCondxUnitColumn, sticky = 'w')
#
# New Electric Usage & Cost
    Label(mainWndw, text = "kWhs").grid(row = electricUsageRow, column = newCondxUnitColumn, sticky = 'w')
    Label(mainWndw, text = "per shower").grid(row = electricCostRow, column = newCondxUnitColumn, sticky = 'w')
#
# New Natural Gas Usage & Cost
    Label(mainWndw, text = "ccf").grid(row = natgasUsageRow, column = newCondxUnitColumn, sticky = 'w')
    Label(mainWndw, text = "per shower").grid(row = natgasCostRow, column = newCondxUnitColumn, sticky = 'w')
#
# New Propane Usage & Cost
    Label(mainWndw, text = "gallons").grid(row = propaneUsageRow, column = newCondxUnitColumn, sticky = 'w')
    Label(mainWndw, text = "per shower").grid(row = propaneCostRow, column = newCondxUnitColumn, sticky = 'w')
#
# New Oil Usage & Cost
    Label(mainWndw, text = "gallons").grid(row = oilUsageRow, column = newCondxUnitColumn, sticky = 'w')
    Label(mainWndw, text = "per shower").grid(row = oilCostRow, column = newCondxUnitColumn, sticky = 'w')
#
# Savings Column
    Label(mainWndw, text = "   |   Savings per Shower", font = "bold").grid(row = headerRow, column = savingsColumn)

def updateEntries(QuantitiesList):
    orgColdWtrTempEntry.delete(0,END)
    orgColdWtrTempEntry.insert(0,QuantitiesList[0])
    orgHotWtrTempEntry.delete(0,END)
    orgHotWtrTempEntry.insert(0,QuantitiesList[1])
    orgShwrHeadFlowRateEntry.delete(0,END)
    orgShwrHeadFlowRateEntry.insert(0,QuantitiesList[2])
    orgShwrTimeEntry.delete(0,END)
    orgShwrTimeEntry.insert(0,QuantitiesList[3])
    orgCombEffEntry.delete(0,END)
    orgCombEffEntry.insert(0,QuantitiesList[4])
    newHotWtrTempEntry.delete(0,END)
    newHotWtrTempEntry.insert(0,QuantitiesList[5])
    newShwrHeadFlowRateEntry.delete(0,END)
    newShwrHeadFlowRateEntry.insert(0,QuantitiesList[6])
    newShwrTimeEntry.delete(0,END)
    newShwrTimeEntry.insert(0,QuantitiesList[7])
    newCombEffEntry.delete(0,END)
    newCombEffEntry.insert(0,QuantitiesList[8])
    electricPriceEntry.delete(0,END)
    electricPriceEntry.insert(0,QuantitiesList[9])
    natgasPriceEntry.delete(0,END)
    natgasPriceEntry.insert(0,QuantitiesList[10])
    propanePriceEntry.delete(0,END)
    propanePriceEntry.insert(0,QuantitiesList[11])
    oilPriceEntry.delete(0,END)
    oilPriceEntry.insert(0,QuantitiesList[12])
#
# Calculation functions:
def tempDiff(hot,cold):                 # Calculate water temperature difference for calcBTU function
    return float(hot) - float(cold)

def waterUsage(flowRate,time):          # Calculate water usage from shower flow rate and shower duration
    return float(flowRate) * float(time)

def calcBTU(water,tempDiff,combEff):    # Calculate BTUs required to raise water temperature by temperature difference
    combEff = float(combEff)/100
    return round(8.33 * water * tempDiff / combEff,1)

def calckWh(btu):                       # Convert BTUs to kWh
    return round(btu / BTU2kwh,2)

def calcCcf(btu):                       # Convert BTUs to ccf
    return round(btu / BTU2ccf,2)

def calcGalPropane(btu):                # Convert BTUs to gallons of propane
    return round(btu / BTU2GallonsPropane,2)

def calcGalOil(btu):                    # Convert BTUs to gallons of oil
    return round(btu / BTU2GallonsOil,2)

def calcCost(quantity,price):           # Calculate fuel cost
    return round(quantity * float(price),2)
#
# Update the window
def updateResults():
#
# Calculate old parameters
    orgTempDiff = tempDiff(orgHotWtrTempEntry.get(),orgColdWtrTempEntry.get())
    orgWtrUsage = round(waterUsage(orgShwrHeadFlowRateEntry.get(),orgShwrTimeEntry.get()),1)
    orgBTU = calcBTU(orgWtrUsage,orgTempDiff,orgCombEffEntry.get())
    orgKwh = calckWh(orgBTU)
    orgElectricCost = calcCost(orgKwh,electricPriceEntry.get())
    orgCcf = calcCcf(orgBTU)
    orgGasCost = calcCost(orgCcf,natgasPriceEntry.get())
    orgGalPropane = calcGalPropane(orgBTU)
    orgPropaneCost = calcCost(orgGalPropane,propanePriceEntry.get())
    orgGalOil = calcGalOil(orgBTU)
    orgOilCost = calcCost(orgGalOil, oilPriceEntry.get())
#
# Calculate new parameters
    newTempDiff = tempDiff(newHotWtrTempEntry.get(),orgColdWtrTempEntry.get())
    newWtrUsage = round(waterUsage(newShwrHeadFlowRateEntry.get(),newShwrTimeEntry.get()),1)
    newBTU = calcBTU(newWtrUsage,newTempDiff,newCombEffEntry.get())
    newKwh = calckWh(newBTU)
    newElectricCost = round(calcCost(newKwh,electricPriceEntry.get()),2)
    newCcf = calcCcf(newBTU)
    newGasCost = round(calcCost(newCcf,natgasPriceEntry.get()),2)
    newGalPropane = calcGalPropane(newBTU)
    newPropaneCost = calcCost(newGalPropane,propanePriceEntry.get())
    newGalOil = calcGalOil(newBTU)
    newOilCost = calcCost(newGalOil, oilPriceEntry.get())
#
# Calculate savings
    waterSavings = round(orgWtrUsage - newWtrUsage,1)
    btuSavings = round(orgBTU - newBTU,1)
    kwhSavings = round(orgKwh - newKwh,2)
    electricCostSavings = round(orgElectricCost - newElectricCost,2)
    ccfSavings = round(orgCcf - newCcf,2)
    gasCostSavings = round(orgGasCost - newGasCost,2)
    gallonsPropaneSavings = round(orgGalPropane - newGalPropane,2)
    propaneCostSavings = round(orgPropaneCost - newPropaneCost,2)
    gallonsOilSavings = round(orgGalOil - newGalOil,2)
    oilCostSavings = round(orgOilCost - newOilCost,2)
#
# Original Conditions Results:
    Label(mainWndw, text = f'{orgWtrUsage}').grid(row = wtrUsageRow, column = orgCondxColumn, sticky = 'e')
#
# Display BTUs with commas to separate thousands
    Label(mainWndw, text = f'{orgBTU:,}').grid(row = btuRow, column = orgCondxColumn, sticky = 'e')
    Label(mainWndw, text = f'{orgKwh}').grid(row = electricUsageRow, column = orgCondxColumn, sticky = 'e')
#
# Display dollar amount floats as 2-digit
    Label(mainWndw, text = f'${orgElectricCost:.2f}').grid(row = electricCostRow, column = orgCondxColumn, sticky = 'e')
    Label(mainWndw, text = f'{orgCcf}').grid(row = natgasUsageRow, column = orgCondxColumn, sticky = 'e')
#
# Display dollar amount floats as 2-digit
    Label(mainWndw, text = f'${orgGasCost:.2f}').grid(row = natgasCostRow, column = orgCondxColumn, sticky = 'e')
    Label(mainWndw, text = f'{orgGalPropane}').grid(row = propaneUsageRow, column = orgCondxColumn, sticky = 'e')
#
# Display dollar amount floats as 2-digit
    Label(mainWndw, text = f'${orgPropaneCost:.2f}').grid(row = propaneCostRow, column = orgCondxColumn, sticky = 'e')
    Label(mainWndw, text = f'{orgGalOil}').grid(row = oilUsageRow, column = orgCondxColumn, sticky = 'e')
#
# Display dollar amount floats as 2-digit
    Label(mainWndw, text = f'${orgOilCost:.2f}').grid(row = oilCostRow, column = orgCondxColumn, sticky = 'e')
#
# New Conditions Results:
    Label(mainWndw, text = f'{newWtrUsage}').grid(row = wtrUsageRow, column = newCondxColumn, sticky = 'e')
#
# Display BTUs with commas to separate thousands
    Label(mainWndw, text = f'{newBTU:,}').grid(row = btuRow, column = newCondxColumn, sticky = 'e')
    Label(mainWndw, text = f'{newKwh}').grid(row = electricUsageRow, column = newCondxColumn, sticky = 'e')
#
# Display dollar amount floats as 2-digit
    Label(mainWndw, text = f'${newElectricCost:.2f}').grid(row = electricCostRow, column = newCondxColumn, sticky = 'e')
    Label(mainWndw, text = f'{newCcf}').grid(row = natgasUsageRow, column = newCondxColumn, sticky = 'e')
#
# Display dollar amount floats as 2-digit
    Label(mainWndw, text = f'${newGasCost:.2f}').grid(row = natgasCostRow, column = newCondxColumn, sticky = 'e')
    Label(mainWndw, text = f'{newGalPropane}').grid(row = propaneUsageRow, column = newCondxColumn, sticky = 'e')
#
# Display dollar amount floats as 2-digit
    Label(mainWndw, text = f'${newPropaneCost:.2f}') .grid(row = propaneCostRow, column = newCondxColumn, sticky = 'e')
    Label(mainWndw, text = f'{newGalOil}').grid(row = oilUsageRow, column = newCondxColumn, sticky = 'e')
#
# Display dollar amount floats as 2-digit
    Label(mainWndw, text = f'${newOilCost:.2f}').grid(row = oilCostRow, column = newCondxColumn, sticky = 'e')
#
# Display savings (blank the cell if quantity saved is ZERO
    if waterSavings == 0:
        waterSavingsLabel = Label(mainWndw, text = None)
    else:
        waterSavingsLabel = Label(mainWndw, text = f"equals {waterSavings} gallons of water saved")
    waterSavingsLabel.grid(row = wtrUsageRow, column = savingsColumn, sticky = 'w')
#
    if btuSavings == 0:
        btuSavingsLabel = Label(mainWndw, text = None)
    else:
        btuSavingsLabel = Label(mainWndw, text = f"equals {btuSavings:,} BTUs saved")
    btuSavingsLabel.grid(row = btuRow, column = savingsColumn, sticky = 'w')
#
    if kwhSavings == 0:
        kwhSavingsLabel = Label(mainWndw, text = None)
    else:
        kwhSavingsLabel = Label(mainWndw, text = f"equals {kwhSavings} kWhs saved")
    kwhSavingsLabel.grid(row = electricUsageRow, column = savingsColumn, sticky = 'w')
#
    if electricCostSavings == 0:
        electricCostSavingsLabel = Label(mainWndw, text = None)
    else:
        electricCostSavingsLabel = Label(mainWndw, text = f"equals ${electricCostSavings:.2f} saved")
    electricCostSavingsLabel.grid(row = electricCostRow, column = savingsColumn, sticky = 'w')
#
    if ccfSavings == 0:
        ccfSavingsLabel = Label(mainWndw, text = None)
    else:
        ccfSavingsLabel = Label(mainWndw, text = f"equals {ccfSavings} ccf saved")
    ccfSavingsLabel.grid(row = natgasUsageRow, column = savingsColumn, sticky = 'w')
#
    if gasCostSavings == 0:
        gasCostSavingsLabel = Label(mainWndw, text = None)
    else:
        gasCostSavingsLabel = Label(mainWndw, text = f"equals ${gasCostSavings:.2f} saved")
    gasCostSavingsLabel.grid(row = natgasCostRow, column = savingsColumn, sticky = 'w')
#
    if gallonsPropaneSavings == 0:
        propaneUsageSavingsLabel = Label(mainWndw, text = None)
    else:
        propaneUsageSavingsLabel = Label(mainWndw, text = f"equals {gallonsPropaneSavings} gallons saved")
    propaneUsageSavingsLabel.grid(row = propaneUsageRow, column = savingsColumn, sticky = 'w')
#
    if propaneCostSavings == 0:
        propaneCostSavingsLabel = Label(mainWndw, text = None)
    else:
        propaneCostSavingsLabel = Label(mainWndw, text = f"equals ${propaneCostSavings:.2f} saved")
    propaneCostSavingsLabel.grid(row = propaneCostRow, column = savingsColumn, sticky = 'w')
#
    if gallonsOilSavings == 0:
        oilUsageSavingsLabel = Label(mainWndw, text = None)
    else:
        oilUsageSavingsLabel = Label(mainWndw, text = f"equals {gallonsOilSavings} gallons saved")
    oilUsageSavingsLabel.grid(row = oilUsageRow, column = savingsColumn, sticky = 'w')
#
    if oilCostSavings == 0:
        oilCostSavingsLabel = Label(mainWndw, text = None)
    else:
        oilCostSavingsLabel = Label(mainWndw, text = f"equals ${oilCostSavings:.2f} saved")
    oilCostSavingsLabel.grid(row = oilCostRow, column = savingsColumn, sticky = 'w')
def debug():
#
# Send calculated quantities to console for debugging
    print(f"Original Temperature Difference: {orgTempDiff}")
    print(f"Original Water Usage:            {orgWtrUsage}")
    print(f"Original BTU:                    {orgBTU}\n")
    print(f"New Temperature Difference:      {newTempDiff}")
    print(f"New Water Usage:                 {newWtrUsage}")
    print(f"New BTU:                         {newBTU}\n")
    print(f"Water Savings:                   {waterSavings}")
    print(f"BTU Savings:                     {btuSavings}\n")

#
# Create a tkinter window
mainWndw = Tk()
mainWndw.title("Chipman Mills - Domestic Hot Water Savings Calculator")
#
# Utility Price Entry boxes
electricPriceEntry = Entry(mainWndw, width = 4)
electricPriceEntry.grid(row = electricUsageRow, column = fuelPriceColumn)
natgasPriceEntry = Entry(mainWndw, width = 4)
natgasPriceEntry.grid(row = natgasUsageRow, column = fuelPriceColumn)
propanePriceEntry = Entry(mainWndw, width = 4)
propanePriceEntry.grid(row = propaneUsageRow, column = fuelPriceColumn)
oilPriceEntry = Entry(mainWndw, width = 4)
oilPriceEntry.grid(row = oilUsageRow, column = fuelPriceColumn)
#
# Original Conditions Entry boxes
orgColdWtrTempEntry = Entry(mainWndw, width = 2)
orgColdWtrTempEntry.grid(row = coldWtrTempRow, column = orgCondxColumn, sticky = 'e')
orgHotWtrTempEntry = Entry(mainWndw, width = 3)
orgHotWtrTempEntry.grid(row = hotWtrTempRow, column = orgCondxColumn, sticky = 'e')
orgShwrHeadFlowRateEntry = Entry(mainWndw, width = 4)
orgShwrHeadFlowRateEntry.grid(row = shwrHeadFlowRateRow, column = orgCondxColumn, sticky = 'e')
orgShwrTimeEntry = Entry(mainWndw, width = 2)
orgShwrTimeEntry.grid(row = shwrTimeRow, column = orgCondxColumn, sticky = 'e')
orgCombEffEntry = Entry(mainWndw, width = 4)
orgCombEffEntry.grid(row = combEffRow, column = orgCondxColumn, sticky = 'e')
#
# New Conditions Entry boxes
newHotWtrTempEntry = Entry(mainWndw, width = 3)
newHotWtrTempEntry.grid(row = hotWtrTempRow, column = newCondxColumn, sticky = 'e')
newShwrHeadFlowRateEntry = Entry(mainWndw, width = 4)
newShwrHeadFlowRateEntry.grid(row = shwrHeadFlowRateRow, column = newCondxColumn, sticky = 'e')
newShwrTimeEntry = Entry(mainWndw, width = 2)
newShwrTimeEntry.grid(row = shwrTimeRow, column = newCondxColumn, sticky = 'e')
newCombEffEntry = Entry(mainWndw, width = 4)
newCombEffEntry.grid(row = combEffRow, column = newCondxColumn, sticky = 'e')

#                           0           1           2               3               4           5           6
initialQuantitiesList = [defaultCWT,defaultHWT,defaultFlowRate,defaultShwrTime,defaultEff,defaultHWT,defaultFlowRate,
                         defaultShwrTime,defaultEff,str(defaultPriceElectric),str(defaultPriceNatGas),str(defaultPricePropane),str(defaultPriceOil)]
#                               7           8                   9                   10                  11                      12

arrangeWndwGrid()
updateEntries(initialQuantitiesList)
#
updateResults()
#debug()

updateBtn = Button(mainWndw, text = "Update", command=updateResults)
updateBtn.grid(row = shwrHeadFlowRateRow, column = fuelsHdrColumn, columnspan = 3)

mainWndw.mainloop()
