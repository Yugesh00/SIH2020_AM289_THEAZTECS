import numpy as np
from .root import app


SIZE = 30
def extract_entities_from_type(request, entity_type):
    return [e for e in request.entities if e['type'] == entity_type]


@app.handle(intent='get_centers_location')
def get_centers_location(request, responder):
  
    action_entities = [e['value'][0]['cname']
                       for e in request.entities
                       if e['type'] == 'employment_action']

   
    qa, size = _resolve_categorical_entities(request, responder)

    if action_entities:
        if action_entities[0] == 'fired':
            qa = qa.filter(field='yc_state', gt='Goa')

    qa_out = qa.execute(size=size)
    responder.slots['centers_list'] = _get_names(qa_out)

    if len(qa_out) == 0 or len([e for e in request.entities]) == 0:
        replies = ["Sorry! No yoga center found in this state. "
                   "Please look for the yoga centers in other states."]
        responder.reply(replies)
        return

    if action_entities:
        responder.slots['action'] = action_entities[0]

        if qa_out and len(qa_out) == 1:
            responder.reply("The {action} employee based on your criteria is: {centers_list}")
        else:
            responder.reply("The {action} employees based on your criteria are: {centers_list}")

    else:
        if qa_out and len(qa_out) == 1:
            responder.reply("This is the yoga center you are looking for: {centers_list}")
        else:
            responder.reply("These are the yoga centers you are looking for: {centers_list}")


def _get_names(qa_out):
    """
    Get a List of Names from a QA Result
    param qa_out (list) Output of QA from a query
    """

    names = [str(out['yc_name']) for out in qa_out]
    names = ', '.join(names)
    return names

def _resolve_categorical_entities(request, responder):
    """
    This function retrieves all categorical entities as listed below and filters
    the knowledge base using these entities as filters. The final search object
    containing the shortlisted employee data is returned back to the calling function.
    """

    categorical_entities = [e for e in request.entities if e['type'] in
                            ('yc_state')]

    qa = app.question_answerer.build_search(index='yoga_centers')

    if categorical_entities:
        try:
            for categorical_entity in categorical_entities:
                key = categorical_entity['type']

                if key == 'Yoga_center_location':
                    key = 'yc_state'

                val = categorical_entity['value'][0]['cname']
                kw = {key: val}
                qa = qa.filter(**kw)
        except KeyError:
            pass

    return qa, SIZE
