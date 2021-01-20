from flask_restful import Resource
from ..extraction.user import User


class Node(Resource):

    def get(self):
        users_ = User.fetch_data()
        return {'users': users_}, 200



