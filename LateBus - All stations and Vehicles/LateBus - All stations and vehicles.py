import requests 
import route_stops

from lxml import etree

import time
from datetime import datetime 


import numpy as np
import pandas as pd

import socket


df_vehicles = pd.DataFrame(np.nan, index=[0], columns=['Bus_route', 'Current_time', 'Bus_ID', 'Latitude', 'Longitude', 'Speed(km/h)'])
count = 0
df_predictions = pd.DataFrame(np.nan, index=[0], columns=['Bus_route', 'Current_time', 'Stop_ID', 'Bus_ID', 'Prediction_time', 'Prediction_minutes', 'Prediction_seconds'])
count_pred = 0

previous = "0"

check_no_vehicles = 0

Vehicles_data = []
all_routes_predictions = []

keylist = sorted(route_stops.Route_stops)


def EveryMinute():
    global Vehicles_data, all_routes_predictions, previous, check_no_vehicles
    global df_vehicles, df_predictions, count, count_pred 


    # checks the date, if it's the same day or is it already next day (after midnight)
    # if it's new day, start from zero, with empty data frames and lists
    today_day = datetime.now().strftime("%d%m%Y")
    if today_day != previous:
        Vehicles_data = []
        count = 0
        df_vehicles = pd.DataFrame(np.nan, index=[0], columns=['Bus_route', 'Current_time', 'Bus_ID', 'Latitude', 'Longitude', 'Speed(km/h)'])
        all_routes_predictions = []
        count_pred = 0
        df_predictions = pd.DataFrame(np.nan, index=[0], columns=['Bus_route', 'Current_time', 'Stop_ID', 'Bus_ID', 'Prediction_time', 'Prediction_minutes', 'Prediction_seconds'])
        previous = today_day
        print(previous)
        
    # get the route and all bus stops on this route
    # use route and bus stops data to get data from the web
    for route in keylist:
        check_no_vehicles = 0
       # print(route_stops.Route_stops)
            # print(route)
        with requests.Session() as s:
           
            # getting Vehicle data
            c = ('http://webservices.nextbus.com/service/publicXMLFeed?command=vehicleLocations&a=sf-muni&r={}&t=0'.format(route))
            req_2 = s.get(c)                                # sending request
            file_content = req_2.content                    # getting response
            parser = etree.XMLParser(recover=True)          # recover=True is keyword argument for try hard to parse through broken XML
            xml = etree.fromstring(file_content, parser)    # parsing XML
            tree_2 = xml

            for chil_d in tree_2.iter('vehicle'): # find element with tag "vehicle" and get its attributes 
                    #print(chil_d)
                    vehicle = []
                    vehicle = [str(route), datetime.now().strftime('%H:%M:%S'), chil_d.attrib['id'], chil_d.attrib['lat'], chil_d.attrib['lon'], chil_d.attrib['speedKmHr']]
                    Vehicles_data.append(vehicle)
                    df_vehicles.loc[count] = vehicle
                    count = count +1
                    check_no_vehicles = 1
                    #print(vehicle)

        # if list Vehicles_data is not empty, save the data
            if len(Vehicles_data) > 0:
               # print(Vehicles_data)
            # save Vehicles data as a csv file
                today_day = datetime.now().strftime("%d%m%Y")
                file_name_v = 'All_vehicles_{}.csv'.format(today_day)
                df_vehicles.to_csv(file_name_v, mode = 'w', header = 'False')

            #if there is no Vehicle data available for this route, go to the next route
            if check_no_vehicles == 1:

            # getting prediction data
    
                all_stops = route_stops.Route_stops[route]
                for stop in all_stops:    #for each stop on a route, get prediction data
           
                    b1 = 'http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=sf-muni&r={}&s={}'.format(route, stop)
                    req = s.get(b1)
                    file_content = req.content
                    parser = etree.XMLParser(recover=True)
                    xml = etree.fromstring(file_content, parser)
                    root = xml
                
                    for child in root.iter('prediction'): #for element with tag "prediction" get its attributes

                        each_prediction = []
                        epoch_time = round(int(child.attrib['epochTime'])/1000)
                        each_prediction = [str(route), datetime.now().strftime('%H:%M:%S'), str(stop), child.attrib['vehicle'], time.strftime("%H:%M:%S %Z", time.localtime(epoch_time)), child.attrib['minutes'], child.attrib['seconds']]
                        all_routes_predictions.append(each_prediction)
                        #add prediction data as a row in the data frame
                        df_predictions.loc[count_pred] = each_prediction
                        count_pred = count_pred + 1
                        #print(each_prediction)
               
        #if list all_routes_prediction is not empty, save data frame with predictions as csv
                if len(all_routes_predictions) > 0:
               # print(all_routes_predictions)
                    today_day = datetime.now().strftime("%d%m%Y")
                    file_name = 'All_predictions_{}.csv'.format(today_day)
                    df_predictions.to_csv(file_name, mode = 'w', header = 'False')
        
            
        
      
while True:
        try:
            t = datetime.now().strftime('%H:%M:%S')
            if "23:00:00" < t < "05:00:00":
                time.sleep(300)
            EveryMinute()
            print('End.')
            time.sleep(60)
        except requests.exceptions.HTTPError as errh:
            print ("Http Error: ", errh)
            time.sleep(300)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting: ", errc)            
            time.sleep(300)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error: " ,errt)
            time.sleep(300)
        except requests.exceptions.RequestException as e:
            print("OOPS!! General Error")
            print(str(e))
            time.sleep(300)
        except socket.error as soc:
            print("Socket error: ", soc)
            time.sleep(300)
#        except KeyboardInterrupt:
 #           print("Someone closed the program")
        except etree.ParseError as e:
            print("Parse Error: ", e)
            time.sleep(300)
