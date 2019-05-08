'''
Python 3
access token must be sent in the soap header when querying the endpoint
ACCESS_TOKEN = {'AccessToken':TOKEN}
put `_soapheaders=ACCESS_TOKEN` in zeep Client query e.g.:
Client('https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx?ver=2017-10-01') \
.service.GetServiceDetails(service_id, _soapheaders=ACCESS_TOKEN)'''

################################################################################
## IMPORT ######################################################################

from zeep import Client
from token import TOKEN
from station_codes import STATION_CODE_LIST

################################################################################
## CONSTANTS ###################################################################

DEBUG = True

ACCESS_TOKEN = {'AccessToken':TOKEN}
LIVE_DEPARTURE_BOARD = \
Client('https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx?ver=2017-10-01')

# Request data
NUM_TRAINS = 10
STATION = 'SUR'

################################################################################
## FUNCTIONS ###################################################################

def get_service_details(service_id):
    ''' make SOAP request to get the details of a train service '''

    # Call api and return data
    service_information = LIVE_DEPARTURE_BOARD.service.GetServiceDetails \
    (service_id, _soapheaders=ACCESS_TOKEN)

    return service_information

def get_departure_board(num_trains, station):
     # Call api and return data
    departure_board = LIVE_DEPARTURE_BOARD.service.GetDepartureBoard \
        (num_trains, station, _soapheaders=ACCESS_TOKEN)

    return departure_board

def get_service_details(service_id):
     # Call api and return data
    service_details = LIVE_DEPARTURE_BOARD.service.GetServiceDetails \
        (service_id, _soapheaders=ACCESS_TOKEN)
    return service_details

def get_fastest_departures():
    '''GetFastestDepartures'''
    fastest_departures = LIVE_DEPARTURE_BOARD.service.GetServiceDetails \
        ('SUR', _soapheaders=ACCESS_TOKEN)
    return fastest_departures

################################################################################
## CHECK VALID CODE ############################################################

def station_code_check(code):
    ''' Check the station codes are valid '''
    if code in STATION_CODE_LIST.values():
        return True
    else:
        return False
