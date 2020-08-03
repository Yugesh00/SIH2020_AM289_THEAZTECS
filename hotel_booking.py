import os
import requests
import json
from .root import app
from mindmeld.core import FormEntity
import random

class UnitNotFound(Exception):
    pass


CITY_NOT_FOUND_CODE = 400
INVALID_API_KEY_CODE = 401
DEFAULT_cityCode = 'DEL'
HOTEL_BASE_STRING = 'https://test.api.amadeus.com/v2/shopping/hotel-offers'

transfer_form = {
    "entities": [
        FormEntity(
            entity="origin_city",
            responses=["Sure. In Which city?"],
            retry_response=["That city is not correct. Please enter a correct city."],
        ),
        FormEntity(
            entity="sys_number",
            responses=["How many rooms do you want?"],
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
    " flight booking and searching for a train",
    "max_retries": 1,
}


@app.auto_fill(intent='search_hotel' ,form=transfer_form)
def search_hotel(request, responder):
    """
    When the user asks for weather, return the weather in that location or use San Francisco if no
      location is given.
    """
   

    try:
        for entity in request.entities:
            if entity["type"] == "origin_city":
                selected_city = (
                    entity["value"][0]["cname"]
                    if len(entity["value"]) > 0
                    else entity["text"]
                )
            else:
                selected_rooms = (
                    entity["value"][0]["value"]
                    if len(entity["value"]) > 0
                    else entity["text"]
                )    
        # Get weather information via the API
        url_string = _construct_search_hotel_api_url(selected_city)
        headers = {'Authorization' : 'Bearer rfl94dxYGEALKkI01KZKiyybZr31'}
        payload = {}
        # hotel_info = requests.get(url_string, headers=headers).json()
        hotel_info = requests.request("GET", url_string, headers = headers, data = payload).json()
        
        # hotel_info = json.loads(str(hotel_infor))
    except ConnectionError:
        reply = "Sorry, I was unable to connect to the book train API, please check your connection."
        responder.reply(reply)
        return
    except UnitNotFound:
        reply = "Sorry, I am not sure which unit you are asking for."
        responder.reply(reply)
        return

    try:
        responder.slots['room'] = selected_rooms 
        responder.slots['currency'] = hotel_info['data'][0]['offers'][0]['price']['currency']
        responder.slots['price'] = hotel_info['data'][0]['offers'][0]['price']['total'] 
        responder.slots['name'] = hotel_info['data'][0]['hotel']['name']
        responder.slots['rating'] = hotel_info['data'][0]['hotel']['rating']
        responder.slots['lines'] = hotel_info['data'][0]['hotel']['address']['lines'][0]
        responder.slots['postal_code'] = hotel_info['data'][0]['hotel']['address']['postalCode']
        responder.slots['city_name'] = hotel_info['data'][0]['hotel']['address']['cityName']
        responder.slots['phone'] = hotel_info['data'][0]['hotel']['contact']['phone']
        # responder.slots['email'] = hotel_info['data'][0]['hotel']['contact']['email']
        responder.slots['description'] = hotel_info['data'][0]['hotel']['description']['text']
        responder.reply("Found a hotel in *{city_name}*, \n*{name}* having rating *{rating}* for *{currency} {price}*. \n{description}\n*Address-* {lines}, {city_name}-{postal_code}\n*Contact No.-* {phone} ")
        responder.slots['code'] =random.choice(["T1H2E","A1Z3T","E2C1S"])
        responder.prompt("You can also book the hotel. \nUse this code '{code}' to start the booking process.")
        responder.listen()

    except:
        if int(hotel_info['errors'][0]['status']) == CITY_NOT_FOUND_CODE:
            reply = "Sorry, I wasn't able to recognize that city."
            responder.reply(reply)
        elif int(hotel_info['errors'][0]['status']) == INVALID_API_KEY_CODE:
            reply = "Sorry, the API key is invalid."
            responder.reply(reply)
    


# Helpers

def _construct_search_hotel_api_url(selected_city):
    url_string = "{base_string}?cityCode={location}".format(base_string=HOTEL_BASE_STRING, location=selected_city.replace(" ", "+"))
    return url_string




