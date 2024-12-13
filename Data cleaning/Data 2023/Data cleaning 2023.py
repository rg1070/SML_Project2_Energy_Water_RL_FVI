import pandas as pd
from datetime import datetime, timedelta

#2023 data cleaning:
#Import expected empty dataframes:
Data23 = pd.read_csv('Data23.csv')

## Date column:
# Define the start and end dates
start_date = datetime.strptime('06/01/2023 00:00', '%m/%d/%Y %H:%M')
end_date = datetime.strptime('08/31/2023 23:59', '%m/%d/%Y %H:%M')

# Generate date strings with minute time step
date_strings = [(start_date + timedelta(minutes=i)).strftime('%m/%d/%Y %H:%M') for i in range(int((end_date - start_date).total_seconds() / 60) + 1)]

# Date
Data23['Date']= date_strings

###############################################################################
## 1. Demand column:
Demand_raw = pd.read_csv('Raw data/2023-06-01_2023-09-01_grassLab_ab3000_islandUse_totalRealPower.csv', delimiter=',', encoding='utf-8')

# Change the format of the 'Date' column to '%m/%d/%Y %H:%M'
Demand_raw['Date'] = pd.to_datetime(Demand_raw['Date'])

Demand_raw['Date'] = Demand_raw['Date'].dt.strftime('%m/%d/%Y %H:%M')

# Write the demand
Data23['Demand (W)'] = pd.merge(Data23, Demand_raw[['Date', 'totalRealPower (W)']], on='Date', how='left')['totalRealPower (W)']

print("Is there any NA? ", Data23['Demand (W)'].isna().any())
print("How many NA? ",Data23['Demand (W)'].isna().sum())

# Fill missing values with the moving average of a window size of 10
Data23['Demand (W)'] = Data23['Demand (W)'].fillna(Data23['Demand (W)'].rolling(10, min_periods=1).mean())

print("Is there any NA now? ", Data23['Demand (W)'].isna().any())
print("How many NA? ",Data23['Demand (W)'].isna().sum())

# Fill missing values with the value from previous day
Data23['Demand (W)'] = Data23['Demand (W)'].fillna(Data23['Demand (W)'].shift(1440))

print("Is there any NA now? ", Data23['Demand (W)'].isna().any())
print("How many NA? ",Data23['Demand (W)'].isna().sum())
if Data23['Demand (W)'].isna().any()==False:
    print("Good!")
    
###############################################################################
## 2 and 3. GHI and Temp column:
GHI_Temp_raw = pd.read_csv('Raw data/2023-06-01_2023-09-01_ecb_pyranometer.csv', delimiter=',', encoding='utf-8')

# Change the format of the 'Date' column to '%m/%d/%Y %H:%M'
GHI_Temp_raw['Date'] = pd.to_datetime(GHI_Temp_raw['Date'])

GHI_Temp_raw['Date'] = GHI_Temp_raw['Date'].dt.strftime('%m/%d/%Y %H:%M')

# Write the GHI data
Data23['GHI (W/m2)'] = pd.merge(Data23, GHI_Temp_raw[['Date', 'E_Irradiance_Global_Horizontal_1 (W/m2)']], on='Date', how='left')['E_Irradiance_Global_Horizontal_1 (W/m2)']

print("Is there any NA? ", Data23['GHI (W/m2)'].isna().any())
print("How many NA? ", Data23['GHI (W/m2)'].isna().sum())

# Fill missing values with the moving average of a window size of 10
Data23['GHI (W/m2)'] = Data23['GHI (W/m2)'].fillna(Data23['GHI (W/m2)'].rolling(10, min_periods=1).mean())

print("Is there any NA now? ", Data23['GHI (W/m2)'].isna().any())
print("How many NA? ",Data23['GHI (W/m2)'].isna().sum())
if Data23['GHI (W/m2)'].isna().any()==False:
    print("Good!")

