from .root import app


@app.handle(intent='generic')
def generic(request, responder):
    responder.reply("Sure, what do you want to know?")
    responder.params.target_dialogue_state = 'all_topics'
    responder.listen()


@app.handle(intent='all_topics')
def all_topics(request, responder):
    query = request.text
    answers = app.question_answerer.get(index='faq', query_type='text', question=query,
                                        answer=query)
    if answers:
        reply = [answers[0]['answer']]
        responder.reply(reply)
    else:
        responder.reply("I'm sorry, I couldn't find an answer to your question")
from .root import app

def extract_entities_from_type(request, entity_type):
    return [e for e in request.entities if e['type'] == entity_type]

# 'Here is the top result:', answers[0]['question'], 
# def _get_question(request, responder, entity_type):
#     name = request.frame.get('question')
    
#     try:
#         name_ent = extract_entities_from_type(request, 'question')
#         name = name_ent[0]['value'][0]['cname']
#     except IndexError:
#         if not name:
#             return responder

#     if name:
#         responder = _fetch_from_kb(responder, name, entity_type)
#     return responder

# @app.handle(intent='all_topics')
# def topics(request, responder):

#     responder = _get_question(request, responder, 'answer')
#     responder = _get_question(request, responder, 'question')


#     try:
#         responder.reply("{answer} \n\nWhat else do you want to know?")
#     except KeyError:
#         responder.reply('Currently, I am not able to find a yoga pose for this.')

# def _fetch_from_kb(responder, name, entity_type):

#     questions = app.question_answerer.get(index='faq', question=name, query_type='text')
#     entity_option = questions[0][entity_type]

#     responder.slots['name'] = name
#     responder.slots[entity_type] = entity_option
#     return responder