from .root import app

def extract_entities_from_type(request, entity_type):
    return [e for e in request.entities if e['type'] == entity_type]


def _get_category(request, responder, entity_type):
   

    name = request.frame.get('category')
    
    try:
        name_ent = extract_entities_from_type(request, 'category')
        name = name_ent[0]['value'][0]['cname']
    except IndexError:
        if not name:
            return responder

    if name:
        responder = _fetch_from_kb(responder, name, entity_type)
    return responder
@app.handle(intent='beginner')
def category(request, responder):

    responder = _get_category(request, responder, 'asanas')
    responder = _get_category(request, responder, 'category')


    try:
        responder.reply("For {category} you can perform {asanas} \n\n Which yoga asanas would you like to know about?")
    except KeyError:
        responder.reply('Currently, I am not able to find a yoga pose for this category.')

def _fetch_from_kb(responder, name, entity_type):

    asanas = app.question_answerer.get(index='category', category=name)
    entity_option = asanas[0][entity_type]

    responder.slots['name'] = name
    responder.slots[entity_type] = entity_option
    return responder