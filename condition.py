from .root import app

def extract_entities_from_type(request, entity_type):
    return [e for e in request.entities if e['type'] == entity_type]


def _get_condition(request, responder, entity_type):
   

    name = request.frame.get('condition_name')
    
    try:
        name_ent = extract_entities_from_type(request, 'condition_name')
        name = name_ent[0]['value'][0]['cname']
    except IndexError:
        if not name:
            return responder

    if name:
        responder = _fetch_from_kb(responder, name, entity_type)
    return responder
@app.handle(intent='condition')
def condition(request, responder):

    responder = _get_condition(request, responder, 'pose')
    responder = _get_condition(request, responder, 'condition_name')


    try:
        responder.reply("For {condition_name} you can do yoga poses like {pose}")
    except KeyError:
        responder.reply('Currently, I am not able to find a yoga pose for this.')

def _fetch_from_kb(responder, name, entity_type):

    yogas = app.question_answerer.get(index='condition', condition_name=name)
    entity_option = yogas[0][entity_type]

    responder.slots['name'] = name
    responder.slots[entity_type] = entity_option
    return responder
