import argparse
import sys
import json
from .extraction.user import User
from .extraction.saved_users import UserDB
from .extraction.database import Database
from .extraction.location_Extraction import UsersDataExtraction
from .extraction.locations import Location
from .transformation.proximity_extraction import ProximityCALC
from .transformation.proximity import Proximity
from .Loading_Blockchian.resources import GetActiveUsers, MineBlockchain, GetChain, ChainValidity, NodeConnection, \
    AddTransaction, ReplaceLongChain, GetActiveNodes, GetConnectedNodeIds, GetInfectedNodes, GetInfectedNodeContacts
from .Loading_Blockchian.node import Node
from flask import Flask
from flask_restful import Api
from .authentication.authorized_users import UserCredentialCheck
from .authentication.security import authenticate, identity
from flask_jwt import JWT
from uuid import uuid4
import requests


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--numUsers', type=int, default=50, help="Number of users in the environment")
    parser.add_argument('--numDays', type=int, default=21, help="Number of days the test is conducted")
    parser.add_argument('--usersInDay', type=int, default=10, help="Number of active users in each day")
    parser.add_argument('--immediate', type=int, default=1, help="Distance where two users are considered immediate")
    parser.add_argument('--near', type=int, default=5, help="Distance where two users are considered near")
    parser.add_argument('--nodePort', type=int, default=5000, help="The ")


    return parser

def main(argv=None):
    """
    :desc: Entry point method
    """
    if argv is None:
        argv = sys.argv

    try:
        parser = create_parser()
        args = parser.parse_args(argv[1:])

        MY_PASS = json.loads(open('../../secretfiles.json', 'r').read())['web']['user_pw']
        Database.initialize(database='chainedSCT', user='i-sip_iot', password=MY_PASS, host='localhost')

        # user = User('patriciarobinson@gmail.com', 'Samantha', 'Gallegos', 66048763)
        # UserDB.users_submission(args)

        # print(args.numUsers)

        # User.fetch_data()
        # User.fetch_ids()

        # Load ids
        ids_lst = User.load_all_ids_from_db()
        # print("ids --->", ids_lst[0])

        # create user location
        # UsersDataExtraction.save_location_to_db(args)

        # return all location values
        # Location.fetch_loc_data()

        # ProximityCALC.prox_calc(args)
        # Proximity.fetch_proximity_data()

        # print(contact_dates[0])
        # print(set(contact_dates))

        # Create the Web App
        app = Flask(__name__)
        app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
        app.secret_key = 'msbeni'
        api = Api(app)
        jwt = JWT(app, authenticate, identity)

        api.add_resource(GetActiveUsers, '/users')
        api.add_resource(GetActiveNodes, '/nodes')
        api.add_resource(MineBlockchain, '/mine_block')
        api.add_resource(GetChain, '/get_chain')
        api.add_resource(ChainValidity, '/validity')
        api.add_resource(NodeConnection, '/connect_nodes')
        api.add_resource(AddTransaction, '/add_transaction')
        api.add_resource(ReplaceLongChain, '/replace_long_chain')
        api.add_resource(UserCredentialCheck, '/login')
        api.add_resource(GetConnectedNodeIds, '/ids')
        api.add_resource(GetInfectedNodes, '/infected_nodes')
        api.add_resource(GetInfectedNodeContacts, '/infected_contacts')


        if args.nodePort == 5000:
            Node.create_nodes_table()
        node_ = Node(ids_lst[0][args.nodePort-5000][0], args.nodePort, "http://127.0.0.1:")
        node_.save_to_db()
        print(Node.load_nodes_url_from_db())
        print(Node.fetch_nodes())




        app.run(host='0.0.0.0', port=args.nodePort)



    except KeyboardInterrupt:
        print('\n Please run command --> [getTweets --h] to receive help the commands you can search')

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))