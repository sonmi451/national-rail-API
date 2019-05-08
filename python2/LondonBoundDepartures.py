'''
Python 2.7
Accessing the Nation Rail Enquiries Live Departure Boards Web Service
Using the python 2.7 suds library to format and send SOAP XML messages
install with python -m pip install suds

Current version op Open LDBWS to be found at https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx?ver=2016-02-16
Documentation to be found at https://lite.realtime.nationalrail.co.uk/OpenLDBWS/
My access token must be transmitted in the SOAP header

query should look like this
b'<?xml version="1.0" encoding="UTF-8"?><SOAP-ENV:Envelope xmlns:ns1="http://tha
lesgroup.com/RTTI/2016-02-16/ldb/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-i
nstance" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns0="h
ttp://schemas.xmlsoap.org/soap/envelope/"><SOAP-ENV:Header/><ns0:Body><ns1:GetDe
partureBoardRequest><ns1:numRows>10</ns1:numRows><ns1:crs>SUR</ns1:crs></ns1:Get
DepartureBoardRequest></ns0:Body></SOAP-ENV:Envelope>
'''

LondonCodes = ['BFR', 'LBG', 'CST', 'CHX', 'EUS', 'FST', 'KGX', 'LST', 'MYB', 'PAD', 'LRB', 'SPX', 'STP', 'VIC', 'WAT', 'WAE']

# client formats the query, sends SOAP packets
# Element adds headers to SOAP packets
# logging allows to see what is being transmitted

from suds.client import Client
from suds.sax.element import Element
import logging
from token import TOKEN

# SOAP details
api = 'https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx?ver=2016-02-16'
TokenValue = Element('TokenValue').setText(TOKEN)
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
        departureTimeDelay = listoftrains[train].etd
        if destinationCode in LondonCodes:
            trainInfo = [departureTime, '[' , departureTimeDelay, ']', 'to', destinationName]
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
print '\n Surbiton: SUR, Barnehurst: BNH, Theale:THE\n'
fromStation = raw_input('departure station code: ')
LondonBound(fromStation)

print '\n We\'re going nowhere slowly but we\'re seeing all the sights. \n'

raw_input()
