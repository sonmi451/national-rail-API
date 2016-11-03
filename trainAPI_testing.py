# python 2.7
# Accessing the Nation Rail Enquiries Live Departure Boards Web Service
# Using the python 2.7 suds library to format and send SOAP XML messages
# python -m pip install suds
# Current version op Open LDBWS to be found at https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx?ver=2016-02-16
# Documentation to be found at https://lite.realtime.nationalrail.co.uk/OpenLDBWS/
# My access token is '5f0c1463-7047-4bc2-a2f8-8ce38b3eb269' which must be transmitted in the SOAP header

from suds.client import Client
from suds.sax.element import Element

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
    services = StationBoard.trainServices.service
    print services
    for service in services:
        callingPointList = service.subsequentCallingPoints.callingPointList[0]
        #print callingPointList
        for callingPoint in range(0,len(callingPointList[0])):
            print callingPointList.callingPoint[callingPoint].locationName
               
        
# global variables
numRows = 10000   
fromStation = 'BNH'
# function call
print '\n Surbiton: SUR, Sheffield: SHF, Barnehurst: BNH \n'
#fromStation = raw_input('departure station code: ')

lookupDepartures(numRows,fromStation)
#raw_input()