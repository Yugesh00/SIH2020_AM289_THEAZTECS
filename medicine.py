from .root import app

def extract_entities_from_type(request, entity_type):
    return [e for e in request.entities if e['type'] == entity_type]


def _get_ayurvedic_medicine(request, responder, entity_type):
   
    name = request.frame.get('problem')
    

    try:
        name_ent = extract_entities_from_type(request, 'problem')
        name = name_ent[0]['value'][0]['cname']
    except IndexError:
        if not name:
            return responder

    if name:
        responder = _fetch_from_kb(responder, name, entity_type)
    return responder
    
@app.handle(intent='ayurvedic_medicine')
def ayurvedic_medicine(request, responder):
   
    responder = _get_ayurvedic_medicine(request, responder, 'problem')
    responder = _get_ayurvedic_medicine(request, responder, 'medicine')


    try:
        responder.reply("For *{problem}* you can take *{medicine}* \n You can also see ayurveda centers for different therapies")
    except KeyError:
        responder.reply("I\'m afraid, I can\'t suggest any medicine for this problem. \nKindly consult a doctor.")

def _fetch_from_kb(responder, name, entity_type):


    medicine = app.question_answerer.get(index='medicine', problem=name)
    entity_option = medicine[0][entity_type]

    responder.slots['name'] = name
    responder.slots[entity_type] = entity_option
    return responder