# Write the Temp data
Data23['AirTemperature (degrees C)'] = pd.merge(Data23, GHI_Temp_raw[['Date', 'E_BOM_Temp_1 (degrees C)']], on='Date', how='left')['E_BOM_Temp_1 (degrees C)']

print("Is there any NA? ", Data23['AirTemperature (degrees C)'].isna().any())
print("How many NA? ", Data23['AirTemperature (degrees C)'].isna().sum())

# Fill missing values with the moving average of a window size of 10
Data23['AirTemperature (degrees C)'] = Data23['AirTemperature (degrees C)'].fillna(Data23['AirTemperature (degrees C)'].rolling(10, min_periods=1).mean())

print("Is there any NA now? ", Data23['AirTemperature (degrees C)'].isna().any())
print("How many NA? ",Data23['AirTemperature (degrees C)'].isna().sum())
if Data23['AirTemperature (degrees C)'].isna().any()==False:
    print("Good!")

###############################################################################
## 4. Wind speed column:
Wind_raw = pd.read_csv('Raw data/2023-06-01_2023-09-01_ecb_acuDC_instantaneous.csv', delimiter=',', encoding='utf-8')

# Change the format of the 'Date' column to '%m/%d/%Y %H:%M'
Wind_raw['Date'] = pd.to_datetime(Wind_raw['Date'])

Wind_raw['Date'] = Wind_raw['Date'].dt.strftime('%m/%d/%Y %H:%M')

# Write the wind data
Data23['WindSpeedIOSN3 (m/s)'] = pd.merge(Data23, Wind_raw[['Date', 'windSpeedIOSN3 (m/s)']], on='Date', how='left')['windSpeedIOSN3 (m/s)']

print("Is there any NA? ", Data23['WindSpeedIOSN3 (m/s)'].isna().any())
print("How many NA? ", Data23['WindSpeedIOSN3 (m/s)'].isna().sum())

# Fill missing values with the moving average of a window size of 10
Data23['WindSpeedIOSN3 (m/s)'] = Data23['WindSpeedIOSN3 (m/s)'].fillna(Data23['WindSpeedIOSN3 (m/s)'].rolling(10, min_periods=1).mean())

print("Is there any NA now? ", Data23['WindSpeedIOSN3 (m/s)'].isna().any())
print("How many NA? ",Data23['WindSpeedIOSN3 (m/s)'].isna().sum())

# Fill missing values with the value from previous day
Data23['WindSpeedIOSN3 (m/s)'] = Data23['WindSpeedIOSN3 (m/s)'].fillna(Data23['WindSpeedIOSN3 (m/s)'].shift(1440))

print("Is there any NA now? ", Data23['WindSpeedIOSN3 (m/s)'].isna().any())
print("How many NA? ",Data23['WindSpeedIOSN3 (m/s)'].isna().sum())
if Data23['WindSpeedIOSN3 (m/s)'].isna().any()==False:
    print("Good!")

###############################################################################
## 5. Water demand column:
Water_raw = pd.read_csv('Raw data/2023-06-01_2023-09-01_grassLab_waterMeter_instantaneous.csv', delimiter=',', encoding='utf-8')

# Change the format of the 'Date' column to '%m/%d/%Y %H:%M'
Water_raw['Date'] = pd.to_datetime(Water_raw['Date'])

Water_raw['Date'] = Water_raw['Date'].dt.strftime('%m/%d/%Y %H:%M')

# Write the water data
Data23['Demand tPlusDifference (gal)'] = pd.merge(Data23, Water_raw[['Date', 'tPlusDifference (gal)']], on='Date', how='left')['tPlusDifference (gal)']

print("Is there any NA? ", Data23['Demand tPlusDifference (gal)'].isna().any())
print("How many NA? ", Data23['Demand tPlusDifference (gal)'].isna().sum())

