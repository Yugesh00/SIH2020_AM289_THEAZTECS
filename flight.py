import os
import requests
import json
from .root import app
import random
from mindmeld.core import FormEntity
class UnitNotFound(Exception):
    pass

CITY_NOT_FOUND_CODE = 400
Des_CITY_NOT_FOUND_CODE = 400
INVALID_API_KEY_CODE = 401
DEFAULT_originLocationCode = 'SYD'
DEFAULT_destinationLocationCode = 'BKK'
DEFAULT_departureDate = '2020-09-01'
DEFAULT_returnDate = '2020-09-05'
DEFAULT_max = '1'
DEFAULT_adults = '1'
FLIGHT_BASE_STRING = 'https://test.api.amadeus.com/v2/shopping/flight-offers'

transfer_form = {
    "entities": [
        FormEntity(
            entity="origin_city",
            role="origin",
            responses=["Sure. Flight from which city?"],
            retry_response=["That city is not correct. Please enter a correct city."],
        ),
        FormEntity(
            entity="origin_city",
            role="dest",
            responses=["To which city?"],
            retry_response=["That city is not correct. Please enter a correct city."],
        ),
        FormEntity(
            entity="sys_number",
            responses=["How many tickets do you want to book?"],
            retry_response=[
                "That number is not correct. "
                "Please try formatting the value like this '2'."
            ],
        ),
    ],
    "exit_keys": [
        "cancel",
        "cancel booking",
        "stop booking",
        "restart",
        "exit",
        "reset",
        "no",
        "nevermind",
        "stop",
        "back",
        "help",
        "stop it",
        "go back",
        "new task",
        "other",
        "return",
        "end",
    ],
    "exit_msg": "A couple of other tasks you can try are"
    " hotel booking and searching for a train",
    "max_retries": 1,
}



@app.auto_fill(intent='search_flight', form=transfer_form)
def search_flight(request, responder):
    try:
        for entity in request.entities:
            if entity["type"] == "origin_city":
                if entity["role"] == "origin":
                    selected_origin_city = (
                        entity["value"][0]["cname"]
                        if len(entity["value"]) > 0
                        else entity["text"]
                    )
                elif entity["role"] == "dest":
                    selected_destination_city = (
                        entity["value"][0]["cname"]
                        if len(entity["value"]) > 0
                        else entity["text"]
                    )
            else:
                selected_adults = (
                    entity["value"][0]["value"]
                    if len(entity["value"]) > 0
                    else entity["text"]
                )    
        selected_dod = DEFAULT_departureDate
        selected_dor = DEFAULT_returnDate
        selected_max = DEFAULT_max
        url_string = _construct_book_flight_api_url(selected_origin_city, selected_destination_city, selected_dod, selected_dor, selected_adults, selected_max)
        headers = {'Authorization' : 'Bearer gTpWkubknSVnpfKQEE75IwZPqDtg'}
        payload = {}
        flight_info = requests.request("GET",url_string, headers = headers, data = payload).json()
        # flight_info = json.loads(str(flight_infor))
    except ConnectionError:
        reply = "Sorry, I was unable to connect to the book flight API, please check your connection."
        responder.reply(reply)
        return
    except UnitNotFound:
        reply = "Sorry, I am not sure which unit you are asking for."
        responder.reply(reply)
        return

    try:
        x = flight_info['data'][0]['itineraries'][0]['segments'][0]['carrierCode']
        responder.slots['origin_city'] = selected_origin_city
        responder.slots['destination_city'] = selected_destination_city
        responder.slots['dod'] = selected_dod
        responder.slots['dor'] = selected_dor
        responder.slots['adult'] = selected_adults
        responder.slots['price'] = flight_info['data'][0]['price']['total']
        responder.slots['currency'] = flight_info['data'][0]['price']['currency']
        responder.slots['lastTicketingDate'] = flight_info['data'][0]['lastTicketingDate']
        responder.slots['numberOfBookableSeats'] = flight_info['data'][0]['numberOfBookableSeats']
        responder.slots['carrierCode'] = flight_info['dictionaries']['carriers'][x]
        responder.slots['code'] =random.choice(["T1H2E","A1Z3T","E2C1S"])
        responder.reply("Found a flight of {carrierCode} for {currency} {price}.\n No. of seats available are {numberOfBookableSeats} and last date for booking is {lastTicketingDate}.\n\nYou can also book this flight. \nUse this code '{code}' to start the booking process.")
        responder.listen()

    except:
        if int(flight_info['errors'][0]['status']) == CITY_NOT_FOUND_CODE:
            reply = "Sorry, I wasn't able to recognize that city."
            responder.reply(reply)
        if int(flight_info['errors'][0]['status']) == Des_CITY_NOT_FOUND_CODE:
            reply = "Sorry, I wasn't able to recognize that city."
            responder.reply(reply)
        elif int(flight_info['errors'][0]['status']) == INVALID_API_KEY_CODE:
            reply = "Sorry, the API key is invalid."
            responder.reply(reply)
    


# Helpers

def _construct_book_flight_api_url(selected_origin_city, selected_destination_city, selected_dod, selected_dor, selected_adults, selected_max):
    url_string = "{base_string}?originLocationCode={location}&destinationLocationCode={destination}&departureDate={ddate}&returnDate={rdate}&adults={adult}&max={max}".format(
        base_string=FLIGHT_BASE_STRING, location=selected_origin_city.replace(" ", "+"), destination=selected_destination_city.replace(" ", "+"), ddate=selected_dod, rdate=selected_dor,
        adult=selected_adults, max=selected_max)

    return url_string
 