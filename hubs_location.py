import numpy as np
from .root import app

SIZE = 80
def extract_entities_from_type(request, entity_type):
    return [e for e in request.entities if e['type'] == entity_type]


@app.handle(intent='get_hubs_location')
def get_hub_loca(request, responder):
   
    action_entities = [e['value'][0]['cname']
                       for e in request.entities
                       if e['type'] == 'hub_action']

    qa, size = _resolve_categorical_entities(request, responder)

    if action_entities:
        if action_entities[0] == 'fired':
            
            qa = qa.filter(field='state', gt='Goa')

    qa_out = qa.execute(size=size)
    responder.slots['hubs_list'] = _get_names(qa_out)

    if len(qa_out) == 0 or len([e for e in request.entities]) == 0:
        replies = ["Sorry! No wellness hub found in this state. "
                   "'Please look for the wellness hubs in other states'."]
        responder.reply(replies)
        return

    if action_entities:
        responder.slots['action'] = action_entities[0]

        if qa_out and len(qa_out) == 1:
            responder.reply("The {action} wellness hub based on your criteria is: {hubs_list}")
        else:
            responder.reply("The {action} wellness hubs based on your criteria are: {hubs_list}")

    else:
        if qa_out and len(qa_out) == 1:
            responder.reply("This is the wellness hub you are looking for: {hubs_list}")
        else:
            responder.reply("These are the wellness hubs you are looking for: {hubs_list}")


def _get_names(qa_out):
 

    names = [str(out['wellness_hub']) for out in qa_out]
    names = ', '.join(names)
    return names

def _resolve_categorical_entities(request, responder):

    categorical_entities = [e for e in request.entities if e['type'] in
                            ('state')]

    qa = app.question_answerer.build_search(index='w_hubs')

    if categorical_entities:
        try:
            for categorical_entity in categorical_entities:
                key = categorical_entity['type']

                if key == 'Wellness_hub_location':
                    key = 'state'

                val = categorical_entity['value'][0]['cname']
                kw = {key: val}
                qa = qa.filter(**kw)
        except KeyError:
            pass

    return qa, SIZE
