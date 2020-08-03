import os
from .root import app
from mindmeld.core import FormEntity

personal_detail_form = {
    "entities": [
        FormEntity(
            entity="name",
            responses=["Please tell the name of the person booking."],
        ),
        FormEntity(
            entity="gender",
            responses=["Please specify the gender."],
            retry_response=["That gender is not correct. Please enter the gender like this 'Male' or 'Female'."],
        ),
        FormEntity(
            entity="sys_number",
            responses=["Please specify the age."],
            retry_response=[
                "That number is not correct. "
                "Please try formatting the value like this '22'."
            ],
        ),
        FormEntity(
            entity="sys_phone-number",
            responses=["Please give your phone no."],
            retry_response=[
                "That number is not correct. "
                "Please try formatting the value like this '2222255555'."
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

@app.auto_fill(intent='book', form=personal_detail_form)
def book(request, responder):
    for entity in request.entities:
        if entity["type"] == "name":
            responder.slots['name'] = (
            entity["value"][0]["cname"]
            if len(entity["value"]) > 0
            else entity["text"]
            )
        elif entity["type"] == "gender":
            responder.slots['gender'] = (
            entity["value"][0]["cname"]
            if len(entity["value"]) > 0
            else entity["text"]
            )
        elif entity["type"] == "sys_number":
            responder.slots['age'] = (
            entity["value"][0]["value"]
            if len(entity["value"]) > 0
            else entity["text"]
            )   
        else:
            responder.slots['phone'] = (
            entity["value"][0]["value"]
            if len(entity["value"]) > 0
            else entity["text"]
            ) 
    responder.reply("The booking process has been initiated for the following personal detail:\nName: *{name}* \nGender: *{gender}* \nAge: *{age}* \nPhone no.: *{phone}*")   
             