# Domestic Hot Water Savings
## How much money and energy can you save by adjusting how much domestic hot water you use?

DHWSAVE.CBL --------- written in Enterprise COBOL v6.3 for z/OS & Unix

dhwsave.COB ---------- written in VSI COBOL for Open VMS

dhw_savings_calc.py --- written in Python3

## Output:
Domestic Hot Water Savings Calculator
Written by, Clifford A. Chipman, EMIT
February 2, 2021
in Python3 for z/OS

Water Temperature Limits: 33 - 79 degF
Enter cold water temperature (in degF): 65

1........Electric    @$0.13 per kWh
2........Natural Gas @$1.18 per ccf
3........Propane     @$2.66 per gallon
Enter initial fuel type: 1

Water Temperature Limits: 80 - 211 degF
Enter initial hot water temperature (in degF): 140

Flow Rate Limits: 1 - 2.5 GPM
Enter initial showerhead flow rate (in GPM): 2.5

Daily Shower Time Limits: 1 - 60 minutes
Enter initial total daily shower time (in minutes): 10

Combustion Efficiency Limits: 1 - 100 %
Enter initial combustion efficiency (in %): 98.1

1........Electric    @$0.13 per kWh
2........Natural Gas @$1.18 per ccf
3........Propane     @$2.66 per gallon
Enter new fuel type: 1

Water Temperature Limits: 80 - 211 degF
Enter new hot water temperature (in degF): 115

Flow Rate Limits: 1 - 2.5 GPM
Enter new showerhead flow rate (in GPM): 2.5

Daily Shower Time Limits: 1 - 60 minutes
Enter new total daily shower time (in minutes): 10

Combustion Efficiency Limits: 1 - 100 %
Enter new combustion efficiency (in %): 98.1

Cold Water Inlet Temperature: 65.0 degF

Initial Hot Water Temperature: 140.0 degF
Initial Flow Rate: 2.5 GPM
Initial Shower Time: 10.0 minutes
Initial Combustion Efficiency: 98.1%

Initial Water Consumption: 25.0 gallons
Initial Energy Consumption: 15921.3 BTUs
Initial Fuel Consumption: 4.6663 kWh
Initial Fuel Cost: $0.61 @$0.13 per kWh


New Hot Water Temperature: 115.0 degF
New Flow Rate: 2.5 GPM
New Shower Time: 10.0 minutes
New Combustion Efficiency: 98.1%

New Water Consumption: 25.0 gallons
New Energy Consumption: 10614.2 BTUs
New Fuel Consumption: 3.1108 kWh
New Fuel Cost: $0.40 @$0.13 per kWh

Water Saved: 0.0 gallons
Energy Saved: 5307.1 BTUs
Fuel Saved: 1.5554 kWh
Cost Saved: $0.20
