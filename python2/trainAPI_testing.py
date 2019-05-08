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

from suds.client import Client
from suds.sax.element import Element
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
