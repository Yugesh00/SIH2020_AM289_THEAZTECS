import os
import requests
import json
from .root import app
from mindmeld.core import FormEntity
import random

class UnitNotFound(Exception):
    pass

CITY_NOT_FOUND_CODE = 201
INVALID_API_KEY_CODE = 201
DEFAULT_Source = 'NGP'
DEFAULT_Destination = 'NZM'

TRAIN_BASE_STRING = "http://indianrailapi.com/api/v2/TrainBetweenStation/apikey/bc9ae8a6bcf75dfe25a66aad3324c19d"

transfer_form = {
    "entities": [
        FormEntity(
            entity="destination",
            role="origin",
            responses=["Sure. From Which city?"],
            retry_response=["That city is not correct. Please enter a correct city."],
        ),
        FormEntity(
            entity="destination",
            role="dest",
            responses=["To which city?"],
            retry_response=["That city is not correct. Please enter a correct city."],
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
    " flight booking and searching for a hotel",
    "max_retries": 1,
}

@app.auto_fill(intent='search_train' ,form=transfer_form)
def search_train(request, responder):
    """
    When the user asks for weather, return the weather in that location or use San Francisco if no
      location is given.
    """
   

    try:
        for entity in request.entities:
            if entity["type"] == "destination":
                if entity["role"] == "origin":
                    selected_source = (
                        entity["value"][0]["cname"]
                        if len(entity["value"]) > 0
                        else entity["text"]
                    )
                elif entity["role"] == "dest":
                    selected_destination = (
                        entity["value"][0]["cname"]
                        if len(entity["value"]) > 0
                        else entity["text"]
                    )    
        url_string = _construct_search_train_api_url(selected_source, selected_destination)
        train_info = requests.get(url_string).json()
       
    except ConnectionError:
        reply = "Sorry, I was unable to connect to the book train API, please check your connection."
        responder.reply(reply)
        return
    except UnitNotFound:
        reply = "Sorry, I am not sure which unit you are asking for."
        responder.reply(reply)
        return

    try:
        responder.slots['selected_source'] = selected_source 
        responder.slots['selected_destination'] = selected_destination
        responder.slots['TrainName'] = train_info['Trains'][0]['TrainName']
        responder.slots['TrainNo'] = train_info['Trains'][0]['TrainNo']
        responder.slots['ArrivalTime'] = train_info['Trains'][0]['ArrivalTime']
        responder.slots['DepartureTime'] = train_info['Trains'][0]['DepartureTime']
        responder.slots['TrainType'] = train_info['Trains'][0]['TrainType']
        responder.reply("Found a {TrainType} train {TrainNo} {TrainName} from {selected_source} to {selected_destination} which will arrive at {DepartureTime} and reach the destination at {ArrivalTime}")
        responder.slots['code'] =random.choice(["T1H2E","A1Z3T","E2C1S"])
        responder.prompt("You can also book this train. \nUse this code '{code}' to start the booking process.")
        responder.listen()
       
  
    except:
        if int(train_info['ResponseCode']) == CITY_NOT_FOUND_CODE:
            reply = "Sorry, I wasn't able to recognize that city."
            responder.reply(reply)
        elif int(train_info['ResponseCode']) == INVALID_API_KEY_CODE:
            reply = "Sorry, the API key is invalid."
            responder.reply(reply)
    


# Helpers

def _construct_search_train_api_url(selected_source, selected_destination):
    url_string = "{base_string}/From/{location1}/To/{location2}".format(base_string=TRAIN_BASE_STRING, location1=selected_source.replace(" ", "+"), location2=selected_destination.replace(" ", "+"))
    return url_string



