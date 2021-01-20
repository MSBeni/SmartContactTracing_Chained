from random import choice
from flask_classful import FlaskView, route
from flask_restful import Resource, reqparse

# we'll make a list to hold some quotes for our app
quotes = [
    "A noble spirit embiggens the smallest man! ~ Jebediah Springfield",
    "If there is a way to do it better... find it. ~ Thomas Edison",
    "No one knows what he can do till he tries. ~ Publilius Syrus"
]


class Node(FlaskView):

    def index(self, quotes):
        return "<br>".join(quotes)

    def get(self, id):
        id = int(id)
        if id < len(quotes) - 1:
            return quotes[id]
        else:
            return "Not Found", 404

    def random(self):
        return choice(quotes)

    @route('/')
    @route('/word_bacon/')  # <--- Adding route
    def random(self):
        return choice(quotes)