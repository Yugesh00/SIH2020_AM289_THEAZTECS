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
