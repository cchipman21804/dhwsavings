      ************************************************************
      *
      * Domestic Hot Water Savings Calculator
      * Written by, Clifford A. Chipman, EMIT
      * February 24, 2021
      * in VSI COBOL
      *
      ************************************************************
      *
       identification division.
       program-id.    dhwsave.
       author.        Chipman.
      *
      ************************************************************
      *
       data division.
       working-storage section.
      *
       01 constant-data.
          02 units.
             03 temp-unit                    pic x(4)  value "degF".
             03 flow-unit                    pic x(3)  value "GPM".
             03 time-unit                    pic x(7)  value "minutes".
             03 comb-eff-unit                pic x     value "%".
             03 water-unit                   pic x(7)  value "gallons".
             03 energy-unit                  pic x(4)  value "BTUs".
      *
          02 fuel-type-menu-limits.
             03 min-menu                     pic 9     value zero.
             03 max-menu                     pic 9     value 3.
      *
          02 water-temperature-limits.
             03 lower-cwt                    pic 99    value 33.
             03 upper-cwt                    pic 99    value 79.
             03 lower-hwt                    pic 99    value 80.
             03 upper-hwt                    pic 999   value 211.
      *
          02 flow-rate-limits.
             03 min-flow-rate                pic 9     value 1.
             03 max-flow-rate                pic 9v9   value 2.5.
      *
          02 time-limits.
             03 min-time                     pic 9     value 1.
             03 max-time                     pic 99    value 60.
      *
          02 combustion-eff-limits.
             03 min-eff                      pic 9     value 1.
             03 max-eff                      pic 999   value 100.
      *
          02 fuel-units.
             03 electric-unit                pic xxx   value "kWh".
             03 natgas-unit                  pic xxx   value "ccf".
             03 propane-unit                 pic x(7)  value "gallons".
      *
          02 fuel-unit-prices.
             03 electric-price               pic 9v99  value 0.13.
             03 natgas-price                 pic 9v99  value 1.18.
             03 propane-price                pic 9v99  value 2.66.
      *
          02 conversion-factors.
             03 btu-kwh                      pic 9(4)  value 3412.
      * DIVIDE BTUS BY 3412 GIVING KWH
      *
             03 btu-ccf                      pic 9(6)  value 103700.
      * DIVIDE BTUS BY 103700 GIVING CCF
      *
             03 btu-gallons                  pic 9(5)  value 91452.
      * DIVIDE BTUS BY 91452 GIVING GALLONS OF PROPANE
      *
          02 data-entry-label-constants.
             03 too-low                      pic x(12)
             value " is too low.".
      *
             03 too-high                     pic x(13)
             value " is too high.".
      *
      **************************************************************
      *
      * initial / new data entry prompt:
       01 which-one                          pic x(9).
      *
       01 init-condx                         pic x(9)
                                             value " initial ".
      *
       01 new-condx                          pic x(9)
                                             value "   new   ".
      *
      **************************************************************
      *
      * NUMERIC DATA ENTRY FIELDS FOR INITIAL VALUES:
      *
       01 cold-water-temp                    pic 99.
      *                                      in degF
       01 init-conditions.
      *
          02 init-fuel                       pic 9.
      * ELECTRICITY, NATURAL GAS, OR PROPANE
      * 1            2               3
      *
          02 init-fuel-price                 pic 9v99.
      *                                      in $
      *
          02 init-conv-unit                  pic 9(6).
          02 init-fuel-unit                  pic x(7).
          02 init-fuel-cost                  pic 99v99.
          02 init-fuel-consumed              pic 99v999.
      *
          02 init-dhw-temp                   pic 999.
      *                                      in degF
      *
          02 init-flow-rate                  pic 9v99.
      *                                      in GPM
      *
          02 init-shower-time                pic 99.
      *                                      in minutes
      *
          02 init-comb-eff                   pic 999v9.
      * APPLIANCE FUEL COMBUSTION EFFICIENCY IN %
      *
      **************************************************************
      *
      * CALCULATED INITIAL VALUES
      *
          02 init-usage                      pic 999v99.
      * WATER CONSUMPTION                    in gallons
      *
          02 init-energy                     pic 9(6)v99.
      * ENERGY CONSUMPTION                   in BTUs
      *
      **************************************************************
      *
      * NUMERIC DATA ENTRY FIELDS FOR NEW VALUES
      *
       01 new-conditions.
      *
          02 new-fuel                        pic 9.
      * ELECTRICITY, NATURAL GAS, OR PROPANE
      * 1            2               3
      *
          02 new-fuel-price                  pic 9v99.
      *                                      in $
      *
          02 new-conv-unit                   pic 9(6).
          02 new-fuel-unit                   pic x(7).
          02 new-fuel-cost                   pic 99v99.
          02 new-fuel-consumed               pic 99v999.
      *
          02 new-dhw-temp                    pic 999.
      *                                      in degF
      *
          02 new-flow-rate                   pic 9v99.
      *                                      in GPM
      *
          02 new-shower-time                 pic 99.
      *                                      in minutes
      *
          02 new-comb-eff                    pic 999v9.
      * APPLIANCE FUEL COMBUSTION EFFICIENCY IN %
      *
      **************************************************************
      *
      * CALCULATED NEW VALUES
      *
          02 new-usage                       pic 999v99.
      * WATER CONSUMPTION                    in gallons
      *
          02 new-energy                      pic 9(6)v99.
      * ENERGY CONSUMPTION                   in BTUs
      *
      **************************************************************
      *
      * CALCULATED SAVINGS
      *
       01 water-saved                        pic s9(3)v99
                                             sign is leading separate.
      *                                      in gallons
      *
       01 energy-saved                       pic s9(6)v99
                                             sign is leading separate.
      *                                      in BTUs
      *
       01 fuel-saved                         pic s999v99
                                             sign is leading separate.
      *
       01 cost-saved                         pic s99v99
                                             sign is leading separate.
      *
      **************************************************************
      *
       01 displayed-report-fields.
          02 min-flow-rate-out               pic 9.99.
          02 max-flow-rate-out               pic 9.99.
          02 cold-water-temp-out             pic z9.
          02 init-dhw-temp-out               pic zz9.
          02 init-flow-rate-out              pic 9.99.
          02 init-shower-time-out            pic z9.
          02 init-comb-eff-out               pic zz9.9.
          02 init-usage-out                  pic zz9.9.
          02 init-energy-out                 pic zzz,zz9.9.
          02 init-fuel-consumed-out          pic zz9.999.
          02 init-fuel-cost-out              pic $$9.99.
          02 new-dhw-temp-out                pic zz9.
          02 new-flow-rate-out               pic 9.99.
          02 new-shower-time-out             pic z9.
          02 new-comb-eff-out                pic zz9.9.
          02 new-usage-out                   pic zz9.9.
          02 new-energy-out                  pic zzz,zz9.9.
          02 new-fuel-consumed-out           pic zz9.999.
          02 new-fuel-cost-out               pic $$9.99.
          02 water-saved-out                 pic +zz9.9.
          02 energy-saved-out                pic +zzz,zz9.9.
          02 fuel-saved-out                  pic +zz9.9.
          02 cost-saved-out                  pic +$$9.99.
          02 price-out                       pic $9.99.
      *
      **************************************************************
      *
      * Screen locations of data entry prompts
      *
       01 cwt-prompt.
          02 cwt-line                        pic 99    value 11.
          02 cwt-col                         pic 99    value 32.
      *
       01 fuel-menu.
          02 fmp-col                         pic 99    value 23.
      *
       01 fuel-prompt.
          02 ifp-line                        pic 99    value 16.
          02 ifp-col                         pic 999   value 20.
      *
       01 dhw-temp-prompt.
          02 idhwt-line                      pic 99    value 18.
          02 idhwt-col                       pic 999   value 39.
      *
       01 flow-rate-prompt.
          02 ifr-line                        pic 99    value 19.
          02 ifr-col                         pic 999   value 27.
      *
       01 shower-time-prompt.
          02 ist-line                        pic 99    value 20.
          02 ist-col                         pic 999   value 29.
      *
       01 comb-eff-prompt.
          02 ice-line                        pic 99    value 21.
          02 ice-col                         pic 999   value 39.
      *
      **************************************************************
      *
      * Screen locations of report data points
      *
       01 cwt-rpt.
          02 cwt-rpt-line                    pic 99    value 11.
          02 cwt-rpt-col                     pic 999   value 32.
      *
       01 init-dhw-temp-rpt.
          02 idhwt-rpt-line                  pic 99    value 13.
          02 idhwt-rpt-col                   pic 999   value 32.
      *
       01 init-flow-rate-rpt.
          02 ifr-rpt-line                    pic 99    value 14.
          02 ifr-rpt-col                     pic 999   value 34.
      *
       01 init-shower-time-rpt.
          02 ist-rpt-line                    pic 99    value 15.
          02 ist-rpt-col                     pic 999   value 33.
      *
       01 init-comb-eff-rpt.
          02 ice-rpt-line                    pic 99    value 16.
          02 ice-rpt-col                     pic 999   value 32.
      *
       01 init-water-usage-rpt.
          02 iwu-rpt-line                    pic 99    value 17.
          02 iwu-rpt-col                     pic 999   value 32.
      *
       01 init-energy-usage-rpt.
          02 ieu-rpt-line                    pic 99    value 18.
          02 ieu-rpt-col                     pic 999   value 32.
      *
       01 init-fuel-consumed-rpt.
          02 ifc-rpt-line                    pic 99    value 19.
          02 ifc-rpt-col                     pic 999   value 32.
      *
       01 init-fuel-dollars-rpt.
          02 ifd-rpt-line                    pic 99    value 20.
          02 ifd-rpt-col                     pic 999   value 32.
      *
       01 new-dhw-temp-rpt.
          02 ndhwt-rpt-line                  pic 99    value 22.
          02 ndhwt-rpt-col                   pic 999   value 32.
      *
       01 new-flow-rate-rpt.
          02 nfr-rpt-line                    pic 99    value 23.
          02 nfr-rpt-col                     pic 999   value 34.
      *
       01 new-shower-time-rpt.
          02 nst-rpt-line                    pic 99    value 24.
          02 nst-rpt-col                     pic 999   value 33.
      *
       01 new-comb-eff-rpt.
          02 nce-rpt-line                    pic 99    value 25.
          02 nce-rpt-col                     pic 999   value 32.
      *
       01 new-water-usage-rpt.
          02 nwu-rpt-line                    pic 99    value 26.
          02 nwu-rpt-col                     pic 999   value 32.
      *
       01 new-energy-usage-rpt.
          02 neu-rpt-line                    pic 99    value 27.
          02 neu-rpt-col                     pic 999   value 32.
      *
       01 new-fuel-consumed-rpt.
          02 nfc-rpt-line                    pic 99    value 28.
          02 nfc-rpt-col                     pic 999   value 32.
      *
       01 new-fuel-dollars-rpt.
          02 nfd-rpt-line                    pic 99    value 29.
          02 nfd-rpt-col                     pic 999   value 32.
      *
       01 water-saved-rpt.
          02 ws-rpt-line                     pic 99    value 31.
          02 ws-rpt-col                      pic 999   value 16.
      *
       01 energy-saved-rpt.
          02 es-rpt-line                     pic 99    value 32.
          02 es-rpt-col                      pic 999   value 17.
      *
       01 fuel-saved-rpt.
          02 fs-rpt-line                     pic 99    value 33.
          02 fs-rpt-col                      pic 999   value 15.
      *
       01 cost-saved-rpt.
          02 cs-rpt-line                     pic 99    value 34.
          02 cs-rpt-col                      pic 999   value 15.
      *
      ******************************************************************
      *
       procedure division.
       main-para.
           perform opening-screen
           perform 1-init-conditions
           perform 11-cw-temp thru 16-init-comb-eff
      *
           perform opening-screen
           perform 2-new-conditions
           perform 21-new-fuel thru 25-new-comb-eff
      *
           perform 3-calc-init-report
           perform 4-calc-new-report
           perform 5-calc-savings
      *
           perform opening-screen
           perform 6-report-screen
           perform 999-end-program.
      *
       opening-screen.
           display "* * * * * * * * * * * * * * * * * * * * * * * * * *"
                   bold 
                   line 1 column 1 
                   erase screen
           display space
           display "*                                                 *"
                   bold
           display "*      Domestic Hot Water Savings Calculator      *" 
                   bold
           display "*                                                 *"
                   bold
           display "* * * * * * * * * * * * * * * * * * * * * * * * * *"
                   bold.
      *
       1-init-conditions.
           display "*                                                 *"
                   bold
           display "*              Initial  Conditions                *"
                   bold
           display "*                                                 *"
                   bold
           display "* * * * * * * * * * * * * * * * * * * * * * * * * *"
                   bold
      *
      * Cold water temperature prompt
      *
           display "Enter cold water temperature ("
                   line cwt-line
           display lower-cwt bold
                   line plus 0 column cwt-col
           display " - " bold
                   line plus 0 column plus 
           display upper-cwt bold
                   line plus 0 column plus 
           display ") in degF:"
                   line plus 0 column plus
      *
      * Initial fuel type prompt
      *
           perform 998-fuel-menu
           display "Initial fuel type:"
                   line plus.
      *
           move init-condx to which-one
           perform 997-data-entry-prompts.
      *
       2-new-conditions.
           display "*                                                 *"
                   bold
           display "*              New      Conditions                *"
                   bold
           display "*                                                 *"
                   bold
           display "* * * * * * * * * * * * * * * * * * * * * * * * * *"
                   bold
      *
      * New fuel type prompt
      *
           display spaces
           perform 998-fuel-menu
           display "    New fuel type:"
                   line plus.
      *
           move new-condx to which-one
           perform 997-data-entry-prompts.
      *
      *********************************************************************
      *
      * I N I T I A L   D A T A   E N T R Y
      *
      *********************************************************************
      *
      * The constant added to the column variables depends on the length
      * of the string prompts for each data entry variable
      *
       11-cw-temp.
           accept cold-water-temp
                  reversed 
                  line cwt-line column cwt-col plus 21
                  protected with conversion
      *                      
           evaluate true
               when cold-water-temp is equal ZERO go to 999-end-program

               when cold-water-temp is less than lower-cwt or
                    cold-water-temp is greater than upper-cwt
                    go to 11-cw-temp
           end-evaluate
           move cold-water-temp to cold-water-temp-out.
      *
       12-init-fuel.
           accept init-fuel 
                  reversed
                  line ifp-line column ifp-col
                  protected with conversion
      *        
           evaluate true
               when init-fuel is equal ZERO go to 999-end-program
           
               when init-fuel is less than min-menu or
                    init-fuel is greater than max-menu 
                    go to 12-init-fuel

               when init-fuel = 1
                    move electric-unit  to init-fuel-unit
                    move electric-price to init-fuel-price
                    move btu-kwh        to init-conv-unit

               when init-fuel = 2
                    move natgas-unit    to init-fuel-unit
                    move natgas-price   to init-fuel-price
                    move btu-ccf        to init-conv-unit

               when init-fuel = 3
                    move propane-unit   to init-fuel-unit
                    move propane-price  to init-fuel-price
                    move btu-gallons    to init-conv-unit
           end-evaluate.
      *
       13-init-hw-temp.
           accept init-dhw-temp
                  reversed 
                  line idhwt-line column idhwt-col plus 22
                  protected with conversion
      *                
           evaluate true
               when init-dhw-temp is equal ZERO go to 999-end-program

               when init-dhw-temp is less than lower-hwt or
                    init-dhw-temp is greater than upper-hwt
                    go to 13-init-hw-temp
           end-evaluate
           move init-dhw-temp to init-dhw-temp-out.
      *
       14-init-flow-rate.
           accept init-flow-rate
                  reversed
                  line ifr-line column ifr-col plus 24
                  protected with conversion
      *
           evaluate true
               when init-flow-rate is equal ZERO
                    go to 999-end-program

               when init-flow-rate is less than min-flow-rate or
                    init-flow-rate is greater than max-flow-rate
                    go to 14-init-flow-rate
           end-evaluate
           move init-flow-rate to init-flow-rate-out.
      *
       15-init-shower-time.
           accept init-shower-time
                  reversed
                  line ist-line column ist-col plus 23
                  protected with conversion
      *
           evaluate true
               when init-shower-time is equal ZERO
                    go to 999-end-program

               when init-shower-time is less than min-time or
                    init-shower-time is greater than max-time
                    go to 15-init-shower-time
           end-evaluate
           move init-shower-time to init-shower-time-out.
      *
       16-init-comb-eff.
           accept init-comb-eff
                  reversed
                  line ice-line column ice-col plus 18
                  protected with conversion
      *            
           evaluate true
               when init-comb-eff is equal ZERO
                    go to 999-end-program

               when init-comb-eff is less than min-eff or
                    init-comb-eff is greater than max-eff
                    go to 16-init-comb-eff
           end-evaluate
           move init-comb-eff to init-comb-eff-out.
      *
      *********************************************************************
      *
      * N E W   D A T A   E N T R Y
      *
      *********************************************************************
      *
       21-new-fuel.
           accept new-fuel 
                  reversed
                  line ifp-line column ifp-col
                  protected with conversion
      *        
           evaluate true
               when new-fuel is equal ZERO go to 999-end-program
           
               when new-fuel is less than min-menu or
                    new-fuel is greater than max-menu 
                    go to 21-new-fuel

               when new-fuel = 1
                    move electric-unit  to new-fuel-unit
                    move electric-price to new-fuel-price
                    move btu-kwh        to new-conv-unit

               when new-fuel = 2
                    move natgas-unit    to new-fuel-unit
                    move natgas-price   to new-fuel-price
                    move btu-ccf        to new-conv-unit

               when new-fuel = 3
                    move propane-unit   to new-fuel-unit
                    move propane-price  to new-fuel-price
                    move btu-gallons    to new-conv-unit
           end-evaluate.
      *
       22-new-hw-temp.
           accept new-dhw-temp
                  reversed 
                  line idhwt-line column idhwt-col plus 22
                  protected with conversion
      *                     
           evaluate true
               when new-dhw-temp is equal ZERO go to 999-end-program

               when new-dhw-temp is less than lower-hwt or
                    new-dhw-temp is greater than upper-hwt
                    go to 22-new-hw-temp
           end-evaluate
           move new-dhw-temp to new-dhw-temp-out.
      *
       23-new-flow-rate.
           accept new-flow-rate
                  reversed
                  line ifr-line column ifr-col plus 24
                  protected with conversion
      *          
           evaluate true
               when new-flow-rate is equal ZERO
                    go to 999-end-program

               when new-flow-rate is less than min-flow-rate or
                    new-flow-rate is greater than max-flow-rate
                    go to 23-new-flow-rate
           end-evaluate
           move new-flow-rate to new-flow-rate-out.
      *
       24-new-shower-time.
           accept new-shower-time
                  reversed
                  line ist-line column ist-col plus 23
                  protected with conversion
      *          
           evaluate true
               when new-shower-time is equal ZERO
                    go to 999-end-program

               when new-shower-time is less than min-time or
                    new-shower-time is greater than max-time
                    go to 24-new-shower-time
           end-evaluate
           move new-shower-time to new-shower-time-out.
      *
       25-new-comb-eff.
           accept new-comb-eff
                  reversed
                  line ice-line column ice-col plus 18
                  protected with conversion
      *        
           evaluate true
               when new-comb-eff is equal ZERO
                    go to 999-end-program

               when new-comb-eff is less than min-eff or
                    new-comb-eff is greater than max-eff
                    go to 25-new-comb-eff
           end-evaluate
           move new-comb-eff to new-comb-eff-out.
      *
      *********************************************************************
      *
      * C A L C U L A T E   I N I T I A L   R E P O R T
      *
      *********************************************************************
      *
       3-calc-init-report.
      *
      * Calculate initial water usage
      *
           multiply init-flow-rate by init-shower-time
                    giving init-usage rounded
           move init-usage to init-usage-out
      *
      * Calculate initial energy consumption
      *
           divide 100 into init-comb-eff
           compute init-energy rounded = 8.33 * init-usage * 
                   (init-dhw-temp - cold-water-temp) / init-comb-eff
           move init-energy to init-energy-out
      *
      * Calculate initial fuel consumption
      *
           divide init-energy by init-conv-unit
                  giving init-fuel-consumed rounded
           move init-fuel-consumed to init-fuel-consumed-out
      *
      * Calculate initial fuel cost
      *
           multiply init-fuel-consumed by init-fuel-price
                    giving init-fuel-cost rounded
           move init-fuel-cost to init-fuel-cost-out.
      *
      *********************************************************************
      *
      * C A L C U L A T E   N E W   R E P O R T
      *
      *********************************************************************
      *
       4-calc-new-report.
      *
      * Calculate new water usage
      *
           multiply new-flow-rate by new-shower-time
                    giving new-usage rounded
           move new-usage to new-usage-out
      *
      * Calculate new energy consumption
      *
           divide 100 into new-comb-eff
           compute new-energy rounded = 8.33 * new-usage * 
                   (new-dhw-temp - cold-water-temp) / new-comb-eff
           move new-energy to new-energy-out
      *
      * Calculate new fuel consumption
      *
           divide new-energy by new-conv-unit
                  giving new-fuel-consumed rounded
           move new-fuel-consumed to new-fuel-consumed-out
      *
      * Calculate new fuel cost
      *
           multiply new-fuel-consumed by new-fuel-price
                    giving new-fuel-cost rounded
           move new-fuel-cost to new-fuel-cost-out.
      *
      *********************************************************************
      *
      * C A L C U L A T E   S A V I N G S
      *
      *********************************************************************
      *
       5-calc-savings.
      * Calculate water saved
           subtract new-usage from init-usage
                    giving water-saved rounded
           move water-saved to water-saved-out
      *
      * Calculate energy saved
           subtract new-energy from init-energy
                    giving energy-saved rounded
           move energy-saved to energy-saved-out
      *
      * If initial fuel same as new fuel then
      *    calculate fuel savings
           if init-fuel is equal to new-fuel then
              subtract new-fuel-consumed from init-fuel-consumed
                       giving fuel-saved rounded
              move fuel-saved to fuel-saved-out
           end-if
      *
      * Calculate cost savings
           subtract new-fuel-cost from init-fuel-cost
                    giving cost-saved rounded
           move cost-saved to cost-saved-out.
      *
      *********************************************************************
      *
      * R E P O R T   S C R E E N
      *
      *********************************************************************
      *
       6-report-screen.
           display "*                                                 *"
                   bold
           display "*                     Report                      *"
                   bold
           display "*                                                 *"
                   bold
           display "* * * * * * * * * * * * * * * * * * * * * * * * * *"
                   bold
      *
      *********************************************************************
      *
      * I N I T I A L   C O N D I T I O N S   R E P O R T
      *
      *********************************************************************
      *
      * Initial Conditions Report
      * 
           display "Cold Water Temperature       : " bold
                   line cwt-rpt-line column 1
           display cold-water-temp-out line plus 0 column cwt-rpt-col
           display temp-unit line plus 0 column plus
      *
           display "Initial Hot Water Temperature: " bold
                   line idhwt-rpt-line column 1
           display init-dhw-temp-out line plus 0 column idhwt-rpt-col
           display temp-unit line plus 0 column plus
      *
           display "        Flow Rate            : " bold
                   line ifr-rpt-line column 1
           display init-flow-rate-out line plus 0 column ifr-rpt-col
           display flow-unit line plus 0 column plus
      *
           display "        Shower Time          : " bold
                   line ist-rpt-line column 1
           display init-shower-time-out line plus 0 column ist-rpt-col
           display time-unit line plus 0 column plus
      *            
           display "        Combustion Efficiency: " bold
                   line ice-rpt-line column 1
           display init-comb-eff-out line plus 0 column ice-rpt-col
           display comb-eff-unit line plus 0 column plus
      *              
           display "        Water Usage          : " bold
                   line iwu-rpt-line column 1
           display init-usage-out line plus 0 column iwu-rpt-col
           display water-unit line plus 0 column plus
      *                
           display "        Energy Consumption   : " bold
                   line ieu-rpt-line column 1
           display init-energy-out line plus 0 column ieu-rpt-col
           display energy-unit line plus 0 column plus
      *                
           display "        Fuel Consumption     : " bold
                   line ifc-rpt-line column 1
           display init-fuel-consumed-out line plus 0 column ifc-rpt-col
           display init-fuel-unit line plus 0 column plus
      *         
           display "        Fuel Cost            : " bold
                   line ifd-rpt-line column 1
           display init-fuel-cost-out line plus 0 column ifd-rpt-col
           move init-fuel-price to price-out
           display "@" line plus 0 column plus 
           display price-out " per" init-fuel-unit
                   line plus 0 column plus.
      *
      *********************************************************************
      *
      * N E W   C O N D I T I O N S   R E P O R T
      *
      *********************************************************************
      *
      * New Conditions Report
      *
           display "    New Hot Water Temperature: " bold
                   line ndhwt-rpt-line column 1
           display new-dhw-temp-out line plus 0 column ndhwt-rpt-col
           display temp-unit line plus 0 column plus
      *
           display "        Flow Rate            : " bold
                   line nfr-rpt-line column 1
           display new-flow-rate-out line plus 0 column nfr-rpt-col
           display flow-unit line plus 0 column plus
      *
           display "        Shower Time          : " bold
                   line nst-rpt-line column 1
           display new-shower-time-out line plus 0 column nst-rpt-col
           display time-unit line plus 0 column plus
      *            
           display "        Combustion Efficiency: " bold
                   line nce-rpt-line column 1
           display new-comb-eff-out line plus 0 column nce-rpt-col
           display comb-eff-unit line plus 0 column plus
      *              
           display "        Water Usage          : " bold
                   line nwu-rpt-line column 1
           display new-usage-out line plus 0 column nwu-rpt-col
           display water-unit line plus 0 column plus
      *                
           display "        Energy Consumption   : " bold
                   line neu-rpt-line column 1
           display new-energy-out line plus 0 column neu-rpt-col
           display energy-unit line plus 0 column plus
      *                
           display "        Fuel Consumption     : " bold
                   line nfc-rpt-line column 1
           display new-fuel-consumed-out line plus 0 column nfc-rpt-col
           display new-fuel-unit line plus 0 column plus
      *         
           display "        Fuel Cost            : " bold
                   line nfd-rpt-line column 1
           display new-fuel-cost-out line plus 0 column nfd-rpt-col
           move new-fuel-price to price-out
           display "@" line plus 0 column plus
           display price-out " per" new-fuel-unit
                   line plus 0 column plus.
      *
      *********************************************************************
      *
      * S A V I N G S   R E P O R T
      *
      *********************************************************************
      *
      * Savings Report
      *
           display "Water Savings: " bold
                   line ws-rpt-line column 1
           display water-saved-out
                   line plus 0 column ws-rpt-col
           display water-unit
                   line plus 0 column plus
      *
           display "Energy Savings: " bold
                   line es-rpt-line column 1
           display energy-saved-out
                   line plus 0 column es-rpt-col
           display energy-unit
                   line plus 0 column plus
      *
           display "Fuel Savings: " bold
                   line fs-rpt-line column 1
      *
           if init-fuel is equal to new-fuel then
              display fuel-saved-out line plus 0 column fs-rpt-col
              display init-fuel-unit line plus 0 column plus
           else 
              display "N/A" line plus 0 column fs-rpt-col
           end-if
      *
           display "Cost Savings: " bold
                   line cs-rpt-line column 1
           display cost-saved-out
                   line plus 0 column cs-rpt-col.
      *
      *********************************************************************
      *
      * D A T A   E N T R Y   P R O M P T S
      *
      *********************************************************************
      *
       997-data-entry-prompts.
      *
      * Hot water temperature prompt
      *
           display "Enter" line idhwt-line 
           display which-one "hot water temperature ("                  
           display lower-hwt bold
                   line idhwt-line column idhwt-col
           display " - " bold
                   line plus 0 column plus 
           display upper-hwt bold
                   line plus 0 column plus 
           display ") in degF:"
                   line plus 0 column plus
      *
      * Flow rate prompt
      *
      *    move flow rate limits to separate display
      *    variables for data entry screen
      *
           move min-flow-rate to min-flow-rate-out
           move max-flow-rate to max-flow-rate-out
      *
           display "Enter" line ifr-line
           display which-one "flow rate ("
           display min-flow-rate-out bold
                   line ifr-line column ifr-col
           display " - " bold
                   line plus 0 column plus
           display max-flow-rate-out bold
                   line plus 0 column plus
           display ") in GPM:"
                   line plus 0 column plus
      *
      * Shower time prompt
      *
           display "Enter" line ist-line
           display which-one "shower time ("
           display min-time bold
                   line ist-line column ist-col
           display " - " bold
                   line plus 0 column plus
           display max-time bold
                   line plus 0 column plus
           display ") in minutes:"
                   line plus 0 column plus
      *
      * Combustion efficiency prompt
      *
           display "Enter" line ice-line
           display which-one "combustion efficiency ("
           display min-eff bold
                   line ice-line column ice-col
           display " - " bold
                   line plus 0 column plus
           display max-eff bold
                   line plus 0 column plus
           display ") in %:"
                   line plus 0 column plus.
      *
      *********************************************************************
      *
      * F U E L   M E N U
      *
      *********************************************************************
      *
       998-fuel-menu.
           move electric-price to price-out
           display "[1]" bold line plus 2 column 2
           display "--- Electric" line plus 0 column plus
           display "@" line plus 0 column fmp-col
           display price-out " per" electric-unit
                   line plus 0 column plus 1
      *
           move natgas-price to price-out
           display "[2]" bold line plus column 2
           display "--- Natural Gas" line plus 0 column plus
           display "@" line plus 0 column fmp-col
           display price-out " per" natgas-unit
                   line plus 0 column plus 1
      *
           move propane-price to price-out
           display "[3]" bold line plus column 2
           display "--- Propane" line plus 0 column plus
           display "@" line plus 0 column fmp-col
           display price-out " per" propane-unit
                   line plus 0 column plus 1
      *
      * Make propane unit singular by placing a space over the trailing s
      * Column number may need to be changed if menu display formatting is
      * changed
      *
           display space line plus 0 column 40.
      *
      *********************************************************************
      *
      * E N D   P R O G R A M
      *
      *********************************************************************
      *
       999-end-program.
           display spaces line plus column 1
           stop run.
