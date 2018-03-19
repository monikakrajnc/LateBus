# LateBus

The aim of this project is to analyse discrepancies between bus departure times and their time tables in San Francisco

## Code features:
- Scrapes NextBus XML data, can be quickly modified for other 
- Only collects data during operating hours
- Adds bus location data to each prediction

## Limitations:
- Currently collects data only for one station
- Currently only saves data in proprietary list format
- Creates new file for each day

Data sample:

‘’’’’’
['16:14:01', {'vehicle': ['busID: 8503', {'latitude': '37.7459909', 'longitude': '-122.450623', 'speed(km/h)': '0'}], 'minutes': '28', 'seconds': '1688', 'time': '16:42:10 PDT'}, {'vehicle': ['busID: 8514', {'latitude': '37.733738', 'longitude': '-122.434174', 'speed(km/h)': '21'}], 'minutes': '58', 'seconds': '3488', 'time': '17:12:10 PDT'}, {'vehicle': 'busID: 8503', 'minutes': '88', 'seconds': '5288', 'time': '17:42:10 PDT'}]

‘’’’’’

At the moment this code is running on my Raspberry Pi collecting departure time prediction and bus location data on a minute by minute basis.

-------

## TO DOs:
- Fix error on connectivity issues or issues with prediction system
- Save data to CSV or JSON
- Include more stations and bus lines

-------

## Vision for this project:
- Collect enough data to be able to make a meaningful analysis
- Create a better bus departure prediction model, ideally with ML
- Collect data across the San Francisco public transportation system (MUNI) and make the historic data available to others 
