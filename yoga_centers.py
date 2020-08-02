import numpy as np
from .root import app

NOT_KNOW = "Looks like I need to study for the yoga center."

def extract_entities_from_type(request, entity_type):
    return [e for e in request.entities if e['type'] == entity_type]


@app.handle(intent='yoga_centers', has_entity='yc_treatments')
def get_yc_treatments(request, responder):
    responder = _get_yoga_centers(request, responder, 'yc_treatments')
    try:
        responder.reply("{yc_treatments} \n\nYou can also ask for 'Details of {name}'")
    except KeyError:
        responder.reply(NOT_KNOW)
    return


@app.handle(intent='yoga_centers', has_entity='yc_location')
def get_yc_location(request, responder):
    responder = _get_yoga_centers(request, responder, 'yc_location')
    try:
        responder.reply("{name} is located at {yc_location}")
    except KeyError:
        responder.reply(NOT_KNOW)
        return


@app.handle(intent='yoga_centers', has_entity='yc_description')
def get_yc_description(request, responder):
    responder = _get_yoga_centers(request, responder, 'yc_description')
    try:
        responder.reply("{yc_description} \n\nYou can also ask for 'Treatments provided at {name}'")
    except KeyError:
        responder.reply(NOT_KNOW)
        return

@app.handle(intent='yoga_centers', has_entity='yc_link')
def get_yc_link(request, responder):
    responder = _get_yoga_centers(request, responder, 'yc_link')
    try:
        responder.reply("The link for {name} is {yc_link}")
    except KeyError:
        responder.reply(NOT_KNOW)
        return

# Default case
@app.handle(intent='yoga_centers')
def get_center_default(request, responder):

    try:
        name_ent = extract_entities_from_type(request, 'yc_name')
        name = name_ent[0]['value'][0]['cname']

        if name == '':
            responder.reply(NOT_KNOW)
            return

        responder.frame['name'] = name
        responder.frame['info_visited'] = True
        responder.slots['name'] = name
        responder.reply("What would you like to know about {name}?  \n\n You can ask 'Give details of {name}' or 'Where is {name} located' or 'What treatments will I get in {name}'")
        responder.listen()

    except (KeyError, IndexError):

        if request.frame.get('info_visited'):
            name = request.frame.get('name')
            responder.slots['name'] = name

            center = app.question_answerer.get(index='yoga_centers', yc_name=name)
            if center:
                details = center[0]

                expand_dict = {'yc_treatments': 'Treatments', 'yc_location': 'Yoga center location',
                               'yc_description': 'Description'}
                details = [str(expand_dict[key]) + " : " + str(details[key])
                           for key in details.keys()
                           if key in expand_dict]

                responder.slots['details'] = '; '.join(details)
                responder.reply("I found the following details about {name}: {details}")
                responder.frame = {}

            else:
                replies = ["Hmmm, looks like I don't know about this yoga center yet! "
                           "Would you like to know about some other yoga center?"]
                responder.reply(replies)
                responder.frame = {}
        else:
            responder.reply("I believe, I need to know about this yoga center.")
            responder.frame['info_visited'] = False



def _get_yoga_centers(request, responder, entity_type):

    name = request.frame.get('yc_name')

    try:
        name_ent = extract_entities_from_type(request, 'yc_name')
        name = name_ent[0]['value'][0]['cname']
    except IndexError:
        if not name:
            return responder

    if name:
        responder = _fetch_from_kb(responder, name, entity_type)
    return responder




def _fetch_from_kb(responder, name, entity_type):

    centers = app.question_answerer.get(index='yoga_centers', yc_name=name)
    entity_option = centers[0][entity_type]

    responder.slots['name'] = name
    responder.slots[entity_type] = entity_option
    return responder

