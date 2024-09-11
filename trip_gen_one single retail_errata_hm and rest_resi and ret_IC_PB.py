# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 16:21:37 2024

@author: Wang Xi
"""


# Title: Trip Generation - one single retail - errata - interaction btw retail and restaurant, residential and retail
# Author: Wang Xi
# Contact: wangxi@trebilcock.biz
# Last Update Date: 08-13-2024
# Required File Format: .py, .csv file, .xlsx file
# Ctrl + 4 for multiple lines comment out, Ctrl + 5 for uncomment
# Shift + Enter will go to the next line (line break)
# A tuple (round parenthesis) is like a list (square brackets), except it is immutable (i.e., you cannot change any part of it after it exists.)
# Update Notes: 
    # (1) Wkd IC is the average of AM and PM Peak Hour's IC rate;
    # (2) Input "Yes or No" can be lower case or upper case;
    # (3) Wkd PB is 10% less than AM/PM PB, i.e., 15% for wkd, 25% for AM and PM;
        # Per Collier County Traffic Impact Study Guidelines and Procedures (Lee County also applies), the pass-by capture is reduced as follows: 
          # - 25% AM and PM peak hour for Strip Retail Plaza  
          # - 50% AM and PM peak hour for Fast Food Restaurant with Drive-Thru   
          # - 40% AM and PM peak hour for High Turnover (Sit-Down) Restaurant and Fine Dining Restaurant
        # For other land uses, type in the specific perc when asked
    # (4) The criteria to use eqn. or avg. will follow Page 26 of ITE Trip Generation Handbook 3rd Edition. 
        # On the other hand, according to FDOT, if the development parameter is out of the ITE study range, use avg. instead of eqn.;
        # Lastly, residential must use eqn. if provided
    # (5) Pass-by trips = PB rate * external trips
    # (6) IC and PB are taken as integer from the floating point (decimal) number, to make external trips or net external trips higher from the conservative consideration.
    # (7) Collier County has a maximum IC limit of 20% (PM/AM/Wkd) and Lee County (includes Estero) IC: not to exceed 30% of the total traffic. If IC exceeds this threshold, it need to be adjusted. 
    # (8) Errata - for residential land uses
    # (9) Add-up directional distribution perc as an additional row right after the total traffic
    # (10) Provide the specific eqn/avg instead of text "eqn"/"avg"
    # (11) Create LUC and unique ratio rate for basketball and volleyball court
    # (12) For AM peak hour, when IC is less than 1 trip, math.ceil () is applied to make it round up to 1 trip, to present there is IC in the AM peak hour;
    # (13) In order to get the highest net external trips as much as possible (being conservative), AM-PM IC and AM-PM PB trips are applied only taking integer (round-down).
    # (14) Provide a table to show how we select Internal Capture Trip as IC
    # (15) LUC 491 doesn't provide any AM Peak Hour info or directional dist perc for PM Peak Hour, therefore, 50%/50% is applied for both AM and PM; and AM Peak Hour follows the PM Peak Hour's average rate.
    # (16) Customize the IC for golf course and tennis club.
    # (17) When the daily or AM Peak Hour trips are negative using eqn., switch from eqn. to avg rate.
 
   
# Example: How to calculate the overall IC and PB percentage
# +--------------------+-------------+---------------+-------------+
# |       Trips        |  PM Entry   |    PM Exit    |   PM Total  |
# +--------------------+-------------+---------------+-------------+
# |    Total Trips     |     60      |      107      |     167     |
# +--------------------+-------------+---------------+-------------+
# |  Internal Capture  |      5      |        5      |      10     |
# +--------------------+-------------+---------------+-------------+
# |   External Trips   |     55      |      102      |     157     |
# +--------------------+-------------+---------------+-------------+
# |  Pass-by Capture   |     11      |       12      |      23     |
# +--------------------+-------------+---------------+-------------+
# | Net External Trips |     44      |       90      |     134     |
# +--------------------+-------------+---------------+-------------+
# | IC rate = Total IC / Total Trips | (5 + 5) / (60 + 107) = 10/167 = 5.988%
# +----------------+--------------+------------------+-------------+-----------+
# | PB rate = Total PB / Total External Trips | (11 + 12) / (55 + 102) = 23/157 = 14.650%
# +----------------+--------------+------------------+-------------+---------------------+
# | Note: only calculate daily total, AM total and PM total's overall IC percent and overall PB percent (regardless of enter & exit)
# +----------------+--------------+------------------+-------------+---------------------+-----------------------------------------+



# Import modules
import os
import pandas as pd
import numpy as np
from datetime import datetime
import math

# Set working directory
os.chdir(r'C:\Users\Wang Xi\Desktop\Wang Xi\Python projects') # instead of r before the quote, we can also use '\\' double backslashes or forward slash '/'.
os.getcwd()

# Create a dataframe
n = int(input("How many land uses are there in the project? "))
land_use = []
measurement = []
LU = []
units = []
Weekdays = []
AM = []
PM = []
trips =[]
tot_wkd_trips = []
wkd_enters = []
wkd_exits = []
tot_AM_trips = []
AM_enters = []
AM_exits = []
tot_PM_trips = []
PM_enters = []
PM_exits = []
AM_enters_dir = []
AM_exits_dir = []
PM_enters_dir = []
PM_exits_dir = []
LU_in_residential = []
LU_in_retail = []
LU_in_restaurant = []
LU_in_hotel = []

# Assign the lists
retail_list = ['816', '820', '821', '822']
residential_list = ['210', '215', '220', '221', '222', '251', '260']
restaurant_list = ['931', '932', '933', '934']
office_list = ['710', '712']
hotel_list = ['310']
other_list = ['842', '420', '430', '488', '490', '491', '498', '499'] # LUC488-Soccer, LUC490-Tennis, LUC491-Racquet/Pickleball/handball/squash
# LUC498 - created for basketball (2.5*tennis ratio), LUC499 - created for volleyball (3.0*tennis ratio)

# Loop over the land uses
for i in range (n):
    LUi = input("What is your ITE LU#? ")
    unit = input("How many units do you have? ")
    if LUi == "210":
        land_use_i = "Single-Family Detached Housing"
        measurement_i = 'Dwelling Units'
        tot_wkd_trips_i = round(np.exp(0.92 * np.log(float(unit)) + 2.68)) # fitted curve equation
        wkd_enters_i = round(float (tot_wkd_trips_i) * 0.5)
        wkd_exits_i = round(tot_wkd_trips_i - wkd_enters_i)
        tot_AM_trips_i = round(np.exp(0.91 * np.log(float(unit)) + 0.12)) # fitted curve equation
        AM_enters_i = round(float (tot_AM_trips_i) * 0.25)
        AM_exits_i = round(float (tot_AM_trips_i) * 0.75)
        tot_PM_trips_i = round(np.exp(0.94 * np.log(float(unit)) + 0.27)) # fitted curve equation
        PM_enters_i = round(float (tot_PM_trips_i) * 0.63)
        PM_exits_i = round(float (tot_PM_trips_i) * 0.37)
        AM_enters_dir_i = '25%'
        AM_exits_dir_i = '75%'
        PM_enters_dir_i = '63%'
        PM_exits_dir_i = '37%'
        weekday_i = 'Ln (T) = 0.92 Ln (X) + 2.68' 
        AMi = 'Ln (T) = 0.91 Ln (X) + 0.12'
        PMi = 'Ln (T) = 0.94 Ln (X) + 0.27'
        tripi = 'Total'
        LUi_in_residential = LUi if LUi in residential_list else None
        LUi_in_retail = LUi if LUi in retail_list else None
        LUi_in_restaurant = LUi if LUi in restaurant_list else None
        LUi_in_hotel = LUi if LUi in hotel_list else None
        
    elif LUi == "215":
        land_use_i = "Single-Family Attached Housing"
        measurement_i = 'Dwelling Units'
        tot_wkd_trips_i = round(7.62 * float(unit) - 50.48) # fitted curve equation
        wkd_enters_i = round(float (tot_wkd_trips_i) * 0.5)
        wkd_exits_i = round(tot_wkd_trips_i - wkd_enters_i)
        tot_AM_trips_i = round(0.52 * float(unit) - 5.70) # fitted curve equation
        AM_enters_i = round(float (tot_AM_trips_i) * 0.25)
        AM_exits_i = round(float (tot_AM_trips_i) * 0.75)
        tot_PM_trips_i = round(0.60 * float(unit) - 3.93) # fitted curve equation
        PM_enters_i = round(float (tot_PM_trips_i) * 0.59)
        PM_exits_i = round(float (tot_PM_trips_i) * 0.41)
        AM_enters_dir_i = '25%'
        AM_exits_dir_i = '75%'
        PM_enters_dir_i = '59%'
        PM_exits_dir_i = '41%'
        weekday_i = 'T = 7.62 (X) - 50.48'
        AMi = 'T = 0.52 (X) - 5.70'
        PMi = 'T = 0.60 (X) - 3.93'
        tripi = 'Total'
        LUi_in_residential = LUi if LUi in residential_list else None
        LUi_in_retail = LUi if LUi in retail_list else None
        LUi_in_restaurant = LUi if LUi in restaurant_list else None
        LUi_in_hotel = LUi if LUi in hotel_list else None

    elif LUi == "220":
        yes_or_no = input("Is it close to rail transit? (Y/N) ")
        if yes_or_no.lower() =="y": # Code to execute if user's input is "Y" or "y"
            tot_wkd_trips_i = round(6.13 * float(unit) - 550.73) # fitted curve equation
            wkd_enters_i = round(float (tot_wkd_trips_i) * 0.5)
            wkd_exits_i = round(tot_wkd_trips_i - wkd_enters_i)
            tot_AM_trips_i = round(0.38 * float(unit)) # average rate
            AM_enters_i = round(float (tot_AM_trips_i) * 0.29)
            AM_exits_i = round(float (tot_AM_trips_i) * 0.71)
            tot_PM_trips_i = round(0.61 * float(unit)) # average rate
            PM_enters_i = round(float (tot_PM_trips_i) * 0.60)
            PM_exits_i = round(float (tot_PM_trips_i) * 0.40)
            # LUi = "220Y"
            land_use_i = "Multifamily Housing (Low-Rise) Close to Rail Transit"
            AM_enters_dir_i = '29%'
            AM_exits_dir_i = '71%'
            PM_enters_dir_i = '60%'
            PM_exits_dir_i = '40%'
            weekday_i = 'T = 6.13 (X) -550.73'
            AMi = '0.38 / Unit'
            PMi = '0.61 / Unit'
            tripi = 'Total'
            LUi_in_residential = LUi if LUi in residential_list else None
            LUi_in_retail = LUi if LUi in retail_list else None
            LUi_in_restaurant = LUi if LUi in restaurant_list else None
            LUi_in_hotel = LUi if LUi in hotel_list else None
          
        elif yes_or_no.lower() == "n":  # Code to execute if user's input is "N" or "n"
            tot_wkd_trips_i = round(6.41 * float(unit) + 75.31) # fitted curve equation
            wkd_enters_i = round(float (tot_wkd_trips_i) * 0.5)
            wkd_exits_i = round(tot_wkd_trips_i - wkd_enters_i)
            tot_AM_trips_i = round(0.31 * float(unit) + 22.85) # fitted curve equation
            AM_enters_i = round(float (tot_AM_trips_i) * 0.24)
            AM_exits_i = round(float (tot_AM_trips_i) * 0.76)
            tot_PM_trips_i = round(0.43 * float(unit) + 20.55) # fitted curve equation
            PM_enters_i = round(float (tot_PM_trips_i) * 0.63)
            PM_exits_i = round(float (tot_PM_trips_i) * 0.37)
            # LUi = "220N"
            land_use_i = "Multifamily Housing (Low-Rise) Not Close to Rail Transit"
            AM_enters_dir_i = '24%'
            AM_exits_dir_i = '76%'
            PM_enters_dir_i = '63%'
            PM_exits_dir_i = '37%'
            weekday_i = 'T = 6.41 (X) + 75.31'
            AMi = 'T = 0.31 (X) + 22.85'
            PMi = 'T = 0.43 (X) + 20.55'
            tripi = 'Total'
            LUi_in_residential = LUi if LUi in residential_list else None
            LUi_in_retail = LUi if LUi in retail_list else None
            LUi_in_restaurant = LUi if LUi in restaurant_list else None
            LUi_in_hotel = LUi if LUi in hotel_list else None
         
        else:
            print ("Invalid input. Please enter 'Y' or 'N'. ") # Code to execute if user's input is neither "Y"/"y" nor "N"/"n"      
        measurement_i = 'Dwelling Units'
    elif LUi == "221":
        yes_or_no = input("Is it close to rail transit? (Y/N) ")
        if yes_or_no.lower() =="y": 
            tot_wkd_trips_i = round(4.75 * float(unit)) # average rate
            wkd_enters_i = round(float (tot_wkd_trips_i) * 0.5)
            wkd_exits_i = round(tot_wkd_trips_i - wkd_enters_i)
            tot_AM_trips_i = round(0.31 * float(unit) + 1.06) # fitted curve equation
            AM_enters_i = round(float (tot_AM_trips_i) * 0.36)
            AM_exits_i = round(float (tot_AM_trips_i) * 0.64)
            tot_PM_trips_i = round(0.29 * float(unit) - 0.09) # fitted curve equation
            PM_enters_i = round(float (tot_PM_trips_i) * 0.65)
            PM_exits_i = round(float (tot_PM_trips_i) * 0.35)
            # LUi = "221Y"
            land_use_i = "Multifamily Housing (Mid-Rise) Close to Rail Transit"
            AM_enters_dir_i = '36%'
            AM_exits_dir_i = '64%'
            PM_enters_dir_i = '65%'
            PM_exits_dir_i = '35%'
            weekday_i = '4.75 / Unit'
            AMi = 'T = 0.31 (X) + 1.06'
            PMi = 'T = 0.29 (X) - 0.09'
            tripi = 'Total'
            LUi_in_residential = LUi if LUi in residential_list else None
            LUi_in_retail = LUi if LUi in retail_list else None
            LUi_in_restaurant = LUi if LUi in restaurant_list else None
            LUi_in_hotel = LUi if LUi in hotel_list else None
          
        elif yes_or_no.lower() == "n": 
            tot_wkd_trips_i = round(4.77 * float(unit) - 46.46) # fitted curve equation
            wkd_enters_i = round(float (tot_wkd_trips_i) * 0.5)
            wkd_exits_i = round(tot_wkd_trips_i - wkd_enters_i)
            tot_AM_trips_i = round(0.44 * float(unit) - 11.61) # fitted curve equation
            AM_enters_i = round(float (tot_AM_trips_i) * 0.23)
            AM_exits_i = round(float (tot_AM_trips_i) * 0.77)
            tot_PM_trips_i = round(0.39 * float(unit) + 0.34) # fitted curve equation
            PM_enters_i = round(float (tot_PM_trips_i) * 0.61)
            PM_exits_i = round(float (tot_PM_trips_i) * 0.39)
            # LUi = "221N"
            land_use_i = "Multifamily Housing (Mid-Rise) Not Close to Rail Transit"
            AM_enters_dir_i = '23%'
            AM_exits_dir_i = '77%'
            PM_enters_dir_i = '61%'
            PM_exits_dir_i = '39%'
            weekday_i = 'T = 4.77 (X) - 46.46'
            AMi = 'T = 0.44 (X) - 11.61'
            PMi = 'T = 0.39 (X) + 0.34'
            tripi = 'Total'
            LUi_in_residential = LUi if LUi in residential_list else None
            LUi_in_retail = LUi if LUi in retail_list else None
            LUi_in_restaurant = LUi if LUi in restaurant_list else None
            LUi_in_hotel = LUi if LUi in hotel_list else None
        else:
            print ("Invalid input. Please enter 'Y' or 'N'. ")       
        measurement_i = 'Dwelling Units'
        
    elif LUi == "222":
        measurement_i = 'Dwelling Units'
        yes_or_no = input("Is it close to rail transit? (Y/N) ")
        if yes_or_no.lower() =="y": 
            tot_wkd_trips_i = round(3.96 * float(unit)) # average rate
            wkd_enters_i = round(float (tot_wkd_trips_i) * 0.5)
            wkd_exits_i = round(tot_wkd_trips_i - wkd_enters_i)
            tot_AM_trips_i = round(0.23 * float(unit)) # average rate
            AM_enters_i = round(float (tot_AM_trips_i) * 0.22)
            AM_exits_i = round(float (tot_AM_trips_i) * 0.78)
            tot_PM_trips_i = round(0.26 * float(unit)) # average rate
            PM_enters_i = round(float (tot_PM_trips_i) * 0.62)
            PM_exits_i = round(float (tot_PM_trips_i) * 0.38)
            # LUi = "221Y"
            land_use_i = "Multifamily Housing (High-Rise) Close to Rail Transit"
            AM_enters_dir_i = '22%'
            AM_exits_dir_i = '78%'
            PM_enters_dir_i = '62%'
            PM_exits_dir_i = '38%'
            weekday_i = '3.96 / Unit'
            AMi = '0.23 / Unit'
            PMi = '0.26 / Unit'
            tripi = 'Total'
            LUi_in_residential = LUi if LUi in residential_list else None
            LUi_in_retail = LUi if LUi in retail_list else None
            LUi_in_restaurant = LUi if LUi in restaurant_list else None
            LUi_in_hotel = LUi if LUi in hotel_list else None
          
        elif yes_or_no.lower() == "n": 
            tot_wkd_trips_i = round(3.76 * float(unit) + 377.04) # fitted curve equation
            wkd_enters_i = round(float (tot_wkd_trips_i) * 0.5)
            wkd_exits_i = round(tot_wkd_trips_i - wkd_enters_i)
            tot_AM_trips_i = round(0.22 * float(unit) + 18.85) # fitted curve equation
            AM_enters_i = round(float (tot_AM_trips_i) * 0.26)
            AM_exits_i = round(float (tot_AM_trips_i) * 0.74)
            tot_PM_trips_i = round(0.26 * float(unit) + 23.12) # fitted curve equation
            PM_enters_i = round(float (tot_PM_trips_i) * 0.62)
            PM_exits_i = round(float (tot_PM_trips_i) * 0.38)
            # LUi = "221N"
            land_use_i = "Multifamily Housing (High-Rise) Not Close to Rail Transit"
            AM_enters_dir_i = '26%'
            AM_exits_dir_i = '74%'
            PM_enters_dir_i = '62%'
            PM_exits_dir_i = '38%'
            weekday_i = 'T = 3.76 (X) + 377.04'
            AMi = 'T = 0.22 (X) + 18.85'
            PMi = 'T = 0.26 (X) + 23.12'
            tripi = 'Total'
            LUi_in_residential = LUi if LUi in residential_list else None
            LUi_in_retail = LUi if LUi in retail_list else None
            LUi_in_restaurant = LUi if LUi in restaurant_list else None
            LUi_in_hotel = LUi if LUi in hotel_list else None
            
    elif LUi == "251":
        land_use_i = "Senior Adult Housing - Single-Family"
        measurement_i = 'Dwelling Units'
        tot_wkd_trips_i = round(np.exp(0.85 * np.log(float(unit)) + 2.47)) # fitted curve equation
        wkd_enters_i = round(float (tot_wkd_trips_i) * 0.5)
        wkd_exits_i = round(tot_wkd_trips_i - wkd_enters_i)
        tot_AM_trips_i = round(np.exp(0.76 * np.log(float(unit)) + 0.16)) # fitted curve equation
        AM_enters_i = round(float (tot_AM_trips_i) * 0.33)
        AM_exits_i = round(float (tot_AM_trips_i) * 0.67)
        tot_PM_trips_i = round(np.exp(0.78 * np.log(float(unit)) + 0.20)) # fitted curve equation
        PM_enters_i = round(float (tot_PM_trips_i) * 0.61)
        PM_exits_i = round(float (tot_PM_trips_i) * 0.39)
        AM_enters_dir_i = '33%'
        AM_exits_dir_i = '67%'
        PM_enters_dir_i = '61%'
        PM_exits_dir_i = '39%'
        weekday_i = 'Ln (T) = 0.85 Ln (X) + 2.47' 
        AMi = 'Ln (T) = 0.76 Ln (X) + 0.16'
        PMi = 'Ln (T) = 0.78 Ln (X) + 0.20'
        tripi = 'Total'
        LUi_in_residential = LUi if LUi in residential_list else None
        LUi_in_retail = LUi if LUi in retail_list else None
        LUi_in_restaurant = LUi if LUi in restaurant_list else None
        LUi_in_hotel = LUi if LUi in hotel_list else None
        
    elif LUi == "260":
        land_use_i = "Recreational Homes"
        measurement_i = 'Dwelling Units'
        tot_wkd_trips_i = round(np.exp(0.94 * np.log(float(unit)) + 1.64)) # fitted curve equation
        wkd_enters_i = round(float (tot_wkd_trips_i) * 0.5)
        wkd_exits_i = round(tot_wkd_trips_i - wkd_enters_i)
        tot_AM_trips_i = round(np.exp(1.00 * np.log(float(unit)) - 1.53)) # fitted curve equation
        AM_enters_i = round(float (tot_AM_trips_i) * 0.55)
        AM_exits_i = round(float (tot_AM_trips_i) * 0.45)
        tot_PM_trips_i = round(np.exp(0.93 * np.log(float(unit)) - 0.76)) # fitted curve equation
        PM_enters_i = round(float (tot_PM_trips_i) * 0.46)
        PM_exits_i = round(float (tot_PM_trips_i) * 0.54)
        AM_enters_dir_i = '55%'
        AM_exits_dir_i = '45%'
        PM_enters_dir_i = '46%'
        PM_exits_dir_i = '54%'
        weekday_i = 'Ln (T) = 0.94 Ln (X) + 1.64' 
        AMi = 'Ln (T) = 1.00 Ln (X) - 1.53'
        PMi = 'Ln (T) = 0.93 Ln (X) - 0.76'
        tripi = 'Total'
        LUi_in_residential = LUi if LUi in residential_list else None
        LUi_in_retail = LUi if LUi in retail_list else None
        LUi_in_restaurant = LUi if LUi in restaurant_list else None
        LUi_in_hotel = LUi if LUi in hotel_list else None
         
        
            
    elif LUi == "310":
        tot_wkd_trips_i = round(12.23 * float(unit)) # average rate
        wkd_enters_i = round(float (tot_wkd_trips_i) * 0.5)
        wkd_exits_i = round(tot_wkd_trips_i - wkd_enters_i)
        tot_AM_trips_i = round(0.62 * float(unit)) # average rate
        AM_enters_i = round(float (tot_AM_trips_i) * 0.56)
        AM_exits_i = round(float (tot_AM_trips_i) * 0.44)
        tot_PM_trips_i = round(0.73 * float(unit)) # average rate
        PM_enters_i = round(float (tot_PM_trips_i) * 0.49)
        PM_exits_i = round(float (tot_PM_trips_i) * 0.51)
        land_use_i = "Hotel"
        AM_enters_dir_i = '56%'
        AM_exits_dir_i = '44%'
        PM_enters_dir_i = '49%'
        PM_exits_dir_i = '51%'
        weekday_i = '12.23 / Unit'
        AMi = '0.62 / Unit'
        PMi = '0.73 / Unit'
        tripi = 'Total'
        measurement_i = 'Occupied Rooms'
        LUi_in_residential = LUi if LUi in residential_list else None
        LUi_in_retail = LUi if LUi in retail_list else None
        LUi_in_restaurant = LUi if LUi in restaurant_list else None
        LUi_in_hotel = LUi if LUi in hotel_list else None
        
    elif LUi == "420":
        tot_wkd_trips_i = round(2.41 * float(unit)) # average
        wkd_enters_i = round(float (tot_wkd_trips_i) * 0.5)
        wkd_exits_i = round(tot_wkd_trips_i - wkd_enters_i)
        tot_AM_trips_i = round(0.07 * float(unit)) # average
        AM_enters_i = round(float (tot_AM_trips_i) * 0.33)
        AM_exits_i = round(float (tot_AM_trips_i) * 0.67)
        AM_enters_dir_i = '33%'
        AM_exits_dir_i = '67%'
        tot_PM_trips_i = round(0.21 * float(unit)) # average
        PM_enters_i = round(float (tot_PM_trips_i) * 0.60)
        PM_exits_i = round(float (tot_PM_trips_i) * 0.40)
        PM_enters_dir_i = '60%'
        PM_exits_dir_i = '40%'
        land_use_i = "Marina"
        weekday_i = '2.41 / Unit'
        AMi = '0.07 / Unit'
        PMi = '0.21 / Unit'
        tripi = 'Total'
        measurement_i = 'Berths'
        LUi_in_residential = LUi if LUi in residential_list else None
        LUi_in_retail = LUi if LUi in retail_list else None
        LUi_in_restaurant = LUi if LUi in restaurant_list else None
        LUi_in_hotel = LUi if LUi in hotel_list else None
        
    elif LUi == "430":
        tot_wkd_trips_i = round(30.38 * float(unit)) # average
        wkd_enters_i = round(float (tot_wkd_trips_i) * 0.5)
        wkd_exits_i = round(tot_wkd_trips_i - wkd_enters_i)
        tot_AM_trips_i = round(1.76 * float(unit)) # average
        AM_enters_i = round(float (tot_AM_trips_i) * 0.79)
        AM_exits_i = round(float (tot_AM_trips_i) * 0.21)
        AM_enters_dir_i = '79%'
        AM_exits_dir_i = '21%'
        tot_PM_trips_i = round(2.91 * float(unit)) # average
        PM_enters_i = round(float (tot_PM_trips_i) * 0.53)
        PM_exits_i = round(float (tot_PM_trips_i) * 0.47)
        PM_enters_dir_i = '53%'
        PM_exits_dir_i = '47%'
        land_use_i = "Golf Course"
        weekday_i = '30.38 / Unit'
        AMi = '1.76 / Unit'
        PMi = '2.91 / Unit'
        tripi = 'Total'
        measurement_i = 'Holes'
        LUi_in_residential = LUi if LUi in residential_list else None
        LUi_in_retail = LUi if LUi in retail_list else None
        LUi_in_restaurant = LUi if LUi in restaurant_list else None
        LUi_in_hotel = LUi if LUi in hotel_list else None
            
    elif LUi == "488":
        tot_wkd_trips_i = round(71.33 * float(unit)) # average rate
        wkd_enters_i = round(float (tot_wkd_trips_i) * 0.5)
        wkd_exits_i = round(tot_wkd_trips_i - wkd_enters_i)
        tot_AM_trips_i = round(0.99 * float(unit)) # average rate
        AM_enters_i = round(float (tot_AM_trips_i) * 0.61)
        AM_exits_i = round(float (tot_AM_trips_i) * 0.39)
        tot_PM_trips_i = round(16.43 * float(unit)) # average rate
        PM_enters_i = round(float (tot_PM_trips_i) * 0.66)
        PM_exits_i = round(float (tot_PM_trips_i) * 0.34)
        land_use_i = "Soccer Complex"
        AM_enters_dir_i = '61%'
        AM_exits_dir_i = '39%'
        PM_enters_dir_i = '66%'
        PM_exits_dir_i = '34%'
        weekday_i = '71.33 / Unit'
        AMi = '0.99 / Unit'
        PMi = '16.43 / Unit'
        tripi = 'Total'
        measurement_i = 'Fields'
        LUi_in_residential = LUi if LUi in residential_list else None
        LUi_in_retail = LUi if LUi in retail_list else None
        LUi_in_restaurant = LUi if LUi in restaurant_list else None
        LUi_in_hotel = LUi if LUi in hotel_list else None
        
    elif LUi == "490":
        tot_wkd_trips_i = round(30.32 * float(unit)) # average rate
        wkd_enters_i = round(float (tot_wkd_trips_i) * 0.5)
        wkd_exits_i = round(tot_wkd_trips_i - wkd_enters_i)
        tot_AM_trips_i = round(0 * float(unit)) # does not have info for AM peak hour
        AM_enters_i = round(float (tot_AM_trips_i) * 0.61) # not important because total AM is zero
        AM_exits_i = round(float (tot_AM_trips_i) * 0.39) # not important because total AM is zero
        tot_PM_trips_i = round(4.21 * float(unit)) # average rate
        PM_enters_i = round(float (tot_PM_trips_i) * 0.50)
        PM_exits_i = round(tot_PM_trips_i - PM_enters_i)
        land_use_i = "Tennis Courts"
        AM_enters_dir_i = '--'
        AM_exits_dir_i = '--'
        PM_enters_dir_i = '50%'
        PM_exits_dir_i = '50%'
        weekday_i = '30.32 / Unit'
        AMi = '-- / Unit'
        PMi = '4.21 / Unit'
        tripi = 'Total'
        measurement_i = 'Tennis Courts'
        LUi_in_residential = LUi if LUi in residential_list else None
        LUi_in_retail = LUi if LUi in retail_list else None
        LUi_in_restaurant = LUi if LUi in restaurant_list else None
        LUi_in_hotel = LUi if LUi in hotel_list else None
        
    elif LUi == "491":
        tot_wkd_trips_i = round(27.71 * float(unit)) # average rate
        wkd_enters_i = round(float (tot_wkd_trips_i) * 0.50)
        wkd_exits_i = round(tot_wkd_trips_i - wkd_enters_i)
        tot_AM_trips_i = round(3.82 * float(unit)) # does not have info for AM peak hour, adopt the PM Peak Hour
        AM_enters_i = round(float (tot_AM_trips_i) * 0.50) # not important because total AM is zero
        AM_exits_i = round(tot_AM_trips_i - AM_enters_i)
        tot_PM_trips_i = round(3.82 * float(unit)) # average rate
        PM_enters_i = round(float (tot_PM_trips_i) * 0.50)
        PM_exits_i = round(tot_PM_trips_i - PM_enters_i)
        land_use_i = "Racquet/Tennis Club"
        AM_enters_dir_i = '50%'
        AM_exits_dir_i = '50%'
        PM_enters_dir_i = '50%'
        PM_exits_dir_i = '50%'
        weekday_i = '27.71 / Unit'
        AMi = '3.82 / Unit'
        PMi = '3.82 / Unit'
        tripi = 'Total'
        measurement_i = 'Tennis Courts'
        LUi_in_residential = LUi if LUi in residential_list else None
        LUi_in_retail = LUi if LUi in retail_list else None
        LUi_in_restaurant = LUi if LUi in restaurant_list else None
        LUi_in_hotel = LUi if LUi in hotel_list else None
        
    elif LUi == "498":
        tot_wkd_trips_i = round(75.8 * float(unit)) # 2.5 times of average rate, 10 players at maximum playing basketball is 2.5 times of 4 players at maximum playing tennis
        wkd_enters_i = round(float (tot_wkd_trips_i) * 0.5)
        wkd_exits_i = round(tot_wkd_trips_i - wkd_enters_i)
        tot_AM_trips_i = round(0 * float(unit)) # does not have info for AM peak hour
        AM_enters_i = round(float (tot_AM_trips_i) * 0.61) # not important because total AM is zero
        AM_exits_i = round(float (tot_AM_trips_i) * 0.39) # not important because total AM is zero
        tot_PM_trips_i = round(10.525 * float(unit)) # 2.5 times of average rate, 10 players at maximum playing basketball is 2.5 times of 4 players at maximum playing tennis
        PM_enters_i = round(float (tot_PM_trips_i) * 0.50)
        PM_exits_i = round(tot_PM_trips_i - PM_enters_i)
        land_use_i = "Basketball Courts"
        AM_enters_dir_i = '--'
        AM_exits_dir_i = '--'
        PM_enters_dir_i = '50%'
        PM_exits_dir_i = '50%'
        weekday_i = '75.8 / Unit'
        AMi = '-- / Unit'
        PMi = '10.525 / Unit'
        tripi = 'Total'
        measurement_i = 'Basketball Courts'
        LUi_in_residential = LUi if LUi in residential_list else None
        LUi_in_retail = LUi if LUi in retail_list else None
        LUi_in_restaurant = LUi if LUi in restaurant_list else None
        LUi_in_hotel = LUi if LUi in hotel_list else None
        
    elif LUi == "499":
        tot_wkd_trips_i = round(90.96 * float(unit)) # 3.0 times of average rate, 12 players at maximum playing basketball is 3.0 times of 4 players at maximum playing tennis
        wkd_enters_i = round(float (tot_wkd_trips_i) * 0.5)
        wkd_exits_i = round(tot_wkd_trips_i - wkd_enters_i)
        tot_AM_trips_i = round(0 * float(unit)) # does not have info for AM peak hour
        AM_enters_i = round(float (tot_AM_trips_i) * 0.61) # not important because total AM is zero
        AM_exits_i = round(float (tot_AM_trips_i) * 0.39) # not important because total AM is zero
        tot_PM_trips_i = round(12.63 * float(unit)) # 3.0 times of average rate, 12 players at maximum playing basketball is 3.0 times of 4 players at maximum playing tennis
        PM_enters_i = round(float (tot_PM_trips_i) * 0.50)
        PM_exits_i = round(tot_PM_trips_i - PM_enters_i)
        land_use_i = "Volleyball Courts"
        AM_enters_dir_i = '--'
        AM_exits_dir_i = '--'
        PM_enters_dir_i = '50%'
        PM_exits_dir_i = '50%'
        weekday_i = '90.96 / Unit'
        AMi = '-- / Unit'
        PMi = '12.63 / Unit'
        tripi = 'Total'
        measurement_i = 'Volleyball Courts'
        LUi_in_residential = LUi if LUi in residential_list else None
        LUi_in_retail = LUi if LUi in retail_list else None
        LUi_in_restaurant = LUi if LUi in restaurant_list else None
        LUi_in_hotel = LUi if LUi in hotel_list else None
            
    elif LUi == "816":
        tot_wkd_trips_i = round(8.07 * float(unit)) # average rate
        wkd_enters_i = round(float (tot_wkd_trips_i) * 0.5)
        wkd_exits_i = round(tot_wkd_trips_i - wkd_enters_i)
        tot_AM_trips_i = round(0.92 * float(unit)) # average rate
        # tot_AM_trips_i = round(0.75 * float(unit) + 1.92) # fitted curve equation, # of stuides = 4 <= 20, R-squared = 0.62 <= 0.75
        AM_enters_i = round(float (tot_AM_trips_i) * 0.54)
        AM_exits_i = round(float (tot_AM_trips_i) * 0.46)
        tot_PM_trips_i = round(2.98 * float(unit)) # average rate
        PM_enters_i = round(float (tot_PM_trips_i) * 0.46)
        PM_exits_i = round(float (tot_PM_trips_i) * 0.54)
        land_use_i = "Hardware/Paint Store"
        AM_enters_dir_i = '54%'
        AM_exits_dir_i = '46%'
        PM_enters_dir_i = '46%'
        PM_exits_dir_i = '54%'
        weekday_i = '8.07 / Unit'
        AMi = '0.92 / Unit'
        PMi = '2.98 / Unit'
        tripi = 'Total'
        measurement_i = 'K Square Feet'
        LUi_in_residential = LUi if LUi in residential_list else None
        LUi_in_retail = LUi if LUi in retail_list else None
        LUi_in_restaurant = LUi if LUi in restaurant_list else None
        LUi_in_hotel = LUi if LUi in hotel_list else None
        
    elif LUi == "820":
        tot_wkd_trips_i = round(26.11 * float(unit) + 5863.73) # fitted curve equation
        wkd_enters_i = round(float (tot_wkd_trips_i) * 0.5)
        wkd_exits_i = round(tot_wkd_trips_i - wkd_enters_i)
        tot_AM_trips_i = round(0.59 * float(unit) + 133.55) # fitted curve equation
        AM_enters_i = round(float (tot_AM_trips_i) * 0.62)
        AM_exits_i = round(float (tot_AM_trips_i) * 0.38)
        tot_PM_trips_i = round(np.exp(0.72 * np.log(float(unit)) + 3.02)) # fitted curve equation
        PM_enters_i = round(float (tot_PM_trips_i) * 0.48)
        PM_exits_i = round(float (tot_PM_trips_i) * 0.52)
        land_use_i = "Shopping Center (>150k)"
        AM_enters_dir_i = '62%'
        AM_exits_dir_i = '38%'
        PM_enters_dir_i = '48%'
        PM_exits_dir_i = '52%'
        weekday_i = 'T = 26.11 (X) + 5863.73'
        AMi = 'T = 0.59 (X) + 133.55'
        PMi = 'Ln (T) = 0.72 Ln(X) + 3.02'
        tripi = 'Total'
        measurement_i = 'K Square Feet'
        LUi_in_residential = LUi if LUi in residential_list else None
        LUi_in_retail = LUi if LUi in retail_list else None
        LUi_in_restaurant = LUi if LUi in restaurant_list else None
        LUi_in_hotel = LUi if LUi in hotel_list else None
                   
    elif LUi == "821":
        yes_or_no = input("Does it have supermarket? (Y/N) ")
        if yes_or_no.lower() == "y":
            tot_wkd_trips_i = round(94.49 * float(unit)) # average rate
            # tot_wkd_trips_i = round(76.96 * float(unit) + 1412.79) # fitted curve equation, # of studies = 17 <= 20, R-square = 0.5 <= 0.75
            wkd_enters_i = round(float (tot_wkd_trips_i) * 0.5)
            wkd_exits_i = round(tot_wkd_trips_i - wkd_enters_i)
            tot_AM_trips_i = round(3.53 * float(unit)) # average rate
            AM_enters_i = round(float (tot_AM_trips_i) * 0.62)
            AM_exits_i = round(float (tot_AM_trips_i) * 0.38)
            tot_PM_trips_i = round(7.67 * float(unit) + 118.86) # fitted curve equation, # of studies = 51
            PM_enters_i = round(float (tot_PM_trips_i) * 0.48)
            PM_exits_i = round(float (tot_PM_trips_i) * 0.52)
            # LUi = "821Y"
            land_use_i = "Shopping Plaza (40-150k) Supermarket Yes"
            AM_enters_dir_i = '62%'
            AM_exits_dir_i = '38%'
            PM_enters_dir_i = '48%'
            PM_exits_dir_i = '52%'
            weekday_i = '94.49 / Unit'
            AMi = '3.53 / Unit'
            PMi = 'T = 7.67 (X) + 118.86'
            tripi = 'Total'
            measurement_i = 'K Square Feet'
            LUi_in_residential = LUi if LUi in residential_list else None
            LUi_in_retail = LUi if LUi in retail_list else None
            LUi_in_restaurant = LUi if LUi in restaurant_list else None
            LUi_in_hotel = LUi if LUi in hotel_list else None
          
        elif yes_or_no.lower() == "n": 
            tot_wkd_trips_i = round(67.52 * float(unit)) # average rate
            wkd_enters_i = round(float (tot_wkd_trips_i) * 0.5)
            wkd_exits_i = round(tot_wkd_trips_i - wkd_enters_i)
            tot_AM_trips_i = round(1.73 * float(unit)) # average rate
            AM_enters_i = round(float (tot_AM_trips_i) * 0.62)
            AM_exits_i = round(float (tot_AM_trips_i) * 0.38)
            tot_PM_trips_i = round(5.19 * float(unit)) # average rate
            PM_enters_i = round(float (tot_PM_trips_i) * 0.49)
            PM_exits_i = round(float (tot_PM_trips_i) * 0.51)
            # LUi = "821N"
            land_use_i = "Shopping Plaza (40-150k) Supermarket No"
            AM_enters_dir_i = '62%'
            AM_exits_dir_i = '38%'
            PM_enters_dir_i = '49%'
            PM_exits_dir_i = '51%'
            weekday_i = '67.52 / Unit'
            AMi = '1.73 / Unit'
            PMi = '5.19 / Unit'
            tripi = 'Total'
            measurement_i = 'K Square Feet'
            LUi_in_residential = LUi if LUi in residential_list else None
            LUi_in_retail = LUi if LUi in retail_list else None
            LUi_in_restaurant = LUi if LUi in restaurant_list else None
            LUi_in_hotel = LUi if LUi in hotel_list else None
            
    elif LUi == "822":
        # tot_wkd_trips_i = round(54.45 * float(unit)) # average rate
        tot_wkd_trips_i = round(42.20 * float(unit) + 229.68) # fitted curve equation, # of studies = 4, but R-square = 0.96
        wkd_enters_i = round(float (tot_wkd_trips_i) * 0.5)
        wkd_exits_i = round(tot_wkd_trips_i - wkd_enters_i)
        tot_AM_trips_i = round(2.36 * float(unit)) # average rate, # of studies = 5 <= 20, R-square = 0.57 <= 0.75
        # tot_AM_trips_i = round(np.exp(0.66 * np.log(float(unit)) + 1.84)) # fitted curve equation
        AM_enters_i = round(float (tot_AM_trips_i) * 0.60)
        AM_exits_i = round(float (tot_AM_trips_i) * 0.40)
        AM_enters_dir_i = '60%'
        AM_exits_dir_i = '40%'
        tot_PM_trips_i = round(np.exp(0.71 * np.log(float(unit)) + 2.72)) # fitted curve equation
        PM_enters_i = round(float (tot_PM_trips_i) * 0.50)
        # PM_exits_i = round(float (tot_PM_trips_i) * 0.50)
        PM_exits_i = round(tot_PM_trips_i - PM_enters_i)
        PM_enters_dir_i = '50%'
        PM_exits_dir_i = '50%'
        land_use_i = "Strip Retail Plaza (<40k)"
        weekday_i = 'T = 42.20 (X) + 229.68'
        AMi = '2.36 / Unit'
        PMi = 'Ln (T) = 0.71 Ln (X) + 2.72'
        tripi = 'Total'
        measurement_i = 'K Square Feet'
        LUi_in_residential = LUi if LUi in residential_list else None
        LUi_in_retail = LUi if LUi in retail_list else None
        LUi_in_restaurant = LUi if LUi in restaurant_list else None
        LUi_in_hotel = LUi if LUi in hotel_list else None
        
    elif LUi == "842":
        tot_wkd_trips_i = round(5.00 * float(unit)) # average
        wkd_enters_i = round(float (tot_wkd_trips_i) * 0.5)
        wkd_exits_i = round(tot_wkd_trips_i - wkd_enters_i)
        tot_AM_trips_i = round(0.46 * float(unit)) # average
        AM_enters_i = round(float (tot_AM_trips_i) * 0.85)
        AM_exits_i = round(float (tot_AM_trips_i) * 0.15)
        tot_PM_trips_i = round(0.77 * float(unit)) # average
        PM_enters_i = round(float (tot_PM_trips_i) * 0.31)
        PM_exits_i = round(float (tot_PM_trips_i) * 0.69)
        land_use_i = "Recreational Vehicle Sales"
        AM_enters_dir_i = '85%'
        AM_exits_dir_i = '15%'
        PM_enters_dir_i = '31%'
        PM_exits_dir_i = '69%'
        weekday_i = '5.00 / Unit'
        AMi = '0.46 / Unit'
        PMi = '0.77 / Unit'
        tripi = 'Total'
        measurement_i = 'K Square Feet'
        LUi_in_residential = LUi if LUi in residential_list else None
        LUi_in_retail = LUi if LUi in retail_list else None
        LUi_in_restaurant = LUi if LUi in restaurant_list else None
        LUi_in_hotel = LUi if LUi in hotel_list else None
        
    elif LUi == "931":
        tot_wkd_trips_i = round(83.84 * float(unit)) # average
        wkd_enters_i = round(float (tot_wkd_trips_i) * 0.5)
        wkd_exits_i = round(tot_wkd_trips_i - wkd_enters_i)
        tot_AM_trips_i = round(0.73 * float(unit)) # average
        AM_enters_i = None
        AM_exits_i = None
        AM_enters_dir_i = 'N/A'
        AM_exits_dir_i = 'N/A'
        tot_PM_trips_i = round(7.80 * float(unit)) # average
        PM_enters_i = round(float (tot_PM_trips_i) * 0.67)
        PM_exits_i = round(float (tot_PM_trips_i) * 0.33)
        PM_enters_dir_i = '67%'
        PM_exits_dir_i = '33%'
        land_use_i = "Fine Dining Restaurant"
        weekday_i = '83.84 / Unit'
        AMi = '0.73 / Unit'
        PMi = '7.80 / Unit'
        tripi = 'Total'
        measurement_i = 'K Square Feet'
        LUi_in_residential = LUi if LUi in residential_list else None
        LUi_in_retail = LUi if LUi in retail_list else None
        LUi_in_restaurant = LUi if LUi in restaurant_list else None
        LUi_in_hotel = LUi if LUi in hotel_list else None
        
    elif LUi == "932":
        tot_wkd_trips_i = round(107.20 * float(unit)) # average
        wkd_enters_i = round(float (tot_wkd_trips_i) * 0.5)
        wkd_exits_i = round(tot_wkd_trips_i - wkd_enters_i)
        tot_AM_trips_i = round(9.57 * float(unit)) # average
        AM_enters_i = round(float (tot_AM_trips_i) * 0.55)
        AM_exits_i = round(float (tot_AM_trips_i) * 0.45)
        AM_enters_dir_i = '55%'
        AM_exits_dir_i = '45%'
        tot_PM_trips_i = round(9.05 * float(unit)) # average
        PM_enters_i = round(float (tot_PM_trips_i) * 0.61)
        PM_exits_i = round(float (tot_PM_trips_i) * 0.39)
        PM_enters_dir_i = '61%'
        PM_exits_dir_i = '39%'
        land_use_i = "High-Turnover (Sit-Down) Restaurant"
        weekday_i = '107.20 / Unit'
        AMi = '9.57 / Unit'
        PMi = '9.05 / Unit'
        tripi = 'Total'
        measurement_i = 'K Square Feet'
        LUi_in_residential = LUi if LUi in residential_list else None
        LUi_in_retail = LUi if LUi in retail_list else None
        LUi_in_restaurant = LUi if LUi in restaurant_list else None
        LUi_in_hotel = LUi if LUi in hotel_list else None
        
    elif LUi == "933":
        tot_wkd_trips_i = round(450.49 * float(unit)) # average
        wkd_enters_i = round(float (tot_wkd_trips_i) * 0.5)
        wkd_exits_i = round(tot_wkd_trips_i - wkd_enters_i)
        tot_AM_trips_i = round(43.18 * float(unit)) # average
        AM_enters_i = round(float (tot_AM_trips_i) * 0.58)
        AM_exits_i = round(float (tot_AM_trips_i) * 0.42)
        AM_enters_dir_i = '58%'
        AM_exits_dir_i = '42%'
        tot_PM_trips_i = round(33.21 * float(unit)) # average
        PM_enters_i = round(float (tot_PM_trips_i) * 0.50)
        PM_exits_i = round(float (tot_PM_trips_i) * 0.50)
        PM_enters_dir_i = '50%'
        PM_exits_dir_i = '50%'
        land_use_i = "Fast-Food Restaurant without Drive-Through Window"
        weekday_i = '450.49 / Unit'
        AMi = '43.18 / Unit'
        PMi = '33.21 / Unit'
        tripi = 'Total'
        measurement_i = 'K Square Feet'
        LUi_in_residential = LUi if LUi in residential_list else None
        LUi_in_retail = LUi if LUi in retail_list else None
        LUi_in_restaurant = LUi if LUi in restaurant_list else None
        LUi_in_hotel = LUi if LUi in hotel_list else None
        
    elif LUi == "934":
        tot_wkd_trips_i = round(467.48 * float(unit)) # average
        wkd_enters_i = round(float (tot_wkd_trips_i) * 0.5)
        wkd_exits_i = round(tot_wkd_trips_i - wkd_enters_i)
        tot_AM_trips_i = round(44.61 * float(unit)) # average
        AM_enters_i = round(float (tot_AM_trips_i) * 0.51)
        AM_exits_i = round(float (tot_AM_trips_i) * 0.49)
        AM_enters_dir_i = '51%'
        AM_exits_dir_i = '49%'
        tot_PM_trips_i = round(33.03 * float(unit)) # average
        PM_enters_i = round(float (tot_PM_trips_i) * 0.52)
        PM_exits_i = round(float (tot_PM_trips_i) * 0.48)
        PM_enters_dir_i = '52%'
        PM_exits_dir_i = '48%'
        land_use_i = "Fast-Food Restaurant with Drive-Through Window"
        weekday_i = '467.48 / Unit'
        AMi = '44.61 / Unit'
        PMi = '33.03 / Unit'
        tripi = 'Total'
        measurement_i = 'K Square Feet'
        LUi_in_residential = LUi if LUi in residential_list else None
        LUi_in_retail = LUi if LUi in retail_list else None
        LUi_in_restaurant = LUi if LUi in restaurant_list else None
        LUi_in_hotel = LUi if LUi in hotel_list else None
        
    elif LUi == "710":
        tot_wkd_trips_i = round(np.exp(0.87 * np.log(float(unit)) + 3.05)) # eqn
        wkd_enters_i = round(float (tot_wkd_trips_i) * 0.5)
        wkd_exits_i = round(tot_wkd_trips_i - wkd_enters_i)
        tot_AM_trips_i = round(np.exp(0.86 * np.log(float(unit)) + 1.16)) # eqn
        AM_enters_i = round(float (tot_AM_trips_i) * 0.88)
        AM_exits_i = round(float (tot_AM_trips_i) * 0.12)
        AM_enters_dir_i = '88%'
        AM_exits_dir_i = '12%'
        tot_PM_trips_i = round(np.exp(0.83 * np.log(float(unit)) + 1.29)) # eqn
        PM_enters_i = round(float (tot_PM_trips_i) * 0.17)
        PM_exits_i = round(float (tot_PM_trips_i) * 0.83)
        PM_enters_dir_i = '17%'
        PM_exits_dir_i = '83%'
        land_use_i = "General Office Building"
        weekday_i = 'Ln (T) = 0.87 Ln (X) + 3.05'
        AMi = 'Ln (T) = 0.86 Ln (X) + 1.16'
        PMi = 'Ln (T) = 0.83 Ln (X) + 1.29'
        tripi = 'Total'
        measurement_i = 'K Square Feet'
        LUi_in_residential = LUi if LUi in residential_list else None
        LUi_in_retail = LUi if LUi in retail_list else None
        LUi_in_restaurant = LUi if LUi in restaurant_list else None
        LUi_in_hotel = LUi if LUi in hotel_list else None
        
    elif LUi == "712":
        tot_wkd_trips_i = round(14.39 * float(unit)) # average
        wkd_enters_i = round(float (tot_wkd_trips_i) * 0.5)
        wkd_exits_i = round(tot_wkd_trips_i - wkd_enters_i)
        tot_AM_trips_i = round(1.67 * float(unit)) # average
        AM_enters_i = round(float (tot_AM_trips_i) * 0.82)
        AM_exits_i = round(float (tot_AM_trips_i) * 0.18)
        AM_enters_dir_i = '82%'
        AM_exits_dir_i = '18%'
        tot_PM_trips_i = round(2.16 * float(unit)) # average
        PM_enters_i = round(float (tot_PM_trips_i) * 0.34)
        PM_exits_i = round(float (tot_PM_trips_i) * 0.66)
        PM_enters_dir_i = '34%'
        PM_exits_dir_i = '66%'
        land_use_i = "Small Office Building"
        weekday_i = '14.39 / Unit'
        AMi = '1.67 / Unit'
        PMi = '2.16 / Unit'
        tripi = 'Total'
        measurement_i = 'K Square Feet'
        LUi_in_residential = LUi if LUi in residential_list else None
        LUi_in_retail = LUi if LUi in retail_list else None
        LUi_in_restaurant = LUi if LUi in restaurant_list else None
        LUi_in_hotel = LUi if LUi in hotel_list else None
        
            
    else:
        print ("Please type in a correct ITE LU#. ")
                                   
    land_use.append(land_use_i)
    measurement.append(measurement_i)
    LU.append(LUi)
    units.append(unit)
    Weekdays.append(weekday_i)
    AM.append(AMi)
    PM.append(PMi)
    trips.append(tripi)
    tot_wkd_trips.append(tot_wkd_trips_i)
    wkd_enters.append(wkd_enters_i)
    wkd_exits.append(wkd_exits_i)
    tot_AM_trips.append(tot_AM_trips_i)
    AM_enters.append(AM_enters_i)
    AM_exits.append(AM_exits_i)
    tot_PM_trips.append(tot_PM_trips_i)
    PM_enters.append(PM_enters_i)
    PM_exits.append(PM_exits_i)
    AM_enters_dir.append(AM_enters_dir_i)
    AM_exits_dir.append(AM_exits_dir_i)
    PM_enters_dir.append(PM_enters_dir_i)
    PM_exits_dir.append(PM_exits_dir_i)
    LU_in_residential.append(LUi_in_residential)
    LU_in_retail.append(LUi_in_retail)
    LU_in_restaurant.append(LUi_in_restaurant)
    LU_in_hotel.append(LUi_in_hotel)
   

# Create dataframe wto IC or pass-by
data_clear = {'ITE Land Use': land_use, 'LUC': LU, 'Size': units, 'Unit': measurement,
        'Weekday': Weekdays, 'AM Peak Hour': AM, 'PM Peak Hour': PM, 'Trips': trips,
        'Wkd Enter': wkd_enters, 'Wkd Exit': wkd_exits, 'Wkd Total': tot_wkd_trips,
        'AM Enter': AM_enters, 'AM Exit': AM_exits, 'AM Total': tot_AM_trips,   
        'PM Enter': PM_enters, 'PM Exit': PM_exits, 'PM Total': tot_PM_trips}
df_clear = pd.DataFrame(data_clear)

# Convert 'LUC' column to integers
df_clear['LUC'] = df_clear['LUC'].astype(int)
# print (df_clear)


# Create an empty dictionary to store directional distribution percentages
dir_dist_perc = {'retail': {}, 'restaurant': {}, 'residential': {}, 'hotel': {}, 'other': {}}

# Iterate over the data_clear list
for i, luc in enumerate(data_clear['LUC']):
    # Check if LUC is between 800 and 899 and set it as 'retail'
    if 800 <= int(luc) <= 899:
        dir_dist_perc['retail'][luc] = {
            'Wkd Enter': '50%',
            'Wkd Exit': '50%',
            'Wkd Total': '100%',
            'AM Enter': AM_enters_dir[i],
            'AM Exit': AM_exits_dir[i],
            'AM Total': '100%',
            'PM Enter': PM_enters_dir[i],
            'PM Exit': PM_exits_dir[i],
            'PM Total': '100%'
        }

    # Check if LUC is between 900 and 999 and set it as 'restaurant'
    elif 900 <= int(luc) <= 999:
        dir_dist_perc['restaurant'][luc] = {
            'Wkd Enter': '50%',
            'Wkd Exit': '50%',
            'Wkd Total': '100%',
            'AM Enter': AM_enters_dir[i],  
            'AM Exit': AM_exits_dir[i],   
            'AM Total': '100%',
            'PM Enter': PM_enters_dir[i],
            'PM Exit': PM_exits_dir[i],
            'PM Total': '100%'
        }
        
    # Check if LUC is between 200 and 299 and set it as 'residential'
    elif 200 <= int(luc) <= 299:
         dir_dist_perc['residential'][luc] = {
             'Wkd Enter': '50%',
             'Wkd Exit': '50%',
             'Wkd Total': '100%',
             'AM Enter': AM_enters_dir[i],  
             'AM Exit': AM_exits_dir[i],   
             'AM Total': '100%',
             'PM Enter': PM_enters_dir[i],
             'PM Exit': PM_exits_dir[i],
             'PM Total': '100%'
         }
         
    # Check if LUC is between 300 and 399 and set it as 'hotel'
    elif 300 <= int(luc) <= 399:
         dir_dist_perc['hotel'][luc] = {
             'Wkd Enter': '50%',
             'Wkd Exit': '50%',
             'Wkd Total': '100%',
             'AM Enter': AM_enters_dir[i],  
             'AM Exit': AM_exits_dir[i],   
             'AM Total': '100%',
             'PM Enter': PM_enters_dir[i],
             'PM Exit': PM_exits_dir[i],
             'PM Total': '100%'
         }
         
    # Check all the other LUC and set it as 'other'
    else:
        dir_dist_perc['other'][luc] = {
            'Wkd Enter': '50%',
            'Wkd Exit': '50%',
            'Wkd Total': '100%',
            'AM Enter': AM_enters_dir[i],  
            'AM Exit': AM_exits_dir[i],   
            'AM Total': '100%',
            'PM Enter': PM_enters_dir[i],
            'PM Exit': PM_exits_dir[i],
            'PM Total': '100%'
        }


# Read IC matrix table
IC_ori_PM = pd.read_csv("Unconstrained Internal Capture Rate Origin PM.csv", index_col = 0)
IC_dest_PM = pd.read_csv("Unconstrained Internal Capture Rate Dest PM.csv", index_col = 0)
IC_ori_AM = pd.read_csv("Unconstrained Internal Capture Rate Origin AM.csv", index_col = 0)
IC_dest_AM = pd.read_csv("Unconstrained Internal Capture Rate Dest AM.csv", index_col = 0)
print()
print('Four IC Rate matrix csv files are successfully read in the console')
print('*********************************************')
print()

# Create each dataframe
df_residential = df_clear.loc[df_clear.apply(lambda x: 200 <= int(x.LUC) <= 299, axis = 1)]
df_hotel = df_clear.loc[df_clear.apply(lambda x: 300 <= int(x.LUC) <= 399, axis = 1)]
df_other = df_clear.loc[df_clear.apply(lambda x: 400 <= int(x.LUC) <= 699, axis = 1)]
df_retail = df_clear.loc[df_clear.apply(lambda x: 800 <= int(x.LUC) <= 899, axis = 1)] # It applies the given lambda function to each row of the dataframe.
df_restaurant = df_clear.loc[df_clear.apply(lambda x: 900 <= int(x.LUC) <= 999, axis = 1)]



# Create a function to find if the elements in the project list are in the two lists
def check_crosslists_not_empty_hm_rest (list_a, list_b):    
    if any(item is not None for item in list_a) and any(item is not None for item in list_b):
        print (" There exists Internal Capture between the hotel and restaurant in a mixed-use development.")

        # calculate the minimun IC from hotel to restaurant in the PM Peak Hour
        IC_PM1_hm_rest = df_hotel['PM Exit'] * IC_ori_PM.loc['From_Hotel', 'To_Restaurant']
        IC_PM2_hm_rest = df_restaurant['PM Enter'] * IC_dest_PM.loc['To_Restaurant', 'From_Hotel']
        
        # In this example, 
        # np.full is used to create a matrix with the specified scalar value repeated in each row. 
        # The (array_length, 1) shape indicates that the matrix should have array_length rows and 1 column.
        # IC_PM1 = IC_PM1.to_numpy().reshape(-1, 1) # same as IC_PM1 = IC_PM1.values.reshape(-1, 1), convert IC_PM1 to a numpy array with shape (n, 1)
        IC_PM1_hm_rest = np.full((len(IC_PM2_hm_rest), 1), IC_PM1_hm_rest.values)
              
        # create a NumPy array from a Pandas Series, and then reshape array to one column two rows array
        IC_PM2_hm_rest = IC_PM2_hm_rest.values.reshape(-1, 1)
        
        # select the minimum value between arrays element-wise, row by row. And only take integer from the floating point (decimal) number.
        # astype(int) is kind of rounddown function, to make IC value as low as possible, in order to get a higher external trips
        IC_PM_hotel_restaurant = np.minimum(IC_PM1_hm_rest, IC_PM2_hm_rest).astype(int)
        
        # calculate the minimun IC from restaurant to retail in the PM Peak Hour
        IC_PM3_hm_rest = df_hotel['PM Enter'] * IC_dest_PM.loc['To_Hotel', 'From_Restaurant']
        IC_PM4_hm_rest = df_restaurant['PM Exit'] * IC_ori_PM.loc['From_Restaurant', 'To_Hotel']
        # IC_PM3 = IC_PM3.to_numpy().reshape(-1, 1) 
        # IC_PM4 = IC_PM4.to_numpy().reshape(-1, 1)
        IC_PM3_hm_rest = np.full((len(IC_PM4_hm_rest), 1), IC_PM3_hm_rest.values)
        IC_PM4_hm_rest = IC_PM4_hm_rest.values.reshape(-1, 1)
        IC_PM_restaurant_hotel = np.minimum(IC_PM3_hm_rest, IC_PM4_hm_rest).astype(int) # only take integer from the floating point number.
             
        # calculate the total IC between retail and restaurant in the PM Peak Hour
        IC_PM_tot_hm_rest = IC_PM_hotel_restaurant + IC_PM_restaurant_hotel

        # AM
        IC_AM1_hm_rest = df_hotel['AM Exit'] * IC_ori_AM.loc['From_Hotel', 'To_Restaurant']
        IC_AM2_hm_rest = df_restaurant['AM Enter'] * IC_dest_AM.loc['To_Restaurant', 'From_Hotel']
        IC_AM1_hm_rest = np.full((len(IC_AM2_hm_rest), 1), IC_AM1_hm_rest.values)
        IC_AM2_hm_rest = IC_AM2_hm_rest.values.reshape(-1, 1)
        # due to low IC value in the AM peak hour (sometimes we have 0.91 IC), instead of using astype(int), we use math.ceil, which is kind of roundup function
        IC_AM_hotel_restaurant = math.ceil(np.minimum(IC_AM1_hm_rest, IC_AM2_hm_rest))
        # convert int to numpy.ndarray
        IC_AM_hotel_restaurant = np.array([IC_AM_hotel_restaurant])
        # reshape 1D array (1,) to 2D array (1,1)
        IC_AM_hotel_restaurant = IC_AM_hotel_restaurant.reshape(1,1)
        
        IC_AM3_hm_rest = df_hotel['AM Enter'] * IC_dest_AM.loc['To_Hotel', 'From_Restaurant']
        IC_AM4_hm_rest = df_restaurant['AM Exit'] * IC_ori_AM.loc['From_Restaurant', 'To_Hotel']
        IC_AM3_hm_rest = np.full((len(IC_AM4_hm_rest), 1), IC_AM3_hm_rest.values)
        IC_AM4_hm_rest = IC_AM4_hm_rest.values.reshape(-1, 1)
        IC_AM_restaurant_hotel = math.ceil(np.minimum(IC_AM3_hm_rest, IC_AM4_hm_rest))
        IC_AM_restaurant_hotel = np.array([IC_AM_restaurant_hotel])
        IC_AM_restaurant_hotel = IC_AM_restaurant_hotel.reshape(1,1)
        IC_AM_tot_hm_rest = IC_AM_hotel_restaurant + IC_AM_restaurant_hotel

        # Wkd
        IC_wkd1_hm_rest = df_hotel['Wkd Exit'] * (IC_ori_AM.loc['From_Hotel', 'To_Restaurant'] + IC_ori_PM.loc['From_Hotel', 'To_Restaurant'])/2
        IC_wkd2_hm_rest = df_restaurant['Wkd Enter'] * (IC_dest_AM.loc['To_Restaurant', 'From_Hotel'] + IC_dest_PM.loc['To_Restaurant', 'From_Hotel'])/2
        IC_wkd2_hm_rest = IC_wkd2_hm_rest.values.reshape(-1, 1)
        IC_wkd_hotel_restaurant= np.minimum(IC_wkd1_hm_rest, IC_wkd2_hm_rest).astype(int)
        
        IC_wkd3_hm_rest = df_hotel['Wkd Enter'] * (IC_dest_AM.loc['To_Hotel', 'From_Restaurant'] + IC_dest_PM.loc['To_Hotel', 'From_Restaurant'])/2
        IC_wkd4_hm_rest = df_restaurant['Wkd Exit'] * (IC_ori_AM.loc['From_Restaurant', 'To_Hotel'] + IC_ori_PM.loc['From_Restaurant', 'To_Hotel'])/2
        IC_wkd3_hm_rest = np.full((len(IC_wkd4_hm_rest), 1), IC_wkd3_hm_rest.values)
        IC_wkd4_hm_rest = IC_wkd4_hm_rest.values.reshape(-1, 1)
        IC_wkd_restaurant_hotel = np.minimum(IC_wkd3_hm_rest, IC_wkd4_hm_rest).astype(int)
        IC_wkd_tot_hm_rest = IC_wkd_hotel_restaurant + IC_wkd_restaurant_hotel
        
#------------------------------------------------------------------------------------------------------------------
        # Store all IC values into one table
        # Create dataframe for storing IC estimates in the wkd
        data_IC_wkd = {'From Hotel to Restaurant': int(IC_wkd1_hm_rest), 
                      'To Restaurant from Hotel': int(IC_wkd2_hm_rest), 
                      'Hotel Exit/Restaurant Enter': int(IC_wkd_hotel_restaurant),
                      'To Hotel from Restaurant': int(IC_wkd3_hm_rest), 
                      'From Restaurant to Hotel': int(IC_wkd4_hm_rest), 
                      'Hotel Enter/Restaurant Exit': int(IC_wkd_restaurant_hotel)
                     }
        df_IC_wkd = pd.DataFrame(data_IC_wkd, index = [0])
        df_IC_wkd['Trip Interchange'] = 'Weekday'
        
        # Create dataframe for storing IC estimates in the AM
        data_IC_AM = {'From Hotel to Restaurant': math.ceil(IC_AM1_hm_rest), 
                      'To Restaurant from Hotel': math.ceil(IC_AM2_hm_rest), 
                      'Hotel Exit/Restaurant Enter': int(IC_AM_hotel_restaurant),
                      'To Hotel from Restaurant': math.ceil(IC_AM3_hm_rest), 
                      'From Restaurant to Hotel': math.ceil(IC_AM4_hm_rest), 
                      'Hotel Enter/Restaurant Exit': int(IC_AM_restaurant_hotel)
                     }
        df_IC_AM = pd.DataFrame(data_IC_AM, index = [0])
        df_IC_AM['Trip Interchange'] = 'AM Peak Hour'
        
        # Create dataframe for storing IC estimates in the PM
        data_IC_PM = {'From Hotel to Restaurant': int(IC_PM1_hm_rest), 
                      'To Restaurant from Hotel': int(IC_PM2_hm_rest), 
                      'Hotel Exit/Restaurant Enter': int(IC_PM_hotel_restaurant),
                      'To Hotel from Restaurant': int(IC_PM3_hm_rest), 
                      'From Restaurant to Hotel': int(IC_PM4_hm_rest), 
                      'Hotel Enter/Restaurant Exit': int(IC_PM_restaurant_hotel)
                     }
        df_IC_PM = pd.DataFrame(data_IC_PM, index = [0])
        df_IC_PM['Trip Interchange'] = 'PM Peak Hour'
        
        # Combine the two dataframes
        df_IC_combined = pd.concat([df_IC_wkd, df_IC_AM, df_IC_PM], ignore_index=True)
        
        # Reorder the columns to move 'Condition' to the first position
        columns_order = ['Trip Interchange'] + [col for col in df_IC_combined.columns if col != 'Trip Interchange']
        df_IC_combined = df_IC_combined[columns_order]

        df_IC_combined.to_csv('Internal Capture.csv', index = False)
        
        # Save to .xlsx file
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        fixed_filename = "Internal Capture"
        output_path = fr'C:\Users\Wang Xi\Desktop\Wang Xi\Python projects\Output\{fixed_filename}_{current_time}.xlsx' # xlsx has to have index because it is a multi-level index
        df_IC_combined.to_excel(output_path)
        # df_IC.to_excel(f"{fixed_filename}_{current_time}.xlsx")
#---------------------------------------------------------------------------------------------------------------------

        # Calculate external trips
        N3 = len(df_restaurant.index)
        N4 = len(df_hotel.index)
        N5 = len(df_other.index)
        ext_PM_restaurant_enter = []
        ext_PM_restaurant_exit = []
        ext_PM_hotel_enter = []
        ext_PM_hotel_exit = []
        ext_PM_other_enter = []
        ext_PM_other_exit = []
        ext_AM_restaurant_enter = []
        ext_AM_restaurant_exit = []
        ext_AM_hotel_enter = []
        ext_AM_hotel_exit = []
        ext_AM_other_enter = []
        ext_AM_other_exit = []
        ext_wkd_restaurant_enter = []
        ext_wkd_restaurant_exit = []
        ext_wkd_hotel_enter = []
        ext_wkd_hotel_exit = []
        ext_wkd_other_enter = []
        ext_wkd_other_exit = []
  
        # Calculating Hotel External
        # PM
        ext_PM_hotel_in = df_hotel['PM Enter'] - np.sum(IC_PM_restaurant_hotel, axis=0) # the summation is done column-wise; the sum of all the values in the same column;
        ext_PM_hotel_out = df_hotel['PM Exit'] - np.sum(IC_PM_hotel_restaurant, axis=0)
        ext_PM_hotel_enter.append(ext_PM_hotel_in)
        ext_PM_hotel_exit.append(ext_PM_hotel_out)
        # AM
        ext_AM_hotel_in = df_hotel['AM Enter'] - np.sum(IC_AM_restaurant_hotel, axis=0)
        ext_AM_hotel_out = df_hotel['AM Exit'] - np.sum(IC_AM_hotel_restaurant, axis=0)
        ext_AM_hotel_enter.append(ext_AM_hotel_in)
        ext_AM_hotel_exit.append(ext_AM_hotel_out)
        # Wkd
        ext_wkd_hotel_in = df_hotel['Wkd Enter'] - np.sum(IC_wkd_restaurant_hotel, axis=0)
        ext_wkd_hotel_out = df_hotel['Wkd Exit'] - np.sum(IC_wkd_hotel_restaurant, axis=0)
        ext_wkd_hotel_enter.append(ext_wkd_hotel_in)
        ext_wkd_hotel_exit.append(ext_wkd_hotel_out)
        
        ext_PM_hotel_tot = sum(ext_PM_hotel_enter) + sum(ext_PM_hotel_exit)
        ext_AM_hotel_tot = sum(ext_AM_hotel_enter) + sum(ext_AM_hotel_exit)
        ext_wkd_hotel_tot = sum(ext_wkd_hotel_enter) + sum(ext_wkd_hotel_exit)
        
        # Calculating Restaurant External
        # PM
        ext_PM_restaurant_in = df_restaurant['PM Enter'] - np.sum(IC_PM_hotel_restaurant, axis=0) # the summation is done column-wise; the sum of all the values in the same column;
        ext_PM_restaurant_out = df_restaurant['PM Exit'] - np.sum(IC_PM_restaurant_hotel, axis=0)
        ext_PM_restaurant_enter.append(ext_PM_restaurant_in)
        ext_PM_restaurant_exit.append(ext_PM_restaurant_out)
        # AM
        ext_AM_restaurant_in = df_restaurant['AM Enter'] - np.sum(IC_AM_hotel_restaurant, axis=0)
        ext_AM_restaurant_out = df_restaurant['AM Exit'] - np.sum(IC_AM_restaurant_hotel, axis=0)
        ext_AM_restaurant_enter.append(ext_AM_restaurant_in)
        ext_AM_restaurant_exit.append(ext_AM_restaurant_out)
        # Wkd
        ext_wkd_restaurant_in = df_restaurant['Wkd Enter'] - np.sum(IC_wkd_hotel_restaurant, axis=0)
        ext_wkd_restaurant_out = df_restaurant['Wkd Exit'] - np.sum(IC_wkd_restaurant_hotel, axis=0)
        ext_wkd_restaurant_enter.append(ext_wkd_restaurant_in)
        ext_wkd_restaurant_exit.append(ext_wkd_restaurant_out)
        
        ext_PM_restaurant_tot = sum(ext_PM_restaurant_enter) + sum(ext_PM_restaurant_exit)
        ext_AM_restaurant_tot = sum(ext_AM_restaurant_enter) + sum(ext_AM_restaurant_exit)
        ext_wkd_restaurant_tot = sum(ext_wkd_restaurant_enter) + sum(ext_wkd_restaurant_exit)
        
        # Calculating Other External
        # PM
        ext_PM_other_in = df_other['PM Enter']
        ext_PM_other_out = df_other['PM Exit']
        ext_PM_other_enter.append(ext_PM_other_in)
        ext_PM_other_exit.append(ext_PM_other_out)
        
        # AM
        ext_AM_other_in = df_other['AM Enter']
        ext_AM_other_out = df_other['AM Exit']
        ext_AM_other_enter.append(ext_AM_other_in)
        ext_AM_other_exit.append(ext_AM_other_out)
        
        # Wkd
        ext_wkd_other_in = df_other['Wkd Enter']
        ext_wkd_other_out = df_other['Wkd Exit']
        ext_wkd_other_enter.append(ext_wkd_other_in)
        ext_wkd_other_exit.append(ext_wkd_other_out)
        
        ext_PM_other_tot = sum(ext_PM_other_enter) + sum(ext_PM_other_exit)
        ext_AM_other_tot = sum(ext_AM_other_enter) + sum(ext_AM_other_exit)
        ext_wkd_other_tot = sum(ext_wkd_other_enter) + sum(ext_wkd_other_exit)

        
        # Print individual values in 'External Restaurant Enter'
        for ext_PM_restaurant_enter_i in ext_PM_restaurant_enter:
            ext_PM_restaurant_enter_i
        for ext_AM_restaurant_enter_i in ext_AM_restaurant_enter:
            ext_AM_restaurant_enter_i
        for ext_wkd_restaurant_enter_i in ext_wkd_restaurant_enter:
            ext_wkd_restaurant_enter_i
            
        # Print individual values in 'External Restaurant Exit'
        for ext_PM_restaurant_exit_i in ext_PM_restaurant_exit:
            ext_PM_restaurant_exit_i
        for ext_AM_restaurant_exit_i in ext_AM_restaurant_exit:
            ext_AM_restaurant_exit_i
        for ext_wkd_restaurant_exit_i in ext_wkd_restaurant_exit:
            ext_wkd_restaurant_exit_i
            
        # Print individual values in 'External Hotel Enter'
        for ext_PM_hotel_enter_i in ext_PM_hotel_enter:
            ext_PM_hotel_enter_i
        for ext_AM_hotel_enter_i in ext_AM_hotel_enter:
            ext_AM_hotel_enter_i
        for ext_wkd_hotel_enter_i in ext_wkd_hotel_enter:
            ext_wkd_hotel_enter_i
            
        # Print individual values in 'External Hotel Exit'
        for ext_PM_hotel_exit_i in ext_PM_hotel_exit:
            ext_PM_hotel_exit_i
        for ext_AM_hotel_exit_i in ext_AM_hotel_exit:
            ext_AM_hotel_exit_i
        for ext_wkd_hotel_exit_i in ext_wkd_hotel_exit:
            ext_wkd_hotel_exit_i
            
        # Print individual values in 'External Other Enter'
        for ext_PM_other_enter_i in ext_PM_other_enter:
            ext_PM_other_enter_i
        for ext_AM_other_enter_i in ext_AM_other_enter:
            ext_AM_other_enter_i
        for ext_wkd_other_enter_i in ext_wkd_other_enter:
            ext_wkd_other_enter_i
            
        # Print individual values in 'External Other Exit'
        for ext_PM_other_exit_i in ext_PM_other_exit:
            ext_PM_other_exit_i
        for ext_AM_other_exit_i in ext_AM_other_exit:
            ext_AM_other_exit_i
        for ext_wkd_other_exit_i in ext_wkd_other_exit:
            ext_wkd_other_exit_i
                  
# =============================================================================
#         # Calculating Restaurant External
#         # PM
#         ext_PM_restaurant_in = df_restaurant['PM Enter'].values.reshape(-1, 1) - IC_PM_retail_restaurant # reshape the array from (2, ) to (2, 1)
#         # IC_PM_retail_residential.flatten(): convert 2-dimensional array into 1-dimensional array, i.e., from (2, 1) to (2, ). 2D array is the presence of rows and columns. 1D array is a single-column array or a single-row array.
#         ext_PM_restaurant_out = df_restaurant['PM Exit'].values.reshape(-1, 1) - IC_PM_restaurant_retail
#         
#         # AM
#         ext_AM_restaurant_in = df_restaurant['AM Enter'].values.reshape(-1, 1) - IC_AM_retail_restaurant
#         ext_AM_restaurant_out = df_restaurant['AM Exit'].values.reshape(-1, 1) - IC_AM_restaurant_retail
#         
#         # Wkd
#         ext_wkd_restaurant_in = df_restaurant['Wkd Enter'].values.reshape(-1, 1) - IC_wkd_retail_restaurant
#         ext_wkd_restaurant_out = df_restaurant['Wkd Exit'].values.reshape(-1, 1) - IC_wkd_restaurant_retail
#         
#         ext_PM_restaurant_tot = ext_PM_restaurant_in + ext_PM_restaurant_out
#         ext_AM_restaurant_tot = ext_AM_restaurant_in + ext_AM_restaurant_out
#         ext_wkd_restaurant_tot = ext_wkd_restaurant_in + ext_wkd_restaurant_out
# =============================================================================

        # Create a list to store new row data
        new_rows = []

        # Insert a row at an arbitrary position in a DataFrame based on the condition of the column range falling within one data range
        # Create the new row data
        
        # Get unique LUC values from df_other
        unique_other_luc_values = df_other['LUC'].unique()
        for i, luc_value in enumerate(unique_other_luc_values):
            dir_row_other = {'ITE Land Use': "", 
                            'LUC': luc_value,
                            'Size': "",
                            'Unit': "",
                            'Weekday': "", 'AM Peak Hour': "", 'PM Peak Hour': "", 
                            'Trips': 'Directional Distribution',
                            'Wkd Enter': dir_dist_perc['other'][str(unique_other_luc_values[i])]['Wkd Enter'],
                            'Wkd Exit': dir_dist_perc['other'][str(unique_other_luc_values[i])]['Wkd Exit'],
                            'Wkd Total': dir_dist_perc['other'][str(unique_other_luc_values[i])]['Wkd Total'], 
                            'AM Enter': dir_dist_perc['other'][str(unique_other_luc_values[i])]['AM Enter'], 
                            'AM Exit': dir_dist_perc['other'][str(unique_other_luc_values[i])]['AM Exit'],
                            'AM Total': dir_dist_perc['other'][str(unique_other_luc_values[i])]['AM Total'],  
                            'PM Enter': dir_dist_perc['other'][str(unique_other_luc_values[i])]['PM Enter'], 
                            'PM Exit': dir_dist_perc['other'][str(unique_other_luc_values[i])]['PM Exit'],
                            'PM Total': dir_dist_perc['other'][str(unique_other_luc_values[i])]['PM Total']}
            new_rows.append(dir_row_other)
            
            # Store the total trips into external when there is no IC or PB
            external_row_other = {'ITE Land Use': "", 
                            'LUC': luc_value,   
                            'Size': "",
                            'Unit': "",
                            'Weekday': "", 'AM Peak Hour': "", 'PM Peak Hour': "", 
                            'Trips': 'External',
                            'Wkd Enter': sum(ext_wkd_other_enter_i), 
                            'Wkd Exit': sum(ext_wkd_other_exit_i), 
                            'Wkd Total': sum(ext_wkd_other_tot),
                            'AM Enter': sum(ext_AM_other_enter_i), 
                            'AM Exit': sum(ext_AM_other_exit_i),  
                            'AM Total': sum(ext_AM_other_tot),   
                            'PM Enter': sum(ext_PM_other_enter_i), 
                            'PM Exit': sum(ext_PM_other_exit_i), 
                            'PM Total': sum(ext_PM_other_tot)}
            new_rows.append(external_row_other)
                      
        # Get unique LUC values from df_hotel
        unique_hm_luc_values = df_hotel['LUC'].unique()
        for i, luc_value in enumerate(unique_hm_luc_values):
            dir_row_hotel = {'ITE Land Use': "", 
                            'LUC': luc_value,
                            'Size': "",
                            'Unit': "",
                            'Weekday': "", 'AM Peak Hour': "", 'PM Peak Hour': "", 
                            'Trips': 'Directional Distribution',
                            'Wkd Enter': dir_dist_perc['hotel'][str(unique_hm_luc_values[i])]['Wkd Enter'],
                            'Wkd Exit': dir_dist_perc['hotel'][str(unique_hm_luc_values[i])]['Wkd Exit'],
                            'Wkd Total': dir_dist_perc['hotel'][str(unique_hm_luc_values[i])]['Wkd Total'], 
                            'AM Enter': dir_dist_perc['hotel'][str(unique_hm_luc_values[i])]['AM Enter'], 
                            'AM Exit': dir_dist_perc['hotel'][str(unique_hm_luc_values[i])]['AM Exit'],
                            'AM Total': dir_dist_perc['hotel'][str(unique_hm_luc_values[i])]['AM Total'],  
                            'PM Enter': dir_dist_perc['hotel'][str(unique_hm_luc_values[i])]['PM Enter'], 
                            'PM Exit': dir_dist_perc['hotel'][str(unique_hm_luc_values[i])]['PM Exit'],
                            'PM Total': dir_dist_perc['hotel'][str(unique_hm_luc_values[i])]['PM Total']}
            new_rows.append(dir_row_hotel)
            
            internal_row_hotel = {'ITE Land Use': "", 
                            'LUC': luc_value,
                            'Size': "",
                            'Unit': "",
                            'Weekday': "", 'AM Peak Hour': "", 'PM Peak Hour': "", 
                            'Trips': 'Internal',
                            'Wkd Enter': sum(np.sum(IC_wkd_restaurant_hotel, axis = 0)),
                            'Wkd Exit': sum(np.sum(IC_wkd_hotel_restaurant, axis = 0)),
                            'Wkd Total': sum(np.sum(IC_wkd_tot_hm_rest, axis = 0)), 
                            'AM Enter': sum(np.sum(IC_AM_restaurant_hotel, axis = 0)), 
                            'AM Exit': sum(np.sum(IC_AM_hotel_restaurant, axis = 0)), 
                            'AM Total': sum(np.sum(IC_AM_tot_hm_rest, axis = 0)),   
                            'PM Enter': sum(np.sum(IC_PM_restaurant_hotel, axis = 0)), 
                            'PM Exit': sum(np.sum(IC_PM_hotel_restaurant, axis = 0)), 
                            'PM Total': sum(np.sum(IC_PM_tot_hm_rest, axis = 0))}
            new_rows.append(internal_row_hotel)
            
            # Create the new row data
            external_row_hotel = {'ITE Land Use': "", 
                            'LUC': luc_value,   
                            'Size': "",
                            'Unit': "",
                            'Weekday': "", 'AM Peak Hour': "", 'PM Peak Hour': "", 
                            'Trips': 'External',
                            'Wkd Enter': sum(ext_wkd_hotel_enter_i), 
                            'Wkd Exit': sum(ext_wkd_hotel_exit_i), 
                            'Wkd Total': sum(ext_wkd_hotel_tot),
                            'AM Enter': sum(ext_AM_hotel_enter_i), 
                            'AM Exit': sum(ext_AM_hotel_exit_i),  
                            'AM Total': sum(ext_AM_hotel_tot),   
                            'PM Enter': sum(ext_PM_hotel_enter_i), 
                            'PM Exit': sum(ext_PM_hotel_exit_i), 
                            'PM Total': sum(ext_PM_hotel_tot)}
            new_rows.append(external_row_hotel)

        # Find the index where the new row should be inserted
        # insert_index = df_clear.index[(df_clear['LUC'].astype(int) <= 800) & (df_clear['LUC'].astype(int) >= 200)].tolist()[1]

        # Insert the new row at the specified index
        # df_IC = df_clear.append(new_row_data, ignore_index=True)

        # Create the new row data
        # Get unique LUC values from df_restaurant
        unique_rest_luc_values = df_restaurant['LUC'].unique()
        for i, luc_value in enumerate(unique_rest_luc_values):
            dir_row_restaurant = {'ITE Land Use': "", 
                            'LUC': luc_value,
                            'Size': "",
                            'Unit': "",
                            'Weekday': "", 'AM Peak Hour': "", 'PM Peak Hour': "", 
                            'Trips': 'Directional Distribution',
                            'Wkd Enter': dir_dist_perc['restaurant'][str(unique_rest_luc_values[i])]['Wkd Enter'],
                            'Wkd Exit': dir_dist_perc['restaurant'][str(unique_rest_luc_values[i])]['Wkd Exit'],
                            'Wkd Total': dir_dist_perc['restaurant'][str(unique_rest_luc_values[i])]['Wkd Total'], 
                            'AM Enter': dir_dist_perc['restaurant'][str(unique_rest_luc_values[i])]['AM Enter'], 
                            'AM Exit': dir_dist_perc['restaurant'][str(unique_rest_luc_values[i])]['AM Exit'],
                            'AM Total': dir_dist_perc['restaurant'][str(unique_rest_luc_values[i])]['AM Total'],  
                            'PM Enter': dir_dist_perc['restaurant'][str(unique_rest_luc_values[i])]['PM Enter'], 
                            'PM Exit': dir_dist_perc['restaurant'][str(unique_rest_luc_values[i])]['PM Exit'],
                            'PM Total': dir_dist_perc['restaurant'][str(unique_rest_luc_values[i])]['PM Total']}
            new_rows.append(dir_row_restaurant)
            
            internal_row_restaurant = {'ITE Land Use': "", 
                            'LUC': luc_value, 
                            'Size': "",
                            'Unit': "",
                            'Weekday': "", 'AM Peak Hour': "", 'PM Peak Hour': "", 
                            'Trips': 'Internal',
                            'Wkd Enter': sum(IC_wkd_hotel_restaurant[i]),
                            'Wkd Exit': sum(IC_wkd_restaurant_hotel[i]), 
                            'Wkd Total': sum(IC_wkd_tot_hm_rest[i]),
                            'AM Enter': sum(IC_AM_hotel_restaurant[i]),
                            'AM Exit': sum(IC_AM_restaurant_hotel[i]), 
                            'AM Total': sum(IC_AM_tot_hm_rest[i]),  
                            'PM Enter': sum(IC_PM_hotel_restaurant[i]),
                            'PM Exit': sum(IC_PM_restaurant_hotel[i]), 
                            'PM Total': sum(IC_PM_tot_hm_rest[i])}
            new_rows.append(internal_row_restaurant)

            # Create the new row data
            external_row_restaurant = {'ITE Land Use': "", 
                            'LUC': luc_value, 
                            'Size': "",
                            'Unit': "",
                            'Weekday': "", 'AM Peak Hour': "", 'PM Peak Hour': "", 
                            'Trips': 'External',
                            'Wkd Enter': sum(ext_wkd_restaurant_enter_i), 
                            'Wkd Exit': sum(ext_wkd_restaurant_exit_i), 
                            'Wkd Total': sum(ext_wkd_restaurant_tot),
                            'AM Enter': sum(ext_AM_restaurant_enter_i), 
                            'AM Exit': sum(ext_AM_restaurant_exit_i), 
                            'AM Total': sum(ext_AM_restaurant_tot),  
                            'PM Enter': sum(ext_PM_restaurant_enter_i), 
                            'PM Exit': sum(ext_PM_restaurant_exit_i), 
                            'PM Total': sum(ext_PM_restaurant_tot)}
            new_rows.append(external_row_restaurant)
        
        
        # Check if there are pass-by capture
        pass_by_restaurant_list = ['932', '934']
        item_list = LU
        
        def check_pass_by_rest (list_c):
            if any(item in item_list for item in list_c):
                print('*********************************************')
                print()
                print (" There are pass-by capture.")
                
                pass_by_rate_PM = input("What is the pass-by rate for the restaurant in the PM Peak Hour? (Please use 2 decimals instead of %) ")
                pass_by_rate_AM = input("What is the pass-by rate for the restaurant in the AM Peak Hour? (Please use 2 decimals instead of %) ")
                pass_by_rate_wkd = input("What is the pass-by rate for the restaurant on Weekday? (Please use 2 decimals instead of %) ")
                
                # PM
                pass_by_restaurant_enter_PMi = int(sum(ext_PM_restaurant_enter_i) * float(pass_by_rate_PM))
                pass_by_restaurant_exit_PMi = int(sum(ext_PM_restaurant_exit_i) * float(pass_by_rate_PM))
                pass_by_restaurant_tot_PMi = pass_by_restaurant_enter_PMi + pass_by_restaurant_exit_PMi
                net_ext_restaurant_enter_PMi = sum(ext_PM_restaurant_enter_i) - pass_by_restaurant_enter_PMi
                net_ext_restaurant_exit_PMi = sum(ext_PM_restaurant_exit_i) - pass_by_restaurant_exit_PMi
                net_ext_restaurant_tot_PMi = net_ext_restaurant_enter_PMi + net_ext_restaurant_exit_PMi
                
                # AM
                pass_by_restaurant_enter_AMi = int(sum(ext_AM_restaurant_enter_i) * float(pass_by_rate_AM))
                pass_by_restaurant_exit_AMi = int(sum(ext_AM_restaurant_exit_i) * float(pass_by_rate_AM))
                pass_by_restaurant_tot_AMi = pass_by_restaurant_enter_AMi + pass_by_restaurant_exit_AMi
                net_ext_restaurant_enter_AMi = sum(ext_AM_restaurant_enter_i) - pass_by_restaurant_enter_AMi
                net_ext_restaurant_exit_AMi = sum(ext_AM_restaurant_exit_i) - pass_by_restaurant_exit_AMi
                net_ext_restaurant_tot_AMi = net_ext_restaurant_enter_AMi + net_ext_restaurant_exit_AMi
                
                # wkd
                pass_by_restaurant_enter_wkdi = int(sum(ext_wkd_restaurant_enter_i) * float(pass_by_rate_wkd))
                pass_by_restaurant_exit_wkdi = int(sum(ext_wkd_restaurant_exit_i) * float(pass_by_rate_wkd))
                pass_by_restaurant_tot_wkdi = pass_by_restaurant_enter_wkdi + pass_by_restaurant_exit_wkdi
                net_ext_restaurant_enter_wkdi = sum(ext_wkd_restaurant_enter_i) - pass_by_restaurant_enter_wkdi
                net_ext_restaurant_exit_wkdi = sum(ext_wkd_restaurant_exit_i) - pass_by_restaurant_exit_wkdi
                net_ext_restaurant_tot_wkdi = net_ext_restaurant_enter_wkdi + net_ext_restaurant_exit_wkdi
                
                # Create the new row data
                pass_by_row_restaurant = {'ITE Land Use': "", 
                                'LUC': sum(df_restaurant['LUC']), # assume: only have one single retail land use within the project
                                'Size': "",
                                'Unit': "",
                                'Weekday': "", 'AM Peak Hour': "", 'PM Peak Hour': "", 
                                'Trips': 'Pass-by',
                                'Wkd Enter': pass_by_restaurant_enter_wkdi,
                                'Wkd Exit': pass_by_restaurant_exit_wkdi,
                                'Wkd Total': pass_by_restaurant_tot_wkdi,
                                'AM Enter': pass_by_restaurant_enter_AMi,
                                'AM Exit': pass_by_restaurant_exit_AMi,
                                'AM Total': pass_by_restaurant_tot_AMi,  
                                'PM Enter': pass_by_restaurant_enter_PMi,
                                'PM Exit': pass_by_restaurant_exit_PMi,
                                'PM Total': pass_by_restaurant_tot_PMi}
                new_rows.append(pass_by_row_restaurant)
                
                # Create the new row data
                net_external_row_restaurant = {'ITE Land Use': "", 
                                'LUC': sum(df_restaurant['LUC']), # assume: only have one single retail land use within the project
                                'Size': "",
                                'Unit': "",
                                'Weekday': "", 'AM Peak Hour': "", 'PM Peak Hour': "", 
                                'Trips': 'Net External',
                                'Wkd Enter': net_ext_restaurant_enter_wkdi,
                                'Wkd Exit': net_ext_restaurant_exit_wkdi,
                                'Wkd Total': net_ext_restaurant_tot_wkdi,
                                'AM Enter': net_ext_restaurant_enter_AMi,
                                'AM Exit': net_ext_restaurant_exit_AMi,
                                'AM Total': net_ext_restaurant_tot_AMi,  
                                'PM Enter': net_ext_restaurant_enter_PMi,
                                'PM Exit': net_ext_restaurant_exit_PMi,
                                'PM Total': net_ext_restaurant_tot_PMi}
                new_rows.append(net_external_row_restaurant)
                           
            print('*********************************************')
            print()
            
        
        check_pass_by_rest (pass_by_restaurant_list)
        
        # Find the index where the new row should be inserted
        # insert_index = df_clear.index[df_clear['LUC'].astype(int) >= 200].tolist()[-1] + 1 #insert row to the end

        # Insert the new row at the specified index
        df_IC = df_clear.append(new_rows, ignore_index=True)

        # Sort the DataFrame based on the 'LUC' column to maintain order
        df_IC = df_IC.sort_values(by='LUC', ignore_index=True)
        # print(df_IC)
        
        # Save to .csv file
        df_IC.to_csv('Trip Generation with IC.csv', index=False)
    
        
        # Initialize variables to store the calculated sums
        # Store into total trips
        total_values_1 = {}

        # Iterate through rows 
        for index, row in df_IC.iterrows():
            if "Total" in row['Trips']:
                for col in df_IC.columns:
                    if col in ['Wkd Enter']:
                        total_values_1[col] = total_values_1.get(col, 0) + row[col] # 'total_values.get(col, 0) ensures that if the key (column name) doesn't exist in the dictionary, it initializes it with a value of 0.
                    if col in ['Wkd Exit']:
                        total_values_1[col] = total_values_1.get(col, 0) + row[col]
                    if col in ['Wkd Total']:
                        total_values_1[col] = total_values_1.get(col, 0) + row[col]
                    if col in ['AM Enter']:
                        total_values_1[col] = total_values_1.get(col, 0) + row[col]
                    if col in ['AM Exit']:
                        total_values_1[col] = total_values_1.get(col, 0) + row[col]
                    if col in ['AM Total']:
                        total_values_1[col] = total_values_1.get(col, 0) + row[col]
                    if col in ['PM Enter']:
                        total_values_1[col] = total_values_1.get(col, 0) + row[col]
                    if col in ['PM Exit']:
                        total_values_1[col] = total_values_1.get(col, 0) + row[col]
                    if col in ['PM Total']:
                        total_values_1[col] = total_values_1.get(col, 0) + row[col]

        # Create a new row with "Total" values
        total_row1 = {'ITE Land Use': 'Total Land Use Property', 'Trips': 'Total Traffic', **total_values_1}

        # Append the new row to the DataFrame
        df_IC = df_IC.append(total_row1, ignore_index=True)
        
        # Initialize variables to store the calculated sums
        # Store into total internal trips
        total_values_2 = {}

        # Iterate through rows
        for index, row in df_IC.iterrows():
            if "Internal" in row['Trips']:
                for col in df_IC.columns:
                    if col in ['Wkd Enter']:
                        total_values_2[col] = total_values_2.get(col, 0) + row[col]
                    if col in ['Wkd Exit']:
                        total_values_2[col] = total_values_2.get(col, 0) + row[col]
                    if col in ['Wkd Total']:
                        total_values_2[col] = total_values_2.get(col, 0) + row[col]
                    if col in ['AM Enter']:
                        total_values_2[col] = total_values_2.get(col, 0) + row[col]
                    if col in ['AM Exit']:
                        total_values_2[col] = total_values_2.get(col, 0) + row[col]
                    if col in ['AM Total']:
                        total_values_2[col] = total_values_2.get(col, 0) + row[col]
                    if col in ['PM Enter']:
                        total_values_2[col] = total_values_2.get(col, 0) + row[col]
                    if col in ['PM Exit']:
                        total_values_2[col] = total_values_2.get(col, 0) + row[col]
                    if col in ['PM Total']:
                        total_values_2[col] = total_values_2.get(col, 0) + row[col]

        # Create a new row with "Total" values
        total_row2 = {'ITE Land Use': 'Total Land Use Property', 'Trips': 'Total Internal Capture', **total_values_2}

        # Append the new row to the DataFrame
        df_IC = df_IC.append(total_row2, ignore_index=True)
        
        # Initialize variables to store the calculated sums
        # Store into total external trips
        total_values_3 = {}

        # Iterate through rows
        for index, row in df_IC.iterrows():
            if row['Trips'].strip() == 'External': # to check for the exact math of "External", not include "Net External"
                for col in df_IC.columns:
                    if col in ['Wkd Enter']:
                        total_values_3[col] = total_values_3.get(col, 0) + row[col]
                    if col in ['Wkd Exit']:
                        total_values_3[col] = total_values_3.get(col, 0) + row[col]
                    if col in ['Wkd Total']:
                        total_values_3[col] = total_values_3.get(col, 0) + row[col]
                    if col in ['AM Enter']:
                        total_values_3[col] = total_values_3.get(col, 0) + row[col]
                    if col in ['AM Exit']:
                        total_values_3[col] = total_values_3.get(col, 0) + row[col]
                    if col in ['AM Total']:
                        total_values_3[col] = total_values_3.get(col, 0) + row[col]
                    if col in ['PM Enter']:
                        total_values_3[col] = total_values_3.get(col, 0) + row[col]
                    if col in ['PM Exit']:
                        total_values_3[col] = total_values_3.get(col, 0) + row[col]
                    if col in ['PM Total']:
                        total_values_3[col] = total_values_3.get(col, 0) + row[col]

        # Create a new row with "Total" values
        total_row3 = {'ITE Land Use': 'Total Land Use Property', 'Trips': 'Total External', **total_values_3}

        # Append the new row to the DataFrame
        df_IC = df_IC.append(total_row3, ignore_index=True)
        
        # Initialize variables to store the calculated sums
        # Store into total pass-by trips
        total_values_4 = {}

        # Iterate through rows
        for index, row in df_IC.iterrows():
            if "Pass-by" in row['Trips']:
                for col in df_IC.columns:
                    if col in ['Wkd Enter']:
                        total_values_4[col] = total_values_4.get(col, 0) + row[col]
                    if col in ['Wkd Exit']:
                        total_values_4[col] = total_values_4.get(col, 0) + row[col]
                    if col in ['Wkd Total']:
                        total_values_4[col] = total_values_4.get(col, 0) + row[col]
                    if col in ['AM Enter']:
                        total_values_4[col] = total_values_4.get(col, 0) + row[col]
                    if col in ['AM Exit']:
                        total_values_4[col] = total_values_4.get(col, 0) + row[col]
                    if col in ['AM Total']:
                        total_values_4[col] = total_values_4.get(col, 0) + row[col]
                    if col in ['PM Enter']:
                        total_values_4[col] = total_values_4.get(col, 0) + row[col]
                    if col in ['PM Exit']:
                        total_values_4[col] = total_values_4.get(col, 0) + row[col]
                    if col in ['PM Total']:
                        total_values_4[col] = total_values_4.get(col, 0) + row[col]

        # Create a new row with "Total" values
        total_row4 = {'ITE Land Use': 'Total Land Use Property', 'Trips': 'Total Pass-by Capture', **total_values_4}

        # Append the new row to the DataFrame
        df_IC = df_IC.append(total_row4, ignore_index=True)
        
        # Initialize variables to store the calculated net values
        # Store into total net external trips
        total_values_5 = {}

        # Iterate through rows
        for index, row in df_IC.iterrows():
            if row['Trips'].strip() in ['Total Traffic', 'Total Internal Capture', 'Total Pass-by Capture']: 
                for col in df_IC.columns:
                    if col in ['Wkd Enter', 'Wkd Exit', 'Wkd Total', 'AM Enter', 'AM Exit', 'AM Total', 'PM Enter', 'PM Exit', 'PM Total']:
                        if row['Trips'].strip() == 'Total Traffic':
                            total_values_5[col] = total_values_5.get(col, 0) + row[col]
                        elif row['Trips'].strip() == 'Total Internal Capture':
                            total_values_5[col] -= row[col]
                        elif row['Trips'].strip() == 'Total Pass-by Capture':
                            total_values_5[col] -= row[col]
                        
        # Create a new row with "Total" values
        total_row5 = {'ITE Land Use': 'Total Land Use Property','Trips': 'Total Net External', **total_values_5}

        # Append the new row to the DataFrame
        df_IC = df_IC.append(total_row5, ignore_index=True)
  
        
        # Initialize variables to store the calculated total internal capture percentage
        total_values_6 = {}

        # Iterate through rows
        for index, row in df_IC.iterrows():
            if row['Trips'].strip() in ['Total Traffic', 'Total Internal Capture']: 
                for col in df_IC.columns:
                    if col in ['Wkd Total', 'AM Total', 'PM Total']:
                        if row['Trips'].strip() == 'Total Traffic':
                            total_values_6[col] = total_values_6.get(col, 0) + row[col]
                        elif row['Trips'].strip() == 'Total Internal Capture':
                            total_values_6[col] = row[col] / total_values_6[col]
        
        # Format the calculated percentages with two decimal places
        for col in total_values_6:
            total_values_6[col] = "{:.2%}".format(total_values_6[col])
                        
        # Create a new row with "Total" values
        total_row6 = {'ITE Land Use': 'Total Land Use Property','Trips': 'Internal Capture Percent', **total_values_6}

        # Append the new row to the DataFrame
        df_IC = df_IC.append(total_row6, ignore_index=True)
 
        
        # Initialize variables to store the calculated total pass-by capture percentage
        total_values_7 = {}

        # Iterate through rows
        for index, row in df_IC.iterrows():
            if row['Trips'].strip() in ['Total External', 'Total Pass-by Capture']: 
                for col in df_IC.columns:
                    if col in ['Wkd Total', 'AM Total', 'PM Total']:
                        if row['Trips'].strip() == 'Total External':
                            total_values_7[col] = total_values_7.get(col, 0) + row[col]
                        elif row['Trips'].strip() == 'Total Pass-by Capture':
                            total_values_7[col] = row[col] / total_values_7[col]
        
        # Format the calculated percentages with two decimal places
        for col in total_values_7:
            total_values_7[col] = "{:.2%}".format(total_values_7[col])
                        
        # Create a new row with "Total" values
        total_row7 = {'ITE Land Use': 'Total Land Use Property','Trips': 'Pass-by Capture Percent', **total_values_7}

        # Append the new row to the DataFrame
        df_IC = df_IC.append(total_row7, ignore_index=True)
        
        # Adding multi-level column names for the output
        df_IC.columns = pd.MultiIndex.from_tuples(
            [('Development', 'ITE Land Use'), ('Development', 'LUC'),
             ('Measurement', 'Size'), ('Measurement', 'Unit'), 
             ('Measurement', 'Weekday'), ('Measurement', 'AM Peak Hour'), ('Measurement', 'PM Peak Hour'), ('Measurement', 'Trips'),
             ('Daily Traffic', 'Wkd Enter'), ('Daily Traffic', 'Wkd Exit'), ('Daily Traffic', 'Wkd Total'),
             ('AM Peak Hour Traffic', 'AM Enter'), ('AM Peak Hour Traffic', 'AM Exit'), ('AM Peak Hour Traffic', 'AM Total'),
             ('PM Peak Hour Traffic', 'PM Enter'), ('PM Peak Hour Traffic', 'PM Exit'), ('PM Peak Hour Traffic', 'PM Total'), ]
            )
        
        # Adding notes
        # it is selective to add footnotes at the bottom of dataframe

        # Save to .csv file
        df_IC.to_csv('Trip Generation with IC.csv', index = False) # csv doesn't have to have index
        
        # Save to .xlsx file
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        fixed_filename = "Trip Generation with IC"
        output_path = fr'C:\Users\Wang Xi\Desktop\Wang Xi\Python projects\Output\{fixed_filename}_{current_time}.xlsx' # xlsx has to have index because it is a multi-level index
        df_IC.to_excel(output_path)
        # df_IC.to_excel(f"{fixed_filename}_{current_time}.xlsx") 
        
        print()
        print('Trip generation with internal capture and external trips spreadsheet is successfully saved')
        print('*********************************************')
        print()
        
def check_crosslists_not_empty_resi_ret (list_a, list_b):    
    if any(item is not None for item in list_a) and any(item is not None for item in list_b):
        print (" There exists Internal Capture between the residential and retail in a mixed-use development.")
        
        # calculate the minimun IC from retail to residential in the PM Peak Hour
        IC_PM1_resi_ret = df_retail['PM Exit'] * IC_ori_PM.loc['From_Retail', 'To_Residential']
        IC_PM2_resi_ret = df_residential['PM Enter'] * IC_dest_PM.loc['To_Residential', 'From_Retail']
        
        # In this example, 
        # np.full is used to create a matrix with the specified scalar value repeated in each row. 
        # The (array_length, 1) shape indicates that the matrix should have array_length rows and 1 column.
        # IC_PM1 = IC_PM1.to_numpy().reshape(-1, 1) # same as IC_PM1 = IC_PM1.values.reshape(-1, 1), convert IC_PM1 to a numpy array with shape (n, 1)
        IC_PM1_resi_ret = np.full((len(IC_PM2_resi_ret), 1), IC_PM1_resi_ret.values)
              
        # create a NumPy array from a Pandas Series, and then reshape array to one column two rows array
        IC_PM2_resi_ret = IC_PM2_resi_ret.values.reshape(-1, 1)
        
        # select the minimum value between arrays element-wise, row by row. And only take integer from the floating point (decimal) number.
        IC_PM_retail_residential = np.minimum(IC_PM1_resi_ret, IC_PM2_resi_ret).astype(int)
        
        
        # calculate the minimun IC from residential to retail in the PM Peak Hour
        IC_PM3_resi_ret = df_retail['PM Enter'] * IC_dest_PM.loc['To_Retail', 'From_Residential']
        IC_PM4_resi_ret = df_residential['PM Exit'] * IC_ori_PM.loc['From_Residential', 'To_Retail']
        # IC_PM3 = IC_PM3.to_numpy().reshape(-1, 1) 
        # IC_PM4 = IC_PM4.to_numpy().reshape(-1, 1)
        IC_PM3_resi_ret = np.full((len(IC_PM4_resi_ret), 1), IC_PM3_resi_ret.values)
        IC_PM4_resi_ret = IC_PM4_resi_ret.values.reshape(-1, 1)
        IC_PM_residential_retail = np.minimum(IC_PM3_resi_ret, IC_PM4_resi_ret).astype(int) # only take integer from the floating point number.
        
            
        # calculate the total IC between retail and residential in the PM Peak Hour
        IC_PM_tot_resi_ret = IC_PM_retail_residential + IC_PM_residential_retail
        # print (IC_PM_retail_residential, IC_PM_residential_retail, IC_PM_tot)

        # AM
        IC_AM1_resi_ret = df_retail['AM Exit'] * IC_ori_AM.loc['From_Retail', 'To_Residential']
        IC_AM2_resi_ret = df_residential['AM Enter'] * IC_dest_AM.loc['To_Residential', 'From_Retail']
        IC_AM1_resi_ret = np.full((len(IC_AM2_resi_ret), 1), IC_AM1_resi_ret.values)
        IC_AM2_resi_ret = IC_AM2_resi_ret.values.reshape(-1, 1)
        IC_AM_retail_residential= math.ceil(np.minimum(IC_AM1_resi_ret, IC_AM2_resi_ret))
        IC_AM_retail_residential = np.array([IC_AM_retail_residential])
        IC_AM_retail_residential = IC_AM_retail_residential.reshape(1,1)
        
        IC_AM3_resi_ret = df_retail['AM Enter'] * IC_dest_AM.loc['To_Retail', 'From_Residential']
        IC_AM4_resi_ret = df_residential['AM Exit'] * IC_ori_AM.loc['From_Residential', 'To_Retail']
        IC_AM3_resi_ret = np.full((len(IC_AM4_resi_ret), 1), IC_AM3_resi_ret.values)
        IC_AM4_resi_ret = IC_AM4_resi_ret.values.reshape(-1, 1)
        IC_AM_residential_retail = math.ceil(np.minimum(IC_AM3_resi_ret, IC_AM4_resi_ret))
        IC_AM_residential_retail = np.array([IC_AM_residential_retail])
        IC_AM_residential_retail = IC_AM_residential_retail.reshape(1,1)
        IC_AM_tot_resi_ret = IC_AM_retail_residential + IC_AM_residential_retail
        # print (IC_AM_retail_residential, IC_AM_residential_retail, IC_AM_tot)

        # Wkd
        IC_wkd1_resi_ret = df_retail['Wkd Exit'] * (IC_ori_AM.loc['From_Retail', 'To_Residential'] + IC_ori_PM.loc['From_Retail', 'To_Residential'])/2
        IC_wkd2_resi_ret = df_residential['Wkd Enter'] * (IC_dest_AM.loc['To_Residential', 'From_Retail'] + IC_dest_PM.loc['To_Residential', 'From_Retail'])/2
        IC_wkd1_resi_ret = np.full((len(IC_wkd2_resi_ret), 1), IC_wkd1_resi_ret.values)
        IC_wkd2_resi_ret = IC_wkd2_resi_ret.values.reshape(-1, 1)
        IC_wkd_retail_residential= np.minimum(IC_wkd1_resi_ret, IC_wkd2_resi_ret).astype(int)
        
        IC_wkd3_resi_ret = df_retail['Wkd Enter'] * (IC_dest_AM.loc['To_Retail', 'From_Residential'] + IC_dest_PM.loc['To_Retail', 'From_Residential'])/2
        IC_wkd4_resi_ret = df_residential['Wkd Exit'] * (IC_ori_AM.loc['From_Residential', 'To_Retail'] + IC_ori_PM.loc['From_Residential', 'To_Retail'])/2
        IC_wkd3_resi_ret = np.full((len(IC_wkd4_resi_ret), 1), IC_wkd3_resi_ret.values)
        IC_wkd4_resi_ret = IC_wkd4_resi_ret.values.reshape(-1, 1)
        IC_wkd_residential_retail = np.minimum(IC_wkd3_resi_ret, IC_wkd4_resi_ret).astype(int)
        IC_wkd_tot_resi_ret = IC_wkd_retail_residential + IC_wkd_residential_retail
        # print (IC_wkd_retail_residential, IC_wkd_residential_retail, IC_wkd_tot)
        
#------------------------------------------------------------------------------------------------------------------
        # Store all IC values into one table
        # Create dataframe for storing IC estimates in the wkd
        data_IC_wkd = {
                      'From Retail to Residential': int(IC_wkd1_resi_ret), 
                      'To Residential from Retail': int(IC_wkd2_resi_ret), 
                      'Retail Exit/Residential Enter': int(IC_wkd_retail_residential),
                      'To Retail from Residential': int(IC_wkd3_resi_ret), 
                      'From Residential to Retail': int(IC_wkd4_resi_ret), 
                      'Retail Enter/Residential Exit': int(IC_wkd_residential_retail)
                     }
        df_IC_wkd = pd.DataFrame(data_IC_wkd, index = [0])
        df_IC_wkd['Trip Interchange'] = 'Weekday'
        
        # Create dataframe for storing IC estimates in the AM
        data_IC_AM = {'From Retail to Residential': math.ceil(IC_AM1_resi_ret), 
                      'To Residential from Retail': math.ceil(IC_AM2_resi_ret), 
                      'Retail Exit/Residential Enter': math.ceil(IC_AM_retail_residential),
                      'To Retail from Residential': math.ceil(IC_AM3_resi_ret), 
                      'From Residential to Retail': math.ceil(IC_AM4_resi_ret), 
                      'Retail Enter/Residential Exit': math.ceil(IC_AM_residential_retail)
                     }
        df_IC_AM = pd.DataFrame(data_IC_AM, index = [0])
        df_IC_AM['Trip Interchange'] = 'AM Peak Hour'
        
        # Create dataframe for storing IC estimates in the PM
        data_IC_PM = {'From Retail to Residential': int(IC_PM1_resi_ret), 
                      'To Residential from Retail': int(IC_PM2_resi_ret), 
                      'Retail Exit/Residential Enter': int(IC_PM_retail_residential),
                      'To Retail from Residential': int(IC_PM3_resi_ret), 
                      'From Residential to Retail': int(IC_PM4_resi_ret), 
                      'Retail Enter/Residential Exit': int(IC_PM_residential_retail)
                     }
        df_IC_PM = pd.DataFrame(data_IC_PM, index = [0])
        df_IC_PM['Trip Interchange'] = 'PM Peak Hour'
        
        # Combine the two dataframes
        df_IC_combined = pd.concat([df_IC_wkd, df_IC_AM, df_IC_PM], ignore_index=True)
        
        # Reorder the columns to move 'Condition' to the first position
        columns_order = ['Trip Interchange'] + [col for col in df_IC_combined.columns if col != 'Trip Interchange']
        df_IC_combined = df_IC_combined[columns_order]

        df_IC_combined.to_csv('Internal Capture.csv', index = False)
        
        # Save to .xlsx file
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        fixed_filename = "Internal Capture"
        output_path = fr'C:\Users\Wang Xi\Desktop\Wang Xi\Python projects\Output\{fixed_filename}_{current_time}.xlsx' # xlsx has to have index because it is a multi-level index
        df_IC_combined.to_excel(output_path)
        # df_IC.to_excel(f"{fixed_filename}_{current_time}.xlsx")
#---------------------------------------------------------------------------------------------------------------------
        
        # Calculate external trips
        N1 = len(df_retail.index) # assume: only have one single retail land use within the project
        N2 = len(df_residential.index)
        ext_PM_retail_enter = []
        ext_PM_retail_exit = []
        ext_AM_retail_enter = []
        ext_AM_retail_exit = []
        ext_wkd_retail_enter = []
        ext_wkd_retail_exit = []
        
        # Calculating Retail External
        # PM
        ext_PM_retail_in = df_retail['PM Enter'] - np.sum(IC_PM_residential_retail, axis=0) # the summation is done column-wise; the sum of all the values in the same column;
        ext_PM_retail_out = df_retail['PM Exit'] - np.sum(IC_PM_retail_residential, axis=0)
        ext_PM_retail_enter.append(ext_PM_retail_in)
        ext_PM_retail_exit.append(ext_PM_retail_out)
        # AM
        ext_AM_retail_in = df_retail['AM Enter'] - np.sum(IC_AM_residential_retail, axis=0)
        ext_AM_retail_out = df_retail['AM Exit'] - np.sum(IC_AM_retail_residential, axis=0)
        ext_AM_retail_enter.append(ext_AM_retail_in)
        ext_AM_retail_exit.append(ext_AM_retail_out)
        # Wkd
        ext_wkd_retail_in = df_retail['Wkd Enter'] - np.sum(IC_wkd_residential_retail, axis=0)
        ext_wkd_retail_out = df_retail['Wkd Exit'] - np.sum(IC_wkd_retail_residential, axis=0)
        ext_wkd_retail_enter.append(ext_wkd_retail_in)
        ext_wkd_retail_exit.append(ext_wkd_retail_out)
        
        ext_PM_retail_tot = sum(ext_PM_retail_enter) + sum(ext_PM_retail_exit)
        ext_AM_retail_tot = sum(ext_AM_retail_enter) + sum(ext_AM_retail_exit)
        ext_wkd_retail_tot = sum(ext_wkd_retail_enter) + sum(ext_wkd_retail_exit)
  
        # Print individual values in 'External Retail Enter'
        for ext_PM_retail_enter_i in ext_PM_retail_enter:
            ext_PM_retail_enter_i
        for ext_AM_retail_enter_i in ext_AM_retail_enter:
            ext_AM_retail_enter_i
        for ext_wkd_retail_enter_i in ext_wkd_retail_enter:
            ext_wkd_retail_enter_i
            
        # Print individual values in 'External Retail Exit'
        for ext_PM_retail_exit_i in ext_PM_retail_exit:
            ext_PM_retail_exit_i
        for ext_AM_retail_exit_i in ext_AM_retail_exit:
            ext_AM_retail_exit_i
        for ext_wkd_retail_exit_i in ext_wkd_retail_exit:
            ext_wkd_retail_exit_i
            
        # Calculating Residential External
        # PM
        ext_PM_residential_in = df_residential['PM Enter'].values.reshape(-1, 1) - IC_PM_retail_residential # reshape the array from (2, ) to (2, 1)
        # IC_PM_retail_residential.flatten(): convert 2-dimensional array into 1-dimensional array, i.e., from (2, 1) to (2, ). 2D array is the presence of rows and columns. 1D array is a single-column array or a single-row array.
        ext_PM_residential_out = df_residential['PM Exit'].values.reshape(-1, 1) - IC_PM_residential_retail
        
        # AM
        ext_AM_residential_in = df_residential['AM Enter'].values.reshape(-1, 1) - IC_AM_retail_residential
        ext_AM_residential_out = df_residential['AM Exit'].values.reshape(-1, 1) - IC_AM_residential_retail
        
        # Wkd
        ext_wkd_residential_in = df_residential['Wkd Enter'].values.reshape(-1, 1) - IC_wkd_retail_residential
        ext_wkd_residential_out = df_residential['Wkd Exit'].values.reshape(-1, 1) - IC_wkd_residential_retail
        
        ext_PM_residential_tot = ext_PM_residential_in + ext_PM_residential_out
        ext_AM_residential_tot = ext_AM_residential_in + ext_AM_residential_out
        ext_wkd_residential_tot = ext_wkd_residential_in + ext_wkd_residential_out
        

        # Create a list to store new row data
        new_rows = []

        # Insert a row at an arbitrary position in a DataFrame based on the condition of the column range falling within one data range
        # Create the new row data
        # Get unique LUC values from df_retail
        unique_ret_luc_values = df_retail['LUC'].unique()
        for i, luc_value in enumerate(unique_ret_luc_values):
            dir_row_retail = {'ITE Land Use': "", 
                            'LUC': luc_value,
                            'Size': "",
                            'Unit': "",
                            'Weekday': "", 'AM Peak Hour': "", 'PM Peak Hour': "", 
                            'Trips': 'Directional Distribution',
                            'Wkd Enter': dir_dist_perc['retail'][str(unique_ret_luc_values[i])]['Wkd Enter'],
                            'Wkd Exit': dir_dist_perc['retail'][str(unique_ret_luc_values[i])]['Wkd Exit'],
                            'Wkd Total': dir_dist_perc['retail'][str(unique_ret_luc_values[i])]['Wkd Total'], 
                            'AM Enter': dir_dist_perc['retail'][str(unique_ret_luc_values[i])]['AM Enter'], 
                            'AM Exit': dir_dist_perc['retail'][str(unique_ret_luc_values[i])]['AM Exit'],
                            'AM Total': dir_dist_perc['retail'][str(unique_ret_luc_values[i])]['AM Total'],  
                            'PM Enter': dir_dist_perc['retail'][str(unique_ret_luc_values[i])]['PM Enter'], 
                            'PM Exit': dir_dist_perc['retail'][str(unique_ret_luc_values[i])]['PM Exit'],
                            'PM Total': dir_dist_perc['retail'][str(unique_ret_luc_values[i])]['PM Total']}
            new_rows.append(dir_row_retail)
            
            internal_row_retail = {'ITE Land Use': "", 
                            'LUC': luc_value,
                            'Size': "",
                            'Unit': "",
                            'Weekday': "", 'AM Peak Hour': "", 'PM Peak Hour': "", 
                            'Trips': 'Internal',
                            'Wkd Enter': sum(np.sum(IC_wkd_residential_retail, axis = 0)),
                            'Wkd Exit': sum(np.sum(IC_wkd_retail_residential, axis = 0)),
                            'Wkd Total': sum(np.sum(IC_wkd_tot_resi_ret, axis = 0)), 
                            'AM Enter': sum(np.sum(IC_AM_residential_retail, axis = 0)), 
                            'AM Exit': sum(np.sum(IC_AM_retail_residential, axis = 0)), 
                            'AM Total': sum(np.sum(IC_AM_tot_resi_ret, axis = 0)),   
                            'PM Enter': sum(np.sum(IC_PM_residential_retail, axis = 0)), 
                            'PM Exit': sum(np.sum(IC_PM_retail_residential, axis = 0)), 
                            'PM Total': sum(np.sum(IC_PM_tot_resi_ret, axis = 0))}
            new_rows.append(internal_row_retail)
            
            # Create the new row data
            external_row_retail = {'ITE Land Use': "", 
                            'LUC': luc_value,   
                            'Size': "",
                            'Unit': "",
                            'Weekday': "", 'AM Peak Hour': "", 'PM Peak Hour': "", 
                            'Trips': 'External',
                            'Wkd Enter': sum(ext_wkd_retail_enter_i), 
                            'Wkd Exit': sum(ext_wkd_retail_exit_i), 
                            'Wkd Total': sum(ext_wkd_retail_tot),
                            'AM Enter': sum(ext_AM_retail_enter_i), 
                            'AM Exit': sum(ext_AM_retail_exit_i),  
                            'AM Total': sum(ext_AM_retail_tot),   
                            'PM Enter': sum(ext_PM_retail_enter_i), 
                            'PM Exit': sum(ext_PM_retail_exit_i), 
                            'PM Total': sum(ext_PM_retail_tot)}
            new_rows.append(external_row_retail)

        # Find the index where the new row should be inserted
        # insert_index = df_clear.index[(df_clear['LUC'].astype(int) <= 800) & (df_clear['LUC'].astype(int) >= 200)].tolist()[1]

        # Insert the new row at the specified index
        # df_IC = df_clear.append(new_row_data, ignore_index=True)

        # Create the new row data
        # Get unique LUC values from df_residential
        unique_resi_luc_values = df_residential['LUC'].unique()
        for i, luc_value in enumerate(unique_resi_luc_values):
            dir_row_residential = {'ITE Land Use': "", 
                            'LUC': luc_value,
                            'Size': "",
                            'Unit': "",
                            'Weekday': "", 'AM Peak Hour': "", 'PM Peak Hour': "", 
                            'Trips': 'Directional Distribution',
                            'Wkd Enter': dir_dist_perc['residential'][str(unique_resi_luc_values[i])]['Wkd Enter'],
                            'Wkd Exit': dir_dist_perc['residential'][str(unique_resi_luc_values[i])]['Wkd Exit'],
                            'Wkd Total': dir_dist_perc['residential'][str(unique_resi_luc_values[i])]['Wkd Total'], 
                            'AM Enter': dir_dist_perc['residential'][str(unique_resi_luc_values[i])]['AM Enter'], 
                            'AM Exit': dir_dist_perc['residential'][str(unique_resi_luc_values[i])]['AM Exit'],
                            'AM Total': dir_dist_perc['residential'][str(unique_resi_luc_values[i])]['AM Total'],  
                            'PM Enter': dir_dist_perc['residential'][str(unique_resi_luc_values[i])]['PM Enter'], 
                            'PM Exit': dir_dist_perc['residential'][str(unique_resi_luc_values[i])]['PM Exit'],
                            'PM Total': dir_dist_perc['residential'][str(unique_resi_luc_values[i])]['PM Total']}
            new_rows.append(dir_row_residential)
            
            internal_row_residential = {'ITE Land Use': "", 
                            'LUC': luc_value, 
                            'Size': "",
                            'Unit': "",
                            'Weekday': "", 'AM Peak Hour': "", 'PM Peak Hour': "", 
                            'Trips': 'Internal',
                            'Wkd Enter': sum(IC_wkd_retail_residential[i]),
                            'Wkd Exit': sum(IC_wkd_residential_retail[i]), 
                            'Wkd Total': sum(IC_wkd_tot_resi_ret[i]),
                            'AM Enter': sum(IC_AM_retail_residential[i]),
                            'AM Exit': sum(IC_AM_residential_retail[i]), 
                            'AM Total': sum(IC_AM_tot_resi_ret[i]),  
                            'PM Enter': sum(IC_PM_retail_residential[i]),
                            'PM Exit': sum(IC_PM_residential_retail[i]), 
                            'PM Total': sum(IC_PM_tot_resi_ret[i])}
            new_rows.append(internal_row_residential)

            # Create the new row data
            external_row_residential = {'ITE Land Use': "", 
                            'LUC': luc_value, 
                            'Size': "",
                            'Unit': "",
                            'Weekday': "", 'AM Peak Hour': "", 'PM Peak Hour': "", 
                            'Trips': 'External',
                            'Wkd Enter': sum(ext_wkd_residential_in[i]), 
                            'Wkd Exit': sum(ext_wkd_residential_out[i]), 
                            'Wkd Total': sum(ext_wkd_residential_tot[i]),
                            'AM Enter': sum(ext_AM_residential_in[i]), 
                            'AM Exit': sum(ext_AM_residential_out[i]), 
                            'AM Total': sum(ext_AM_residential_tot[i]),  
                            'PM Enter': sum(ext_PM_residential_in[i]), 
                            'PM Exit': sum(ext_PM_residential_out[i]), 
                            'PM Total': sum(ext_PM_residential_tot[i])}
            new_rows.append(external_row_residential)
        
        # Check if there are pass-by capture
        pass_by_list = ['816', '820', '821', '822']
        item_list = LU
        def check_pass_by (list_c):
            if any(item in item_list for item in list_c):
                print('*********************************************')
                print()
                print (" There are pass-by capture.")
                
                pass_by_rate_PM = input("What is the pass-by rate for the retail in the PM Peak Hour? (Please use 2 decimals instead of %) ")
                pass_by_rate_AM = input("What is the pass-by rate for the retail in the AM Peak Hour? (Please use 2 decimals instead of %) ")
                pass_by_rate_wkd = input("What is the pass-by rate for the retail on Weekday? (Please use 2 decimals instead of %) ")
                
                # PM
                pass_by_retail_enter_PMi = int(sum(ext_PM_retail_enter_i) * float(pass_by_rate_PM))
                pass_by_retail_exit_PMi = int(sum(ext_PM_retail_exit_i) * float(pass_by_rate_PM))
                pass_by_retail_tot_PMi = pass_by_retail_enter_PMi + pass_by_retail_exit_PMi
                net_ext_retail_enter_PMi = sum(ext_PM_retail_enter_i) - pass_by_retail_enter_PMi
                net_ext_retail_exit_PMi = sum(ext_PM_retail_exit_i) - pass_by_retail_exit_PMi
                net_ext_retail_tot_PMi = net_ext_retail_enter_PMi + net_ext_retail_exit_PMi
                
                # AM
                pass_by_retail_enter_AMi = int(sum(ext_AM_retail_enter_i) * float(pass_by_rate_AM))
                pass_by_retail_exit_AMi = int(sum(ext_AM_retail_exit_i) * float(pass_by_rate_AM))
                pass_by_retail_tot_AMi = pass_by_retail_enter_AMi + pass_by_retail_exit_AMi
                net_ext_retail_enter_AMi = sum(ext_AM_retail_enter_i) - pass_by_retail_enter_AMi
                net_ext_retail_exit_AMi = sum(ext_AM_retail_exit_i) - pass_by_retail_exit_AMi
                net_ext_retail_tot_AMi = net_ext_retail_enter_AMi + net_ext_retail_exit_AMi
                
                # wkd
                pass_by_retail_enter_wkdi = int(sum(ext_wkd_retail_enter_i) * float(pass_by_rate_wkd))
                pass_by_retail_exit_wkdi = int(sum(ext_wkd_retail_exit_i) * float(pass_by_rate_wkd))
                pass_by_retail_tot_wkdi = pass_by_retail_enter_wkdi + pass_by_retail_exit_wkdi
                net_ext_retail_enter_wkdi = sum(ext_wkd_retail_enter_i) - pass_by_retail_enter_wkdi
                net_ext_retail_exit_wkdi = sum(ext_wkd_retail_exit_i) - pass_by_retail_exit_wkdi
                net_ext_retail_tot_wkdi = net_ext_retail_enter_wkdi + net_ext_retail_exit_wkdi
                
                # Create the new row data
                pass_by_row_retail = {'ITE Land Use': "", 
                                'LUC': sum(df_retail['LUC']), # assume: only have one single retail land use within the project
                                'Size': "",
                                'Unit': "",
                                'Weekday': "", 'AM Peak Hour': "", 'PM Peak Hour': "", 
                                'Trips': 'Pass-by',
                                'Wkd Enter': pass_by_retail_enter_wkdi,
                                'Wkd Exit': pass_by_retail_exit_wkdi,
                                'Wkd Total': pass_by_retail_tot_wkdi,
                                'AM Enter': pass_by_retail_enter_AMi,
                                'AM Exit': pass_by_retail_exit_AMi,
                                'AM Total': pass_by_retail_tot_AMi,  
                                'PM Enter': pass_by_retail_enter_PMi,
                                'PM Exit': pass_by_retail_exit_PMi,
                                'PM Total': pass_by_retail_tot_PMi}
                new_rows.append(pass_by_row_retail)
                
                # Create the new row data
                net_external_row_retail = {'ITE Land Use': "", 
                                'LUC': sum(df_retail['LUC']), # assume: only have one single retail land use within the project
                                'Size': "",
                                'Unit': "",
                                'Weekday': "", 'AM Peak Hour': "", 'PM Peak Hour': "", 
                                'Trips': 'Net External',
                                'Wkd Enter': net_ext_retail_enter_wkdi,
                                'Wkd Exit': net_ext_retail_exit_wkdi,
                                'Wkd Total': net_ext_retail_tot_wkdi,
                                'AM Enter': net_ext_retail_enter_AMi,
                                'AM Exit': net_ext_retail_exit_AMi,
                                'AM Total': net_ext_retail_tot_AMi,  
                                'PM Enter': net_ext_retail_enter_PMi,
                                'PM Exit': net_ext_retail_exit_PMi,
                                'PM Total': net_ext_retail_tot_PMi}
                new_rows.append(net_external_row_retail)
                           
            print('*********************************************')
            print()
            
        check_pass_by (pass_by_list)
        
        # Find the index where the new row should be inserted
        # insert_index = df_clear.index[df_clear['LUC'].astype(int) >= 200].tolist()[-1] + 1 #insert row to the end

        # Insert the new row at the specified index
        df_IC = df_clear.append(new_rows, ignore_index=True)

        # Sort the DataFrame based on the 'LUC' column to maintain order
        df_IC = df_IC.sort_values(by='LUC', ignore_index=True)
        # print(df_IC)
        
        # Save to .csv file
        df_IC.to_csv('Trip Generation with IC.csv', index=False)

        
        # Initialize variables to store the calculated sums
        # Store into total trips
        total_values_1 = {}

        # Iterate through rows 
        for index, row in df_IC.iterrows():
            if "Total" in row['Trips']:
                for col in df_IC.columns:
                    if col in ['Wkd Enter']:
                        total_values_1[col] = total_values_1.get(col, 0) + row[col] # 'total_values.get(col, 0) ensures that if the key (column name) doesn't exist in the dictionary, it initializes it with a value of 0.
                    if col in ['Wkd Exit']:
                        total_values_1[col] = total_values_1.get(col, 0) + row[col]
                    if col in ['Wkd Total']:
                        total_values_1[col] = total_values_1.get(col, 0) + row[col]
                    if col in ['AM Enter']:
                        total_values_1[col] = total_values_1.get(col, 0) + row[col]
                    if col in ['AM Exit']:
                        total_values_1[col] = total_values_1.get(col, 0) + row[col]
                    if col in ['AM Total']:
                        total_values_1[col] = total_values_1.get(col, 0) + row[col]
                    if col in ['PM Enter']:
                        total_values_1[col] = total_values_1.get(col, 0) + row[col]
                    if col in ['PM Exit']:
                        total_values_1[col] = total_values_1.get(col, 0) + row[col]
                    if col in ['PM Total']:
                        total_values_1[col] = total_values_1.get(col, 0) + row[col]

        # Create a new row with "Total" values
        total_row1 = {'ITE Land Use': 'Total Land Use Property', 'Trips': 'Total Traffic', **total_values_1}

        # Append the new row to the DataFrame
        df_IC = df_IC.append(total_row1, ignore_index=True)
        
        # Initialize variables to store the calculated sums
        # Store into total internal trips
        total_values_2 = {}

        # Iterate through rows
        for index, row in df_IC.iterrows():
            if "Internal" in row['Trips']:
                for col in df_IC.columns:
                    if col in ['Wkd Enter']:
                        total_values_2[col] = total_values_2.get(col, 0) + row[col]
                    if col in ['Wkd Exit']:
                        total_values_2[col] = total_values_2.get(col, 0) + row[col]
                    if col in ['Wkd Total']:
                        total_values_2[col] = total_values_2.get(col, 0) + row[col]
                    if col in ['AM Enter']:
                        total_values_2[col] = total_values_2.get(col, 0) + row[col]
                    if col in ['AM Exit']:
                        total_values_2[col] = total_values_2.get(col, 0) + row[col]
                    if col in ['AM Total']:
                        total_values_2[col] = total_values_2.get(col, 0) + row[col]
                    if col in ['PM Enter']:
                        total_values_2[col] = total_values_2.get(col, 0) + row[col]
                    if col in ['PM Exit']:
                        total_values_2[col] = total_values_2.get(col, 0) + row[col]
                    if col in ['PM Total']:
                        total_values_2[col] = total_values_2.get(col, 0) + row[col]

        # Create a new row with "Total" values
        total_row2 = {'ITE Land Use': 'Total Land Use Property', 'Trips': 'Total Internal Capture', **total_values_2}

        # Append the new row to the DataFrame
        df_IC = df_IC.append(total_row2, ignore_index=True)
        
        # Initialize variables to store the calculated sums
        # Store into total external trips
        total_values_3 = {}

        # Iterate through rows
        for index, row in df_IC.iterrows():
            if row['Trips'].strip() == 'External': # to check for the exact math of "External", not include "Net External"
                for col in df_IC.columns:
                    if col in ['Wkd Enter']:
                        total_values_3[col] = total_values_3.get(col, 0) + row[col]
                    if col in ['Wkd Exit']:
                        total_values_3[col] = total_values_3.get(col, 0) + row[col]
                    if col in ['Wkd Total']:
                        total_values_3[col] = total_values_3.get(col, 0) + row[col]
                    if col in ['AM Enter']:
                        total_values_3[col] = total_values_3.get(col, 0) + row[col]
                    if col in ['AM Exit']:
                        total_values_3[col] = total_values_3.get(col, 0) + row[col]
                    if col in ['AM Total']:
                        total_values_3[col] = total_values_3.get(col, 0) + row[col]
                    if col in ['PM Enter']:
                        total_values_3[col] = total_values_3.get(col, 0) + row[col]
                    if col in ['PM Exit']:
                        total_values_3[col] = total_values_3.get(col, 0) + row[col]
                    if col in ['PM Total']:
                        total_values_3[col] = total_values_3.get(col, 0) + row[col]

        # Create a new row with "Total" values
        total_row3 = {'ITE Land Use': 'Total Land Use Property', 'Trips': 'Total External', **total_values_3}

        # Append the new row to the DataFrame
        df_IC = df_IC.append(total_row3, ignore_index=True)
        
        # Initialize variables to store the calculated sums
        # Store into total pass-by trips
        total_values_4 = {}

        # Iterate through rows
        for index, row in df_IC.iterrows():
            if "Pass-by" in row['Trips']:
                for col in df_IC.columns:
                    if col in ['Wkd Enter']:
                        total_values_4[col] = total_values_4.get(col, 0) + row[col]
                    if col in ['Wkd Exit']:
                        total_values_4[col] = total_values_4.get(col, 0) + row[col]
                    if col in ['Wkd Total']:
                        total_values_4[col] = total_values_4.get(col, 0) + row[col]
                    if col in ['AM Enter']:
                        total_values_4[col] = total_values_4.get(col, 0) + row[col]
                    if col in ['AM Exit']:
                        total_values_4[col] = total_values_4.get(col, 0) + row[col]
                    if col in ['AM Total']:
                        total_values_4[col] = total_values_4.get(col, 0) + row[col]
                    if col in ['PM Enter']:
                        total_values_4[col] = total_values_4.get(col, 0) + row[col]
                    if col in ['PM Exit']:
                        total_values_4[col] = total_values_4.get(col, 0) + row[col]
                    if col in ['PM Total']:
                        total_values_4[col] = total_values_4.get(col, 0) + row[col]

        # Create a new row with "Total" values
        total_row4 = {'ITE Land Use': 'Total Land Use Property', 'Trips': 'Total Pass-by Capture', **total_values_4}

        # Append the new row to the DataFrame
        df_IC = df_IC.append(total_row4, ignore_index=True)
        
        # Initialize variables to store the calculated net values
        # Store into total net external trips
        total_values_5 = {}

        # Iterate through rows
        for index, row in df_IC.iterrows():
            if row['Trips'].strip() in ['Total Traffic', 'Total Internal Capture', 'Total Pass-by Capture']: 
                for col in df_IC.columns:
                    if col in ['Wkd Enter', 'Wkd Exit', 'Wkd Total', 'AM Enter', 'AM Exit', 'AM Total', 'PM Enter', 'PM Exit', 'PM Total']:
                        if row['Trips'].strip() == 'Total Traffic':
                            total_values_5[col] = total_values_5.get(col, 0) + row[col]
                        elif row['Trips'].strip() == 'Total Internal Capture':
                            total_values_5[col] -= row[col]
                        elif row['Trips'].strip() == 'Total Pass-by Capture':
                            total_values_5[col] -= row[col]
                        
        # Create a new row with "Total" values
        total_row5 = {'ITE Land Use': 'Total Land Use Property','Trips': 'Total Net External', **total_values_5}

        # Append the new row to the DataFrame
        df_IC = df_IC.append(total_row5, ignore_index=True)

        
        # Initialize variables to store the calculated total internal capture percentage
        total_values_6 = {}

        # Iterate through rows
        for index, row in df_IC.iterrows():
            if row['Trips'].strip() in ['Total Traffic', 'Total Internal Capture']: 
                for col in df_IC.columns:
                    if col in ['Wkd Total', 'AM Total', 'PM Total']:
                        if row['Trips'].strip() == 'Total Traffic':
                            total_values_6[col] = total_values_6.get(col, 0) + row[col]
                        elif row['Trips'].strip() == 'Total Internal Capture':
                            total_values_6[col] = row[col] / total_values_6[col]
        
        # Format the calculated percentages with two decimal places
        for col in total_values_6:
            total_values_6[col] = "{:.2%}".format(total_values_6[col])
                        
        # Create a new row with "Total" values
        total_row6 = {'ITE Land Use': 'Total Land Use Property','Trips': 'Internal Capture Percent', **total_values_6}

        # Append the new row to the DataFrame
        df_IC = df_IC.append(total_row6, ignore_index=True)

        
        # Initialize variables to store the calculated total pass-by capture percentage
        total_values_7 = {}

        # Iterate through rows
        for index, row in df_IC.iterrows():
            if row['Trips'].strip() in ['Total External', 'Total Pass-by Capture']: 
                for col in df_IC.columns:
                    if col in ['Wkd Total', 'AM Total', 'PM Total']:
                        if row['Trips'].strip() == 'Total External':
                            total_values_7[col] = total_values_7.get(col, 0) + row[col]
                        elif row['Trips'].strip() == 'Total Pass-by Capture':
                            total_values_7[col] = row[col] / total_values_7[col]
        
        # Format the calculated percentages with two decimal places
        for col in total_values_7:
            total_values_7[col] = "{:.2%}".format(total_values_7[col])
                        
        # Create a new row with "Total" values
        total_row7 = {'ITE Land Use': 'Total Land Use Property','Trips': 'Pass-by Capture Percent', **total_values_7}

        # Append the new row to the DataFrame
        df_IC = df_IC.append(total_row7, ignore_index=True)
        
        # Adding multi-level column names for the output
        df_IC.columns = pd.MultiIndex.from_tuples(
            [('Development', 'ITE Land Use'), ('Development', 'LUC'),
             ('Measurement', 'Size'), ('Measurement', 'Unit'), 
             ('Measurement', 'Weekday'), ('Measurement', 'AM Peak Hour'), ('Measurement', 'PM Peak Hour'), ('Measurement', 'Trips'),
             ('Daily Traffic', 'Wkd Enter'), ('Daily Traffic', 'Wkd Exit'), ('Daily Traffic', 'Wkd Total'),
             ('AM Peak Hour Traffic', 'AM Enter'), ('AM Peak Hour Traffic', 'AM Exit'), ('AM Peak Hour Traffic', 'AM Total'),
             ('PM Peak Hour Traffic', 'PM Enter'), ('PM Peak Hour Traffic', 'PM Exit'), ('PM Peak Hour Traffic', 'PM Total'), ]
            )
        
        # Adding notes
        # it is selective to add footnotes at the bottom of dataframe

        # Save to .csv file
        df_IC.to_csv('Trip Generation with IC.csv', index = False) # csv doesn't have to have index
        
        # Save to .xlsx file
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        fixed_filename = "Trip Generation with IC"
        output_path = fr'C:\Users\Wang Xi\Desktop\Wang Xi\Python projects\Output\{fixed_filename}_{current_time}.xlsx' # xlsx has to have index because it is a multi-level index
        df_IC.to_excel(output_path)
        # df_IC.to_excel(f"{fixed_filename}_{current_time}.xlsx") 
        
        print()
        print('Trip generation with internal capture and external trips spreadsheet is successfully saved')
        print('*********************************************')
        print()
        
    else:
        print(" There is no internal capture because it is a single land use")
        
        # Check if there are pass-by capture
        pass_by_retail_list = ['816', '820', '821', '822']
        pass_by_restaurant_list = ['932', '934']
        item_list = LU
        
        def check_pass_by_ret (list_c):
            if any(item in item_list for item in list_c):
                print('*********************************************')
                print()
                print (" There are pass-by capture.")
                
                pass_by_rate_PM = input("What is the pass-by rate for the retail in the PM Peak Hour? (Please use 2 decimals instead of %) ")
                pass_by_rate_AM = input("What is the pass-by rate for the retail in the AM Peak Hour? (Please use 2 decimals instead of %) ")
                pass_by_rate_wkd = input("What is the pass-by rate for the retail on Weekday? (Please use 2 decimals instead of %) ")
                
                # Create a list to store new row data
                new_rows = []
                
                # Calculating Retail PB
                unique_ret_luc_values = df_retail['LUC'].unique()
                for i, luc_value in enumerate(unique_ret_luc_values):
                    # PM
                    pass_by_retail_enter_PM = (df_retail['PM Enter'] * pass_by_rate_PM).astype(int)
                    pass_by_retail_exit_PM = (df_retail['PM Exit'] * pass_by_rate_PM).astype(int)
                    pass_by_retail_tot_PM = pass_by_retail_enter_PM + pass_by_retail_exit_PM
                    net_ext_retail_enter_PM = df_retail['PM Enter'] - pass_by_retail_enter_PM
                    net_ext_retail_exit_PM = df_retail['PM Exit'] - pass_by_retail_exit_PM
                    net_ext_retail_tot_PM = net_ext_retail_enter_PM + net_ext_retail_exit_PM
                    
                    # AM
                    pass_by_retail_enter_AM = (df_retail['AM Enter'] * pass_by_rate_AM).astype(int)
                    pass_by_retail_exit_AM = (df_retail['AM Exit'] * pass_by_rate_AM).astype(int)
                    pass_by_retail_tot_AM = pass_by_retail_enter_AM + pass_by_retail_exit_AM
                    net_ext_retail_enter_AM = df_retail['AM Enter'] - pass_by_retail_enter_AM
                    net_ext_retail_exit_AM = df_retail['AM Exit'] - pass_by_retail_exit_AM
                    net_ext_retail_tot_AM = net_ext_retail_enter_AM + net_ext_retail_exit_AM
                    
                    # wkd
                    pass_by_retail_enter_wkd = (df_retail['Wkd Enter'] * pass_by_rate_wkd).astype(int)
                    pass_by_retail_exit_wkd = (df_retail['Wkd Exit'] * pass_by_rate_wkd).astype(int)
                    pass_by_retail_tot_wkd = pass_by_retail_enter_wkd + pass_by_retail_exit_wkd
                    net_ext_retail_enter_wkd = df_retail['Wkd Enter'] - pass_by_retail_enter_wkd
                    net_ext_retail_exit_wkd = df_retail['Wkd Exit'] - pass_by_retail_exit_wkd
                    net_ext_retail_tot_wkd = net_ext_retail_enter_wkd + net_ext_retail_exit_wkd
                    
                    # Create the new row data
                    pass_by_row_retail = {'ITE Land Use': "", 
                                    'LUC': luc_value,
                                    'Size': "",
                                    'Unit': "",
                                    'Weekday': "", 'AM Peak Hour': "", 'PM Peak Hour': "", 
                                    'Trips': 'Pass-by',
                                    'Wkd Enter': pass_by_retail_enter_wkd[i],
                                    'Wkd Exit': pass_by_retail_exit_wkd[i],
                                    'Wkd Total': pass_by_retail_tot_wkd[i],
                                    'AM Enter': pass_by_retail_enter_AM[i],
                                    'AM Exit': pass_by_retail_exit_AM[i],
                                    'AM Total': pass_by_retail_tot_AM[i],  
                                    'PM Enter': pass_by_retail_enter_PM[i],
                                    'PM Exit': pass_by_retail_exit_PM[i],
                                    'PM Total': pass_by_retail_tot_PM[i]}
                    new_rows.append(pass_by_row_retail)
                    
                    # Create the new row data
                    net_external_row_retail = {'ITE Land Use': "", 
                                    'LUC': luc_value,
                                    'Size': "",
                                    'Unit': "",
                                    'Weekday': "", 'AM Peak Hour': "", 'PM Peak Hour': "", 
                                    'Trips': 'Net External',
                                    'Wkd Enter': net_ext_retail_enter_wkd[i],
                                    'Wkd Exit': net_ext_retail_exit_wkd[i],
                                    'Wkd Total': net_ext_retail_tot_wkd[i],
                                    'AM Enter': net_ext_retail_enter_AM[i],
                                    'AM Exit': net_ext_retail_exit_AM[i],
                                    'AM Total': net_ext_retail_tot_AM[i],  
                                    'PM Enter': net_ext_retail_enter_PM[i],
                                    'PM Exit': net_ext_retail_exit_PM[i],
                                    'PM Total': net_ext_retail_tot_PM[i]}
                    new_rows.append(net_external_row_retail)
                    
                
                # Append the new row to the DataFrame
                df_PB = df_clear.append(new_rows, ignore_index=True)
                
                # Sort the DataFrame based on the 'LUC' column to maintain order
                df_PB = df_PB.sort_values(by='LUC', ignore_index=True)
                
                # Store into total trips
                total_values_1 = {}

                # Iterate through rows
                for index, row in df_PB.iterrows():
                    if "Total" in row['Trips']:
                        for col in df_PB.columns:
                            if col in ['Wkd Enter']:
                                total_values_1[col] = total_values_1.get(col, 0) + row[col]
                            if col in ['Wkd Exit']:
                                total_values_1[col] = total_values_1.get(col, 0) + row[col]
                            if col in ['Wkd Total']:
                                total_values_1[col] = total_values_1.get(col, 0) + row[col]
                            if col in ['AM Enter']:
                                total_values_1[col] = total_values_1.get(col, 0) + row[col]
                            if col in ['AM Exit']:
                                total_values_1[col] = total_values_1.get(col, 0) + row[col]
                            if col in ['AM Total']:
                                total_values_1[col] = total_values_1.get(col, 0) + row[col]
                            if col in ['PM Enter']:
                                total_values_1[col] = total_values_1.get(col, 0) + row[col]
                            if col in ['PM Exit']:
                                total_values_1[col] = total_values_1.get(col, 0) + row[col]
                            if col in ['PM Total']:
                                total_values_1[col] = total_values_1.get(col, 0) + row[col]

                # Create a new row with "Total" values
                total_row1 = {'ITE Land Use': 'Total Land Use Property', 'Trips': 'Total Traffic', **total_values_1}

                # Append the new row to the DataFrame
                df_PB = df_PB.append(total_row1, ignore_index=True)
                
                # Initialize variables to store the calculated sums
                # Store into total pass-by trips
                total_values_2 = {}

                # Iterate through rows
                for index, row in df_PB.iterrows():
                    if "Pass-by" in row['Trips']:
                        for col in df_PB.columns:
                            if col in ['Wkd Enter']:
                                total_values_2[col] = total_values_2.get(col, 0) + row[col]
                            if col in ['Wkd Exit']:
                                total_values_2[col] = total_values_2.get(col, 0) + row[col]
                            if col in ['Wkd Total']:
                                total_values_2[col] = total_values_2.get(col, 0) + row[col]
                            if col in ['AM Enter']:
                                total_values_2[col] = total_values_2.get(col, 0) + row[col]
                            if col in ['AM Exit']:
                                total_values_2[col] = total_values_2.get(col, 0) + row[col]
                            if col in ['AM Total']:
                                total_values_2[col] = total_values_2.get(col, 0) + row[col]
                            if col in ['PM Enter']:
                                total_values_2[col] = total_values_2.get(col, 0) + row[col]
                            if col in ['PM Exit']:
                                total_values_2[col] = total_values_2.get(col, 0) + row[col]
                            if col in ['PM Total']:
                                total_values_2[col] = total_values_2.get(col, 0) + row[col]

                # Create a new row with "Total" values
                total_row2 = {'ITE Land Use': 'Total Land Use Property', 'Trips': 'Total Pass-by Capture', **total_values_2}

                # Append the new row to the DataFrame
                df_PB = df_PB.append(total_row2, ignore_index=True)
                
                # Initialize variables to store the calculated net values
                # Store into total nom-pass by trips
                total_values_3 = {}

                # Iterate through rows
                for index, row in df_PB.iterrows():
                    if row['Trips'].strip() in ['Total Traffic', 'Total Pass-by Capture']: 
                        for col in df_PB.columns:
                            if col in ['Wkd Enter', 'Wkd Exit', 'Wkd Total', 'AM Enter', 'AM Exit', 'AM Total', 'PM Enter', 'PM Exit', 'PM Total']:
                                if row['Trips'].strip() == 'Total Traffic':
                                    total_values_3[col] = total_values_3.get(col, 0) + row[col]
                                elif row['Trips'].strip() == 'Total Pass-by Capture':
                                    total_values_3[col] -= row[col]
                                
                # Create a new row with "Total" values
                total_row3 = {'ITE Land Use': 'Total Land Use Property','Trips': 'Total Non-pass-by', **total_values_3}

                # Append the new row to the DataFrame
                df_PB = df_PB.append(total_row3, ignore_index=True)
         
                
                # Initialize variables to store the calculated total pass-by capture percentage
                total_values_4 = {}

                # Iterate through rows
                for index, row in df_PB.iterrows():
                    if row['Trips'].strip() in ['Total Traffic', 'Total Pass-by Capture']: 
                        for col in df_PB.columns:
                            if col in ['Wkd Total', 'AM Total', 'PM Total']:
                                if row['Trips'].strip() == 'Total Traffic':
                                    total_values_4[col] = total_values_4.get(col, 0) + row[col]
                                elif row['Trips'].strip() == 'Total Pass-by Capture':
                                    total_values_4[col] = row[col] / total_values_4[col]
                
                # Format the calculated percentages with two decimal places
                for col in total_values_4:
                    total_values_4[col] = "{:.2%}".format(total_values_4[col])
                                
                # Create a new row with "Total" values
                total_row4 = {'ITE Land Use': 'Total Land Use Property','Trips': 'Pass-by Capture Percent', **total_values_4}
                
                # Append the new row to the DataFrame
                df_PB = df_PB.append(total_row4, ignore_index=True)
                
                # Adding multi-level column names for the output
                df_PB.columns = pd.MultiIndex.from_tuples(
                    [('Development', 'ITE Land Use'), ('Development', 'LUC'),
                     ('Measurement', 'Size'), ('Measurement', 'Unit'), 
                     ('Measurement', 'Weekday'), ('Measurement', 'AM Peak Hour'), ('Measurement', 'PM Peak Hour'), ('Measurement', 'Trips'),
                     ('Daily Traffic', 'Wkd Enter'), ('Daily Traffic', 'Wkd Exit'), ('Daily Traffic', 'Wkd Total'),
                     ('AM Peak Hour Traffic', 'AM Enter'), ('AM Peak Hour Traffic', 'AM Exit'), ('AM Peak Hour Traffic', 'AM Total'),
                     ('PM Peak Hour Traffic', 'PM Enter'), ('PM Peak Hour Traffic', 'PM Exit'), ('PM Peak Hour Traffic', 'PM Total'), ]
                    )
                
                # Save to .csv file
                df_PB.to_csv('Trip Generation wto IC.csv', index = False)
                
                # Save to .xlsx file
                current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                fixed_filename = "Trip Generation wto IC"
                output_path = fr'C:\Users\Wang Xi\Desktop\Methodology\Python projects\Output\{fixed_filename}_{current_time}.xlsx' # xlsx has to have index because it is a multi-level index
                df_PB.to_excel(output_path)
                # df_IC.to_excel(f"{fixed_filename}_{current_time}.xlsx")
                
                print()
                print('Trip generation csv and xlsx file is successfully saved')
                print('*********************************************')
                print()
                
            
                
                
            else:
                print('*********************************************')
                print()
                print (" There are no pass-by capture.")
                
                # Create a list to store new row data
                new_rows = []
                df_other = df_clear.loc[df_clear.apply(lambda x: 400 <= int(x.LUC) <= 699, axis = 1)]
                
                # Get unique LUC values from df_residential
                unique_res_luc_values = df_residential['LUC'].unique()
                for i, luc_value in enumerate(unique_res_luc_values):
                    dir_row_residential = {'ITE Land Use': "", 
                                    'LUC': luc_value,
                                    'Size': "",
                                    'Unit': "",
                                    'Weekday': "", 'AM Peak Hour': "", 'PM Peak Hour': "", 
                                    'Trips': 'Directional Distribution',
                                    'Wkd Enter': dir_dist_perc['residential'][str(unique_res_luc_values[i])]['Wkd Enter'],
                                    'Wkd Exit': dir_dist_perc['residential'][str(unique_res_luc_values[i])]['Wkd Exit'],
                                    'Wkd Total': dir_dist_perc['residential'][str(unique_res_luc_values[i])]['Wkd Total'], 
                                    'AM Enter': dir_dist_perc['residential'][str(unique_res_luc_values[i])]['AM Enter'], 
                                    'AM Exit': dir_dist_perc['residential'][str(unique_res_luc_values[i])]['AM Exit'],
                                    'AM Total': dir_dist_perc['residential'][str(unique_res_luc_values[i])]['AM Total'],  
                                    'PM Enter': dir_dist_perc['residential'][str(unique_res_luc_values[i])]['PM Enter'], 
                                    'PM Exit': dir_dist_perc['residential'][str(unique_res_luc_values[i])]['PM Exit'],
                                    'PM Total': dir_dist_perc['residential'][str(unique_res_luc_values[i])]['PM Total']}
                    new_rows.append(dir_row_residential)
                    
                # Get unique LUC values from df_hotel
                unique_hm_luc_values = df_hotel['LUC'].unique()
                for i, luc_value in enumerate(unique_hm_luc_values):
                    dir_row_hotel = {'ITE Land Use': "", 
                                    'LUC': luc_value,
                                    'Size': "",
                                    'Unit': "",
                                    'Weekday': "", 'AM Peak Hour': "", 'PM Peak Hour': "", 
                                    'Trips': 'Directional Distribution',
                                    'Wkd Enter': dir_dist_perc['hotel'][str(unique_hm_luc_values[i])]['Wkd Enter'],
                                    'Wkd Exit': dir_dist_perc['hotel'][str(unique_hm_luc_values[i])]['Wkd Exit'],
                                    'Wkd Total': dir_dist_perc['hotel'][str(unique_hm_luc_values[i])]['Wkd Total'], 
                                    'AM Enter': dir_dist_perc['hotel'][str(unique_hm_luc_values[i])]['AM Enter'], 
                                    'AM Exit': dir_dist_perc['hotel'][str(unique_hm_luc_values[i])]['AM Exit'],
                                    'AM Total': dir_dist_perc['hotel'][str(unique_hm_luc_values[i])]['AM Total'],  
                                    'PM Enter': dir_dist_perc['hotel'][str(unique_hm_luc_values[i])]['PM Enter'], 
                                    'PM Exit': dir_dist_perc['hotel'][str(unique_hm_luc_values[i])]['PM Exit'],
                                    'PM Total': dir_dist_perc['hotel'][str(unique_hm_luc_values[i])]['PM Total']}
                    new_rows.append(dir_row_hotel)
                
                # Get unique LUC values from df_retail
                unique_ret_luc_values = df_retail['LUC'].unique()
                for i, luc_value in enumerate(unique_ret_luc_values):
                    dir_row_retail = {'ITE Land Use': "", 
                                    'LUC': luc_value,
                                    'Size': "",
                                    'Unit': "",
                                    'Weekday': "", 'AM Peak Hour': "", 'PM Peak Hour': "", 
                                    'Trips': 'Directional Distribution',
                                    'Wkd Enter': dir_dist_perc['retail'][str(unique_ret_luc_values[i])]['Wkd Enter'],
                                    'Wkd Exit': dir_dist_perc['retail'][str(unique_ret_luc_values[i])]['Wkd Exit'],
                                    'Wkd Total': dir_dist_perc['retail'][str(unique_ret_luc_values[i])]['Wkd Total'], 
                                    'AM Enter': dir_dist_perc['retail'][str(unique_ret_luc_values[i])]['AM Enter'], 
                                    'AM Exit': dir_dist_perc['retail'][str(unique_ret_luc_values[i])]['AM Exit'],
                                    'AM Total': dir_dist_perc['retail'][str(unique_ret_luc_values[i])]['AM Total'],  
                                    'PM Enter': dir_dist_perc['retail'][str(unique_ret_luc_values[i])]['PM Enter'], 
                                    'PM Exit': dir_dist_perc['retail'][str(unique_ret_luc_values[i])]['PM Exit'],
                                    'PM Total': dir_dist_perc['retail'][str(unique_ret_luc_values[i])]['PM Total']}
                    new_rows.append(dir_row_retail)
                    
                # Get unique LUC values from df_other
                unique_other_luc_values = df_other['LUC'].unique()
                for i, luc_value in enumerate(unique_other_luc_values):
                    dir_row_other = {'ITE Land Use': "", 
                                    'LUC': luc_value,
                                    'Size': "",
                                    'Unit': "",
                                    'Weekday': "", 'AM Peak Hour': "", 'PM Peak Hour': "", 
                                    'Trips': 'Directional Distribution',
                                    'Wkd Enter': dir_dist_perc['other'][str(unique_other_luc_values[i])]['Wkd Enter'],
                                    'Wkd Exit': dir_dist_perc['other'][str(unique_other_luc_values[i])]['Wkd Exit'],
                                    'Wkd Total': dir_dist_perc['other'][str(unique_other_luc_values[i])]['Wkd Total'], 
                                    'AM Enter': dir_dist_perc['other'][str(unique_other_luc_values[i])]['AM Enter'], 
                                    'AM Exit': dir_dist_perc['other'][str(unique_other_luc_values[i])]['AM Exit'],
                                    'AM Total': dir_dist_perc['other'][str(unique_other_luc_values[i])]['AM Total'],  
                                    'PM Enter': dir_dist_perc['other'][str(unique_other_luc_values[i])]['PM Enter'], 
                                    'PM Exit': dir_dist_perc['other'][str(unique_other_luc_values[i])]['PM Exit'],
                                    'PM Total': dir_dist_perc['other'][str(unique_other_luc_values[i])]['PM Total']}
                    new_rows.append(dir_row_other)
                               
                # Insert the new row at the specified index
                df_other = df_clear.append(new_rows, ignore_index=True)
                
                # Convert 'LUC' column to string type
                df_other['LUC'] = df_other['LUC'].astype(str)

                # Sort the DataFrame based on the 'LUC' column to maintain order
                df_other = df_other.sort_values(by='LUC', ignore_index=True)
                
                # Store into total trips
                total_values_1 = {}

                # Iterate through rows
                for index, row in df_other.iterrows():
                    if "Total" in row['Trips']:
                        for col in df_other.columns:
                            if col in ['Wkd Enter', 'Wkd Exit', 'Wkd Total', 'AM Enter', 'AM Exit', 'AM Total', 'PM Enter', 'PM Exit', 'PM Total']:
                                total_values_1[col] = total_values_1.get(col, 0) + row[col]
                

                # Create a new row with "Total" values
                total_row1 = {'ITE Land Use': 'Total Land Use Property', 'Trips': 'Total Traffic', **total_values_1}

                # Append the new row to the DataFrame
                df_other = df_other.append(total_row1, ignore_index=True)

                # Adding multi-level column names for the output
                df_other.columns = pd.MultiIndex.from_tuples(
                     [('Development', 'ITE Land Use'), ('Development', 'LUC'),
                      ('Measurement', 'Size'), ('Measurement', 'Unit'), 
                      ('Measurement', 'Weekday'), ('Measurement', 'AM Peak Hour'), ('Measurement', 'PM Peak Hour'), ('Measurement', 'Trips'),
                      ('Daily Traffic', 'Wkd Enter'), ('Daily Traffic', 'Wkd Exit'), ('Daily Traffic', 'Wkd Total'),
                      ('AM Peak Hour Traffic', 'AM Enter'), ('AM Peak Hour Traffic', 'AM Exit'), ('AM Peak Hour Traffic', 'AM Total'),
                      ('PM Peak Hour Traffic', 'PM Enter'), ('PM Peak Hour Traffic', 'PM Exit'), ('PM Peak Hour Traffic', 'PM Total'), ],
                      )
               
                # Transpose the dataframe
                # df_T = df_clear.transpose()
                
                # Rename the index after transpose
                # df_T.columns = [f'Development {i + 1}' for i in range(len(df_clear.index))]
                
                # Rename the index
                # df_clear_new.index = [f'Development {i + 1}' for i in range(len(df_clear_new.index))]
                
                # Save to .csv file
                df_other.to_csv('Trip Generation wto IC-PB.csv') # after transpose, need index in csv
                
                # Save to .xlsx file
                current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                fixed_filename = "Trip Generation wto IC-PB"
                output_path = fr'C:\Users\Wang Xi\Desktop\Wang Xi\Python projects\Output\{fixed_filename}_{current_time}.xlsx' # xlsx has to have index because it is a multi-level index
                df_other.to_excel(output_path)
                # df_IC.to_excel(f"{fixed_filename}_{current_time}.xlsx")
                
                print()
                print('Trip generation csv and xlsx file is successfully saved')
                print('*********************************************')
                print()
                
        check_pass_by_ret (pass_by_retail_list)
            
    
    
    
check_crosslists_not_empty_resi_ret(LU_in_residential, LU_in_retail)
check_crosslists_not_empty_hm_rest(LU_in_hotel, LU_in_restaurant)
print('*********************************************')
print()