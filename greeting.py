from .root import app
import random

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