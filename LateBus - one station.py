
import threading

import requests


import pprint
from threading import Timer

import xml.etree.ElementTree as ET

import time

#import datetime

from datetime import datetime, timedelta

Predictions = []
n = 0

def EveryMinute():
    global Predictions, n
    Timer(60.0, EveryMinute).start() # called function EveryMinute every minute
   
    req = requests.get('http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=sf-muni&r=52&s=3696&useShortTitles=true')
    tree = ET.fromstring(req.text)
    
    req_2 = requests.get('http://webservices.nextbus.com/service/publicXMLFeed?command=vehicleLocations&a=sf-muni&r=52&t=0')
    tree_2 = ET.fromstring(req_2.text)


    def funkcija_1(tree_2):
        Vehicles_data = []
        for child in tree_2:
    #print(child)
            if child.tag == 'vehicle':
                vehicle = []
                vehicle.append('busID'+': '+ child.attrib['id'])
                vehicle.append({'latitude': child.attrib['lat'],
                                'longitude': child.attrib['lon'],
                                'speed(km/h)': child.attrib['speedKmHr']})
                Vehicles_data.append(vehicle)
        return(Vehicles_data)



    def funkcija_2(tree_2, nic):
        Vehicles_data = funkcija_1(tree_2)
    #print(Vehicles_data)
        for i in Vehicles_data:
            #print(i)
            if nic in i[0]:
 #               print(i[0])
                return(i)


    def funkcija_3() :                        
        each_minute.append(datetime.now().strftime('%H:%M:%S'))  #append current time
        for child in tree: # loop through all the routes
            for child_1 in child: #go through all elements named predictions
                for child_2 in child_1: #go through each element named direction
                    if child_2.tag == 'prediction':
                        epoch_time = round(int(child_2.attrib['epochTime'])/1000)

                        #date should be at the beginning of the list, to easier differentiet between days
                        if len(Predictions) == 0:
                        #just the date
                          date = time.strftime("%a, %d %b %Y", time.localtime(epoch_time))
                          Predictions.append(date)
                  
                    #just the time
                        d_time = time.strftime("%H:%M:%S %Z", time.localtime(epoch_time))
                    #print(Vehicles_data)
                        bus_info = funkcija_2(tree_2, child_2.attrib['vehicle'])
                        #print(bus_info)
                        if bus_info[0] not in all_buses:   #this part is just to prevent doubled the data for the vehicles location, when bus has already scheduled 2 prediction times 
                            all_buses.append(bus_info[0])
                            #print(bus_info)
                            each_minute.append({'time': d_time,         
                                                'seconds': child_2.attrib['seconds'],
                                                'minutes': child_2.attrib['minutes'],
                                                'vehicle': bus_info})
                        else:
                            each_minute.append({'time': d_time,         
                                                'seconds': child_2.attrib['seconds'],
                                                'minutes': child_2.attrib['minutes'],
                                                'vehicle': bus_info[0]})
                                                       
        print(each_minute)
        Predictions.append(each_minute) #each time when you go through the function Everytime, append list each_minute with data to list Predictions
        #print(Predictions)

    if len(Predictions) > 0:
        each_minute = []
        all_buses = []

        for child in tree: # loop through all the routes
            if child.get('dirTitleBecauseNoPredictions'): #== 'Outbound to Persia + Prague':
                n = 1
            else: 
                if n == 1:
                    Predictions = []
                    n = 0
                    funkcija_3()
                else:
                    funkcija_3() 
 
    else: 
        each_minute = []
        all_buses = []
           
        funkcija_3()            


    if n != 1 and len(Predictions) > 0:
# save the routes dictionary to a text file (routedata1.py) to use later
        a = datetime.now().strftime("%d%m%Y")
        b = 'busStop3696_predictions_every_minute_' + a +'.py'
        fo = open(b, 'w')
        fo.write('allPredictions = ' + pprint.pformat(Predictions))
        fo.close()



 
EveryMinute()


