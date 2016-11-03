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

# SOAP details
api = 'https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx?ver=2016-02-16'
TokenValue = Element('TokenValue').setText('5f0c1463-7047-4bc2-a2f8-8ce38b3eb269')
AccessToken = Element('AccessToken')
AccessToken.append(TokenValue)
trainDB = Client(api)
trainDB.set_options(soapheaders=AccessToken)

# Global variables  
trainsHome = []
numRows = 10000
LondonCodes = ['BFR', 'LBG', 'CST', 'CHX', 'EUS', 'FST', 'KGX', 'LST', 'MYB', 'PAD', 'LRB', 'SPX', 'STP', 'VIC', 'WAT', 'WAE']
LondonStationCodes = {
'LBG':'London Bridge',
'CST':'London Cannon Street',	
'CHX': 'London Charing Cross',
'VIC': 'London Victoria',
'WAE': 'London Waterloo East'
#London Waterloo East	WAE
}

# functions
def lookupDepartures(numRows,stationCode):
    StationBoard = trainDB.service.GetDepBoardWithDetails(numRows,stationCode)
    services = StationBoard.trainServices.service
    return services
    
def toBarnehurst(station):
    departingServices = lookupDepartures(numRows,station)
    for train in range(0,len(departingServices)):
            originName = departingServices[train].origin.location[0].locationName  
            destinationCode = departingServices[train].destination.location[0].crs
            destinationName = departingServices[train].destination.location[0].locationName
            departureTime = departingServices[train].std
            callingPointList = departingServices[train].subsequentCallingPoints.callingPointList[0]
            for callingPoint in range(0,len(callingPointList[0])):
                if callingPointList.callingPoint[callingPoint].locationName == 'Barnehurst':
                    BarnehurstCallingNumber = callingPoint 
                    if hasattr(departingServices[train].destination.location[0],'via') == True:
                        via = departingServices[train].destination.location[0].via
                        trainInfo = [departureTime, LondonStationCodes[station], 'to', destinationName, via]
                        trainsHome.append(trainInfo)
                    else: # destinationName != 'Barnehurst':                   
                        trainInfo = [departureTime, LondonStationCodes[station], 'to', destinationName, 'via', callingPointList.callingPoint[BarnehurstCallingNumber-1].locationName]
                        trainsHome.append(trainInfo)
                    #else:
                    #    trainInfo = [departureTime,LondonStationCodes[station], 'to', destinationName]
                    #    trainsHome.append(trainInfo)
    return trainsHome

# function call
print '\n your next trains home are \n'

for station in LondonStationCodes:
    toBarnehurst(str(station))
trainsHome = sorted(trainsHome, key = lambda x: x[0])

for train in trainsHome:
    print ' '.join(train)
raw_input('\n')