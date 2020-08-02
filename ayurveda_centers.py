from .root import app

def extract_entities_from_type(request, entity_type):
    return [e for e in request.entities if e['type'] == entity_type]


def _get_ayurvedic_centers(request, responder, entity_type):
   
    name = request.frame.get('therapy')
    try:
        name_ent = extract_entities_from_type(request, 'therapy')
        name = name_ent[0]['value'][0]['cname']
    except IndexError:
        if not name:
            return responder

    if name:
        responder = _fetch_from_kb(responder, name, entity_type)
    return responder
    
@app.handle(intent='ayurveda_centers')
def ayurvedic_centers(request, responder):
   
    responder = _get_ayurvedic_centers(request, responder, 'therapy')
    responder = _get_ayurvedic_centers(request, responder, 'hubs')

    try:
        responder.reply("For *{therapy}* you can visit {hubs}")
    except KeyError:
        responder.reply("I\'m afraid, I can\'t suggest any medicine for this problem. \nKindly consult a doctor.")

def _fetch_from_kb(responder, name, entity_type):


    therapies = app.question_answerer.get(index='ayurveda_centers', therapy=name)
    entity_option = therapies[0][entity_type]

    responder.slots['name'] = name
    responder.slots[entity_type] = entity_option
    return responder