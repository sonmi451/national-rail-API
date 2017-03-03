# python 2.7
# Accessing the Nation Rail Enquiries Live Departure Boards Web Service
# Using the python 2.7 suds library to format and send SOAP XML messages
# python -m pip install suds
# Current version op Open LDBWS to be found at https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx?ver=2016-02-16
# Documentation to be found at https://lite.realtime.nationalrail.co.uk/OpenLDBWS/
# My access token is '5f0c1463-7047-4bc2-a2f8-8ce38b3eb269' which must be transmitted in the SOAP header

# client formats the query, sends SOAP packets
# Element adds headers to SOAP packets
# logging allows to see what is being transmitted

from suds.client import Client
from suds.sax.element import Element
import logging
import csv
import re

# station crs codes
import csv
reader = csv.reader(open('station_codes.csv'))
station_to_crs = {}
crs_to_station = {}
for row in reader:
    key0 = row[0]
    key1 = row[1]
    station_to_crs[key0] = row[1]
    crs_to_station[key1] = row[0]

LondonCodes = ['BFR', 'LBG', 'CST', 'CHX', 'EUS', 'FST', 'KGX', 'LST', 'MYB', 'PAD', 'VIC', 'WAT', 'WAE']

# SOAP details
api = 'https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx?ver=2016-02-16'
TokenValue = Element('TokenValue').setText('5f0c1463-7047-4bc2-a2f8-8ce38b3eb269')
AccessToken = Element('AccessToken')
AccessToken.append(TokenValue)
trainDB = Client(api)
trainDB.set_options(soapheaders=AccessToken)

# functions
def lookupDepartures(numRows,departStationCode,arriveStationCode):
    StationBoard = trainDB.service.GetDepBoardWithDetails(numRows,departStationCode,arriveStationCode)
    #print StationBoard
    if hasattr(StationBoard,'trainServices') == True:
        services = StationBoard.trainServices.service
        for train in range(0,len(services)):
            originStationName = services[train].origin.location[0].locationName
            originStationCode = services[train].origin.location[0].crs
            terminateStationCode = services[train].destination.location[0].crs
            terminateStationName = services[train].destination.location[0].locationName    
            departureTime = services[train].std
            callingPointList = services[train].subsequentCallingPoints.callingPointList[0]
            for callingPoint in range(0,len(callingPointList[0])):
                if callingPointList.callingPoint[callingPoint].crs == arriveStationCode:
                    arrivialStationName = callingPointList.callingPoint[callingPoint].locationName
                    arrivalTime = callingPointList.callingPoint[callingPoint].st
                    if terminateStationCode == arriveStationCode:
                        trainInfo = [departureTime, 'from', crs_to_station[departStationCode], 'to', terminateStationName, 'arriving at', arrivalTime]
                        trainServices.append(trainInfo)
                    else:
                        trainInfo = [departureTime, 'from', crs_to_station[departStationCode], 'to', terminateStationName, 'calling at', arrivialStationName, 'at', arrivalTime]
                        trainServices.append(trainInfo)
                    #print ' '.join(trainInfo)
    elif departStationCode in LondonCodes or arriveStationCode in LondonCodes:
        print '...'
    else:
        print 'No direct trains from', crs_to_station[departStationCode], 'to', crs_to_station[arriveStationCode]

# global variables
trainServices = []
numRows = 1000
print '\n Please enter your station name. For London terminals use ''London''.'
departStation = raw_input('\n travelling from: ')
arriveStation = raw_input('\n travelling to: ')
print '\n checking train times... \n'
if (departStation == 'London' or departStation in station_to_crs) and (arriveStation == 'London' or arriveStation in station_to_crs):
    if departStation == 'London':
        arriveStationCode = station_to_crs[arriveStation]
        for LondonCode in LondonCodes:          
            lookupDepartures(numRows,LondonCode,arriveStationCode)
    elif arriveStation == 'London':
        departStationCode = station_to_crs[departStation]
        for LondonCode in LondonCodes:
            #print departStationCode, departStation, LondonCode, crs_to_station[LondonCode]
            lookupDepartures(numRows,departStationCode,LondonCode)
    else:
        departStationCode = station_to_crs[departStation]
        arriveStationCode = station_to_crs[arriveStation]
        lookupDepartures(numRows,departStationCode,arriveStationCode)
else:
    print 'invalid station name'

# Results
trainServices = sorted(trainServices)
for train in trainServices:
    print ' '.join(train)
print '\n We\'re going nowhere slowly but we\'re seeing all the sights. \n'

raw_input()