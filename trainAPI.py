# python 2.7
# Accessing the Nation Rail Enquiries Live Departure Boards Web Service
# Using the python 2.7 suds library to format and send SOAP XML messages
# python -m pip install suds
# Current version op Open LDBWS to be found at https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx?ver=2016-02-16
# Documentation to be found at https://lite.realtime.nationalrail.co.uk/OpenLDBWS/
# My access token is '5f0c1463-7047-4bc2-a2f8-8ce38b3eb269' which must be transmitted in the SOAP header

# query should look like this
#b'<?xml version="1.0" encoding="UTF-8"?><SOAP-ENV:Envelope xmlns:ns1="http://tha
#lesgroup.com/RTTI/2016-02-16/ldb/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-i
#nstance" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns0="h
#ttp://schemas.xmlsoap.org/soap/envelope/"><SOAP-ENV:Header/><ns0:Body><ns1:GetDe
#partureBoardRequest><ns1:numRows>10</ns1:numRows><ns1:crs>SUR</ns1:crs></ns1:Get
#DepartureBoardRequest></ns0:Body></SOAP-ENV:Envelope>'

LondonStationCodes = {
#London Blackfriars	BFR
'LBG':'London Bridge',
'CST':'London Cannon Street',	
'CHX': 'London Charing Cross'	
#London Euston	EUS
#London Fenchurch Street	FST
#London Kings Cross	KGX
#London Liverpool Street	LST
#London Marylebone	MYB
#London Paddington	PAD
#London Road (Brighton)	LRB
#London Road (Guildford)	LRD
#London St Pancras (Intl)	SPX
#London St Pancras International	STP
#London Victoria	VIC
#London Waterloo	WAT
#London Waterloo East	WAE
}

LondonCodes = ['BFR', 'LBG', 'CST', 'CHX', 'EUS', 'FST', 'KGX', 'LST', 'MYB', 'PAD', 'LRB', 'SPX', 'STP', 'VIC', 'WAT', 'WAE']

# client formats the query, sends SOAP packets
# Element adds headers to SOAP packets
# logging allows to see what is being transmitted

from suds.client import Client
from suds.sax.element import Element
#from suds import WebFault
import logging
import re
import time

logging.basicConfig(level=logging.INFO)
#logging.basicConfig(level=logging.DEBUG)

api = 'https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx?ver=2016-02-16'
TokenValue = Element('TokenValue').setText('5f0c1463-7047-4bc2-a2f8-8ce38b3eb269')
AccessToken = Element('AccessToken')
AccessToken.append(TokenValue)

# sets up envelope and header
trainDB = Client(api)
trainDB.set_options(soapheaders=AccessToken)

# prints the data retrieved, proof it worked
# print(trainDB)

#save API response as a python object
def lookupDepartures(numRows,stationCode):
    StationBoard = trainDB.service.GetDepBoardWithDetails(numRows,stationCode)
    services = StationBoard.trainServices.service
    #subsequentDepartures = StationBoard.trainServices.service.subsequentCallingPoints.callingPointList[0]
    #print services.subsequentCallingPoints.callingPointList[0].callingPoint[1].locationName
    #print services
    return services
    
   
def LondonBoundDepartureTimes(stationCode):
    services = lookupDepartures(numRows,stationCode)
    for train in range(0,len(services)):
        destinationCode = services[train].destination.location[0].crs
        destinationName = services[train].destination.location[0].locationName
        departureTime = services[train].std
        if destinationCode in LondonCodes:
            trainInfo = [departureTime, 'to', destinationName]
            #print trainInfo
            trainsToLondon.append(trainInfo)
    return trainsToLondon

def viaBexleyheath(station):
    departingServices = lookupDepartures(numRows,station)
    for train in range(0,len(departingServices)):
            originName = departingServices[train].origin.location[0].locationName  
            destinationCode = departingServices[train].destination.location[0].crs
            destinationName = departingServices[train].destination.location[0].locationName
            departureTime = departingServices[train].std
            #print departureTime, destinationName
            if hasattr(departingServices[train].destination.location[0],'via') == True:
                via = departingServices[train].destination.location[0].via
                viaBexleyheath = re.match('via Bexleyheath',via)
                if viaBexleyheath != None:
                    trainInfo = [departureTime, LondonStationCodes[station], 'to', destinationName, via]
                    #print trainInfo
                    trainsHome.append(trainInfo)
    return trainsHome
                    
def toBarnehurst(station):
    departingServices = lookupDepartures(numRows,station)
    for train in range(0,len(departingServices)):
            originName = departingServices[train].origin.location[0].locationName  
            destinationCode = departingServices[train].destination.location[0].crs
            destinationName = departingServices[train].destination.location[0].locationName
            departureTime = departingServices[train].std
            callingPointList = departingServices[train].subsequentCallingPoints.callingPointList[0]
            #print callingPointList
            for callingPoint in range(0,len(callingPointList[0])):
                #print train, callingPointList.callingPoint[callingPoint].locationName
                if callingPointList.callingPoint[callingPoint].locationName == 'Barnehurst':
                    BarnehurstCallingNumber = callingPoint 
                    if hasattr(departingServices[train].destination.location[0],'via') == True:
                        via = departingServices[train].destination.location[0].via
                        trainInfo = [departureTime, LondonStationCodes[station], 'to', destinationName, via]
                        #print trainInfo
                        trainsHome.append(trainInfo)
                    else:# destinationName != 'Barnehurst':                   
                        trainInfo = [departureTime, LondonStationCodes[station], 'to', destinationName, 'via', callingPointList.callingPoint[BarnehurstCallingNumber-1].locationName]
                        #print trainInfo
                        trainsHome.append(trainInfo)
                    #else:
                    #    trainInfo = [departureTime,LondonStationCodes[station], 'to', destinationName]
                    #    trainsHome.append(trainInfo)
    return trainsHome
  
trainsHome = []
numRows = 10000

def workToHome():
#    viaBexleyheath('LBG')
#    viaBexleyheath('CST')
    toBarnehurst('LBG')
    toBarnehurst('CST')
    sorted(trainsHome, key = lambda x: x[0])
    #print trainsHome
    for train in trainsHome:
        print ' '.join(train)

    
        
trainsToLondon = []
def LondonBound(fromStation):
    #fromStation = str(fromStation)
    LondonBoundDepartureTimes(fromStation)
    sorted(trainsToLondon, key = lambda x: x[0])
    for train in trainsToLondon:
        print ' '.join(train)

workToHome()
#LondonBound('BNH')
#lookupDepartures(10,'BNH')