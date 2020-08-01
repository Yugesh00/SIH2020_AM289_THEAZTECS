from .root import app
import random


@app.handle(intent='unsupported')
def unsupported(request, responder):
    query = random.choice(["How to perform Tadasana?", "Show me all yoga centers in Uttarakhand.",
                           "Which medicine can be used to treat Arthrities?",
                           "How is yoga different from stretching or other kinds of fitness?",
                           "How can I cure Indigestion",
                           "Benefits of Shirshasana",
                           "Yoga poses for fitness", "Show me the list of hubs in goa",
                           "Where can i get treatment for Diabetes?"])

    responder.slots['query'] = query
    responder.reply("Hmmm, I don't quite understand, you can ask me something like '{query}'")
    responder.listen()