# Fill missing values with the moving average of a window size of 10
Data23['Demand tPlusDifference (gal)'] = Data23['Demand tPlusDifference (gal)'].fillna(Data23['Demand tPlusDifference (gal)'].rolling(10, min_periods=1).mean())

print("Is there any NA? ", Data23['Demand tPlusDifference (gal)'].isna().any())
print("How many NA? ", Data23['Demand tPlusDifference (gal)'].isna().sum())

# Fill missing values with the value from previous day
Data23['Demand tPlusDifference (gal)'] = Data23['Demand tPlusDifference (gal)'].fillna(Data23['Demand tPlusDifference (gal)'].shift(1440))

print("Is there any NA? ", Data23['Demand tPlusDifference (gal)'].isna().any())
print("How many NA? ", Data23['Demand tPlusDifference (gal)'].isna().sum())
if Data23['Demand tPlusDifference (gal)'].isna().any()==False:
    print("Good!")

###############################################################################
## 6. Rain column:
Rain_raw = pd.read_csv('Raw data/2023-06-01_2023-09-01_tower_wunderground_daily.csv', delimiter=',', encoding='utf-8')

# Change the format of the 'Date' column to '%m/%d/%Y %H:%M'
Rain_raw['Date'] = pd.to_datetime(Rain_raw['Date'])

Rain_raw['Date'] = Rain_raw['Date'].dt.strftime('%m/%d/%Y %H:%M')

# Write the rain data
Data23['Rain (in)'] = pd.merge(Data23, Rain_raw[['Date', 'precipTotal (Inches)']], on='Date', how='left')['precipTotal (Inches)']

# Treat the rain data
# Calculate the average rainfall value for each day
daily_avg_rainfall = Data23.groupby(Data23.index // 1440)['Rain (in)'].last().div(1440)

# Fill the preceding rows for each day with the calculated average
for day in range(0,92):
    Data23['Rain (in)'][day*1440:(day+1)*1440] = daily_avg_rainfall[day]

# Check for NAs    
print("Is there any NA? ", Data23['Rain (in)'].isna().any())
print("How many NA? ", Data23['Rain (in)'].isna().sum())
if Data23['Rain (in)'].isna().any()==False:
    print("Good!")

###############################################################################
## 6. RO and Well switches:
Data23['RO_Switch'] = 0 # The whole season RO was off due to the good precipitation.

Well_raw = pd.read_csv('Raw data/2023-06-01_2023-09-01_grassLab_an130_well_instantaneous.csv', delimiter=',', encoding='utf-8')

# Change the format of the 'Date' column to '%m/%d/%Y %H:%M'
Well_raw['Date'] = pd.to_datetime(Well_raw['Date'])

Well_raw['Date'] = Well_raw['Date'].dt.strftime('%m/%d/%Y %H:%M')

# Write the well pump data
Data23['Well_Switch'] = pd.merge(Data23, Well_raw[['Date', 'pulseDifference (gal)']], on='Date', how='left')['pulseDifference (gal)']

print("Is there any NA? ", Data23['Well_Switch'].isna().any())
print("How many NA? ", Data23['Well_Switch'].isna().sum())

# Fill missing values with the moving average of a window size of 10
Data23['Well_Switch'] = Data23['Well_Switch'].fillna(Data23['Well_Switch'].rolling(11, min_periods=1).mean()) # Changing 10 to 11 does not impact as we change it to zero and one

print("Is there any NA? ", Data23['Well_Switch'].isna().any())
print("How many NA? ", Data23['Well_Switch'].isna().sum())
if Data23['Well_Switch'].isna().any()==False:
    print("Good!")

# Changing data to switch status
Data23['Well_Switch'] = (Data23['Well_Switch'] > 0).astype(int)
Data23['Well_Switch'].sum()

# Make sure the dataframe is free of any NA
Data23.isna().any().any()
if Data23.isna().any().any()==False:
    print("Great job!")
    
# Export:
Data23.to_csv('Input Data 2023.csv', index=False)





