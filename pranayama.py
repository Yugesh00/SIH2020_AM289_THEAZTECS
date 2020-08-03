import numpy as np
from .root import app

NOT_KNOW = "Looks like I need to study for this pranayama."

def extract_entities_from_type(request, entity_type):
    return [e for e in request.entities if e['type'] == entity_type]

@app.handle(intent='pranayama', has_entity='pranayama_type')
def get_pranayama_type(request, responder):
    responder = _get_pranayama(request, responder, 'pranayama_type')
    try:
        responder.reply("{name} is {pranayama_type} type of Pranayama.\n\n You may also ask for 'Steps for {name}' or 'Timing for performing {name}'")
    except KeyError:
        responder.reply(NOT_KNOW)
    return


@app.handle(intent='pranayama', has_entity='pranayama_steps')
def get_pranayama_steps(request, responder):
    responder = _get_pranayama(request, responder, 'pranayama_steps')
    try:
        responder.reply("Steps to follow {name} are as follows: \n {pranayama_steps}.\n\nYou can also ask me about 'Type of {name}'")
    except KeyError:
        responder.reply(NOT_KNOW)
        return


@app.handle(intent='pranayama', has_entity='pranayama_timing')
def get_pranayama_timing(request, responder):
    responder = _get_pranayama(request, responder, 'pranayama_timing')
    try:
        responder.reply("Timing for performing {name} is {pranayama_timing} \n\nYou can ask for 'Precautions of {name}' or Steps of peforming {name}'")
    except KeyError:
        responder.reply(NOT_KNOW)
        return

@app.handle(intent='pranayama', has_entity='pranayama_precautions')
def get_pranayama_precautions(request, responder):
    responder = _get_pranayama(request, responder, 'pranayama_precautions')
    try:
        responder.reply("Precautions that should be taken while doing {name} are: \n{pranayama_precautions}\n\nYou can ask for 'Benefits of {name}'")
    except KeyError:
        responder.reply(NOT_KNOW)
        return

@app.handle(intent='pranayama', has_entity='pranayama_benefits')
def get_pranayama_benefits(request, responder):
    responder = _get_pranayama(request, responder, 'pranayama_benefits')
    try:
        responder.reply("Benefits of {name} are: \n{pranayama_benefits} \n\nYou can ask for 'Precautions of {name}'")
    except KeyError:
        responder.reply(NOT_KNOW)
    return

# Default case
@app.handle(intent='pranayama')
def get_pranayama_default(request, responder):

    try:
        name_ent = extract_entities_from_type(request, 'pranayama_name')
        name = name_ent[0]['value'][0]['cname']
        if name == '':
            responder.reply(NOT_KNOW)
            return

        responder.frame['name'] = name
        responder.frame['info_visited'] = True
        responder.slots['name'] = name
        responder.reply("What would you like to know about {name}?")
        responder.listen()

    except (KeyError, IndexError):
        if request.frame.get('info_visited'):
            name = request.frame.get('name')
            responder.slots['name'] = name
            center = app.question_answerer.get(index='pranayama', pranayama_name=name)
            if center:
                details = center[0]
                expand_dict = {'pranayama_type': 'Type of Pranayama', 'pranayama_steps': 'Steps for doing Pranayama',
                               'pranayama_timing': 'Timing of Pranayama', 'pranayama_precautions': 'Precautions while performing Pranayama',
                               'pranayama_benefits': 'Benefits of Pranayama'}
                details = [str(expand_dict[key]) + " : " + str(details[key])
                           for key in details.keys()
                           if key in expand_dict]
                responder.slots['details'] = '; '.join(details)
                responder.reply("I found the following details about {name}: {details}")
                responder.frame = {}

            else:
                replies = ["Hmmm, looks like I don't know about this Pranayama yet! "
                           "Would you like to know about some other Pranayama?"]
                responder.reply(replies)
                responder.frame = {}
        else:
            responder.reply("I believe, I need to know about this Pranayama.")
            responder.frame['info_visited'] = False



def _get_pranayama(request, responder, entity_type):

    name = request.frame.get('pranayama_name')
    try:
        name_ent = extract_entities_from_type(request, 'pranayama_name')
        name = name_ent[0]['value'][0]['cname']
    except IndexError:
        if not name:
            return responder

    if name:
        responder = _fetch_from_kb(responder, name, entity_type)
    return responder




def _fetch_from_kb(responder, name, entity_type):

    pranayama = app.question_answerer.get(index='pranayama', pranayama_name=name)
    entity_option = pranayama[0][entity_type]

    responder.slots['name'] = name
    responder.slots[entity_type] = entity_option
    return responder