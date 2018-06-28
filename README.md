# LateBus

The aim of this project is to analyse discrepancies between bus departure times and their time tables in San Francisco and build better prediction models

## Code features:
- Scrapes NextBus XML data in San Francisco, can quickly be adapted for other cities
- Doesn’t parse routes with no upcoming predictions
- Saves station predicted departure times in CSV 
- Saves vehicle location and speed data in CSV 
- Catches major parsing errors
- Runs three instances in parallel to get through all the predictions and vehicles quicker
- Runs in terminal if initialised through LateBus - Run Routelist 1,2,3

## Limitations:
- Creates new CSV files for each day
- Slow-ish sampling frequency - Based on your hardware and connection speed


Data sample for Latebus - all stations:

```
,Bus_route,Current_time,Stop_ID,Bus_ID,Prediction_time,Prediction_minutes,Prediction_seconds
0,1,08:34:02,4015,5578,08:37:00 PDT,2,177
1,1,08:34:02,4015,5538,08:44:00 PDT,9,597
```


Data sample for Latebus - all vehicles:

```
,Bus_route,Current_time,Bus_ID,Latitude,Longitude,Speed(km/h)
0,1,15:09:02,5518,37.795105,-122.399597,29
1,1,15:09:02,5572,37.784649,-122.46785,27
```


Data sample for LateBus - one station (needs to be updated):

```
['16:14:01', {'vehicle': ['busID: 8503', {'latitude': '37.7459909', 'longitude': '-122.450623', 'speed(km/h)': '0'}], 'minutes': '28', 'seconds': '1688', 'time': '16:42:10 PDT'}, {'vehicle': ['busID: 8514', {'latitude': '37.733738', 'longitude': '-122.434174', 'speed(km/h)': '21'}], 'minutes': '58', 'seconds': '3488', 'time': '17:12:10 PDT'}, {'vehicle': 'busID: 8503', 'minutes': '88', 'seconds': '5288', 'time': '17:42:10 PDT'}]
```

At the moment this code is running on my Raspberry Pi collecting departure time predictions and bus location data every few minutes for all stations and vehicles in San Francisco.



## Requirements:
- To run this code you will need numpy and pandas packages
- I am running it in Spyder


## TO DOs:
- Update LateBus - one station.py to save to CSV format
- There are still a bug that cause the code to crash occasionally
- After restart the code needs to add the the existing file not overwrite it


## Vision for this project:
- Collect enough data to be able to make a meaningful analysis
- Create a better bus departure prediction model, ideally with ML
- Collect data across the San Francisco public transportation system (MUNI) and make the historic data available to others 
