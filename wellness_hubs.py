import numpy as np
from .root import app

NOT_KNOW = "Looks like I need to study for the wellness hub."
SIZE = 80
def extract_entities_from_type(request, entity_type):
    return [e for e in request.entities if e['type'] == entity_type]

@app.handle(intent='wellness_hubs', has_entity='packages')
def get_packages(request, responder):
    responder = _get_wellness_hub(request, responder, 'packages')
    try:
        responder.reply("Packages provided at {name} are {packages}  \n\n You can ask 'Give details of {name}' or 'Where is {name} located' ")
    except KeyError:
        responder.reply(NOT_KNOW)
    return


@app.handle(intent='wellness_hubs', has_entity='center_type')
def get_center_type(request, responder):
    responder = _get_wellness_hub(request, responder, 'center_type')
    try:
        responder.reply("It is a {center_type} \n\nYou can ask 'What packages are available at {name}' or 'Where is {name} located' ")
    except KeyError:
        responder.reply(NOT_KNOW)
        return


@app.handle(intent='wellness_hubs', has_entity='hub_description')
def get_hub_description(request, responder):
    responder = _get_wellness_hub(request, responder, 'hub_description')
    try:
        responder.reply("{hub_description}  \n\n You can ask 'What packages are available at {name}' or 'Where is {name} located' ")
    except KeyError:
        responder.reply(NOT_KNOW)
        return


@app.handle(intent='wellness_hubs', has_entity='place')
def get_place(request, responder):
    responder = _get_wellness_hub(request, responder, 'place')
    try:
        responder.reply("{name} located at {place}  \n\nIf you are planning for a tour here say 'flights' or 'trains'")
    except KeyError:
        responder.reply(NOT_KNOW)
        return

@app.handle(intent='wellness_hubs')
def get_info_hubs(request, responder):

    try:
        name_ent = extract_entities_from_type(request, 'wellness_hub')
        name = name_ent[0]['value'][0]['cname']

        if name == '':
            responder.reply(NOT_KNOW)
            return

        responder.frame['name'] = name
        responder.frame['info_visited'] = True
        responder.slots['name'] = name
        responder.reply("What would you like to know about {name}?    \n\n You can ask 'Give details of {name}' or 'Where is {name} located' or 'What packages are available at {name}'")
        responder.listen()

    except (KeyError, IndexError):
        if request.frame.get('info_visited'):
            name = request.frame.get('name')
            responder.slots['name'] = name
            hub = app.question_answerer.get(index='w_hubs', wellness_hub=name)
            if hub:
                details = hub[0]
                expand_dict = {'packages': 'packages', 'center_type': 'center_type',
                               'place': 'place', 'hub_description': 'description'}
                details = [str(expand_dict[key]) + " : " + str(details[key])
                           for key in details.keys()
                           if key in expand_dict]
                responder.slots['details'] = '; '.join(details)
                responder.reply("I found the following details about {name}: {details}")
                responder.frame = {}

            else:
                replies = ["Hmmm, looks like I don't know about this wellness hub yet! "
                           "Would you like to know about some other wellness hub?"]
                responder.reply(replies)
                responder.frame = {}
        else:
            responder.reply("I believe, I need to study regarding this wellness hub.")
            responder.frame['info_visited'] = False



def _get_wellness_hub(request, responder, entity_type):


    name = request.frame.get('wellness_hub')
    try:
        name_ent = extract_entities_from_type(request, 'wellness_hub')
        name = name_ent[0]['value'][0]['cname']
    except IndexError:
        if not name:
            return responder
    if name:
        responder = _fetch_from_kb(responder, name, entity_type)
    return responder




def _fetch_from_kb(responder, name, entity_type):

    wellness = app.question_answerer.get(index='w_hubs', wellness_hub=name)
    entity_option = wellness[0][entity_type]

    responder.slots['name'] = name
    responder.slots[entity_type] = entity_option
    return responder