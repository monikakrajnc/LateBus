#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 10:53:40 2018

@author: monikakrajnc
"""



import requests, route_stops

from urllib.request import urlopen

from lxml import etree


import time
from datetime import datetime, timedelta

#import csv
import numpy as np
import pandas as pd

from requests.exceptions import ConnectionError


#Create two empty data frames
df_vehicles = pd.DataFrame(np.nan, index=[0], columns=['Bus_route', 'Current_time', 'Bus_ID', 'Latitude', 'Longitude', 'Speed(km/h)'])
count = 0
df_predictions = pd.DataFrame(np.nan, index=[0], columns=['Bus_route', 'Current_time', 'Stop_ID', 'Bus_ID', 'Prediction_time', 'Prediction_minutes', 'Prediction_seconds'])
count_pred = 0



previous = "0"   #or datetime.now().strftime("%d%m%Y")

check_no_vehicles = 0

Vehicles_data = []
all_routes_predictions = []

#Sort all existing routes and use selected routes in this code
keylist = sorted(route_stops.Route_stops)
#print(keylist)
keylist_1 = keylist[28:54]





def EveryMinute():
    global Vehicles_data, all_routes_predictions, previous 
    global count, count_pred, df_vehicles, df_predictions

    #check the day, if it's the same day or is it already next day (after midnight)
    #if it's new day, start from zero, with empty data frames and lists
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
        
        
        #this function enables you to get all vehicles data that are on the specific route
    def Funkcija_vehicle(route):

        global check_no_vehicles
        global count 
  
        
      #Vehicle data from XML
        c = ('http://webservices.nextbus.com/service/publicXMLFeed?command=vehicleLocations&a=sf-muni&r=' + route + '&t=0')

        file_content = urlopen(c).read()
        parser = etree.XMLParser(recover=True)
        xml = etree.fromstring(file_content, parser)
        tree_2 = xml
 

        for chil_d in tree_2: # loop through all elements in the body

            if chil_d.tag == 'vehicle':   # find element with tag vehicle and get its attributes
                vehicle = []
                vehicle = [str(route), datetime.now().strftime('%H:%M:%S'), chil_d.attrib['id'], chil_d.attrib['lat'], chil_d.attrib['lon'], chil_d.attrib['speedKmHr']]
                Vehicles_data.append(vehicle)
                df_vehicles.loc[count] = vehicle
                count = count +1
                check_no_vehicles = 1
            else:
                if check_no_vehicles == 1:
                            # if list Vehicles_data is not empty, save these data
                    if len(Vehicles_data) > 0:
                    # save Vehicles data as csv format to use later
                        today_day = datetime.now().strftime("%d%m%Y")
                        file_name_v = 'Routelist2_All_vehicles_' + today_day +'.csv'
                        df_vehicles.to_csv(file_name_v, mode = 'w', header = 'False') 

                        Funkcija_prediction(route)
                continue
                        
       
   #next function enables you to get all arrivals predictions for each bus stop
    def Funkcija_prediction(route):
        global count_pred 
        #getting prediction data from XML
        a = ('http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=sf-muni&r=%s' % (route))

        all_stops = route_stops.Route_stops[route]
        for stop in all_stops:    #for each stop on a route, get prediction data
            b = (a + '&s=%s' % stop)

            file_content_1 = urlopen(b).read()
            parser_1 = etree.XMLParser(recover=True)
            xml = etree.fromstring(file_content_1, parser_1)
            tree = xml


            for child in tree: #go through element named body (First level)

                for child_1 in child: #loop through all elements under 1st level elements ("predictions") - Second level
                    for child_2 in child_1: #elements that are on the 3rd level ("direction")
                        if child_2.tag == 'prediction': #for each "prediction" element, get its attributes
                            each_prediction = []
                            epoch_time = round(int(child_2.attrib['epochTime'])/1000)
                            each_prediction = [str(route), datetime.now().strftime('%H:%M:%S'), str(stop), child_2.attrib['vehicle'], time.strftime("%H:%M:%S %Z", time.localtime(epoch_time)), child_2.attrib['minutes'], child_2.attrib['seconds']]
                            all_routes_predictions.append(each_prediction)
                                #add prediction data as row in data frame
                            df_predictions.loc[count_pred] = each_prediction
                            count_pred = count_pred + 1
                        else:
                            continue
        #if list all_routes_prediction is not empty, save data frame with predictions as csv
        if len(all_routes_predictions) > 0:
            today_day = datetime.now().strftime("%d%m%Y")
            file_name = 'Routelist2_All_predictions_' + today_day +'.csv'
            df_predictions.to_csv(file_name, mode = 'w', header = 'False')
   
    #get the route and all bus stops on that route
    #use route and bus stop data to get data from the web
    for route in keylist_1:
        print(route)

        Funkcija_vehicle(route)            
        
#def random1():       
while True:
        try:
            t = datetime.now().strftime('%H:%M:%S')
            if "23:00:00" < t < "05:00:00":
                time.sleep(300)

            EveryMinute()
            print('End_2.')
            time.sleep(60)
    
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
            time.sleep(180)
        except KeyboardInterrupt:
            print("Someone closed the program")


