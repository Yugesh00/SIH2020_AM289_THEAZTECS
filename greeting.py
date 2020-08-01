from .root import app
import random
# @app.handle(intent='greet')
# def greet(request, responder):
#     responder.reply("Hi, I am Getfit "
#                     "Your personal yoga assistant ")

# @app.handle(intent='greet')
# def welcome(request, responder):
#     """
#     When the user starts a conversation, say hi and give some restaurant suggestions to explore.
#     """
#     try:
#         # Get user's name from session information in a request to personalize the greeting.
#         responder.slots['name'] = request.context['name']
#         prefix = 'Hello, {name}. '
#     except KeyError:
#         prefix = 'Hello. '

#     # Get suggestions for three restaurants from the knowledge base.
#     # Ideally, these should be selected using factors like popularity, proximity, etc.
#     yoga_pose = app.question_answerer.get(index='yoga_pose')
#     suggestions = ', '.join([r['pose_name'] for r in yoga_pose[0:5]])

#     # Build up the final natural language response and reply to the user.
#     responder.reply(prefix + 'I am Getfit your personal Yoga Assistant, You can ask me for yoga poses like '
#                     + suggestions)

@app.handle(intent="greet")
def greet(request, responder):
    responder.slots['name'] = "I'm GetFit"
    replies = [
        "Hi {name}, how can I help with your wellness ? You can ask about yoga poses like tadasana, lolasana, etc."
        "and ayurveedic medicines for various problems",
        "Hello {name}, as your Wellness assistant. You can do things "
        "like: ask for poses for your different problems.",
    ]
    responder.reply(replies)

@app.handle(intent='exit')
def exit(request, responder):
    replies = random.choice([
        "Stay hydrated.",
        "Take your vitamins.",
        "Do exercise and yoga daily"
    ])
    responder.reply('Have a healthy day ahead, bye!\nTip of the day: '+ replies)



