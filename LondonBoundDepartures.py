# python 2.7
# Accessing the Nation Rail Enquiries Live Departure Boards Web Service
# Using the python 2.7 suds library to format and send SOAP XML messages
# python -m pip install suds
# Current version op Open LDBWS to be found at https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx?ver=2016-02-16
# Documentation to be found at https://lite.realtime.nationalrail.co.uk/OpenLDBWS/
# My access token is '5f0c1463-7047-4bc2-a2f8-8ce38b3eb269' which must be transmitted in the SOAP header

LondonCodes = ['BFR', 'LBG', 'CST', 'CHX', 'EUS', 'FST', 'KGX', 'LST', 'MYB', 'PAD', 'LRB', 'SPX', 'STP', 'VIC', 'WAT', 'WAE']

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

# functions
def lookupDepartures(numRows,stationCode):
    StationBoard = trainDB.service.GetDepBoardWithDetails(numRows,stationCode)
    listoftrains = StationBoard.trainServices.service
    return listoftrains
   
def LondonBoundDepartureTimes(stationCode):
    listoftrains = lookupDepartures(numRows,stationCode)
    for train in range(0,len(listoftrains)):
        destinationCode = listoftrains[train].destination.location[0].crs
        destinationName = listoftrains[train].destination.location[0].locationName
        departureTime = listoftrains[train].std
        if destinationCode in LondonCodes:
            trainInfo = [departureTime, stationCode, 'to', destinationName]
            #print trainInfo
            trainsToLondon.append(trainInfo)
    return trainsToLondon

def LondonBound(fromStation):
    #fromStation = str(fromStation)
    LondonBoundDepartureTimes(fromStation)
    sorted(trainsToLondon, key = lambda x: x[0])
    for train in trainsToLondon:
        print ' '.join(train)
    
# Global variables
numRows = 1000    
trainsToLondon = []

# function call
print '\n Surbiton: SUR, Sheffield: SHF, Barnehurst: BNH \n'
fromStation = raw_input('departure station code: ')
LondonBound(fromStation)
raw_input()