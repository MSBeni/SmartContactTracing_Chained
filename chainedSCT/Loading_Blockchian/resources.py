from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from ..extraction.user import User
from uuid import uuid4
from .node import Node
from .blockchain import Blockchain
from ..authentication.IUP_Definition import InfectedUsersPool
from ..transformation.proximity import Proximity
from ..authentication.authentication_IUP import AuthorizedUsers

# Create Blockchain
blockchain = Blockchain()

# Create an add address for the node 5000
node_address = str(uuid4()).replace('-', '')


class GetActiveUsers(Resource):
    @jwt_required()
    def get(self):
        users_ = User.fetch_data()
        return {'users': users_}, 200


class GetConnectedNodeIds(Resource):
    @jwt_required()
    def get(self):
        node_ids = Node.fetch_ids()
        return {'Node Ids': node_ids}, 200


class GetActiveNodes(Resource):
    def get(self):
        nodes_ = Node.fetch_nodes()
        return {'users': nodes_}, 200


class GetInfectedNodes(Resource):
    @jwt_required()
    def get(self):
        Infected_nodes_ = InfectedUsersPool.save_infected_user()
        return {'infected users': Infected_nodes_}, 200


class InfectedContacts:
    @staticmethod
    def infected_ids(user_id_):
        Infected_nodes_ = Proximity.fetch_ids_in_close_proximity(user_id_)

        unique_infected_Contact_List = []
        for el in Infected_nodes_:
            unique_infected_Contact_List.append(el[0])
        unique_infected_Contact_List = list(set(unique_infected_Contact_List))
        return unique_infected_Contact_List


class GetInfectedNodeContacts(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id',
                        type=str,
                        required=True,
                        help='This field cannot be empty')

    @jwt_required()
    def get(self):
        """
        This function return the contact list of an infected user
        :return:
        """
        node_id = NodeConnection.parser.parse_args()
        unique_inf_CT = InfectedContacts.infected_ids(node_id.id)
        return {'infected users': unique_inf_CT}, 200




class MineBlockchain(Resource):
    @jwt_required()
    def get(self):   # Mining a new block
        """
        the app route to mine the new block
        :return: json file of the mined block and the success http code 200
        """
        PreviousBlock = blockchain.get_previous_block()
        PreviousProof = PreviousBlock['proof']
        CurrentProof = blockchain.proof_of_work(PreviousProof)
        PreviousHash = blockchain.hash_calc(PreviousBlock)
        blockchain.add_transaction(sender=node_address, receiver='MSBeni', Contacts=[ ])
        CurrentBlock = blockchain.create_block(CurrentProof, PreviousHash)
        response = {'message': 'Congrats, You Mined this Block !!!...',
                    'index': CurrentBlock['index'],
                    'timestamp': CurrentBlock['timestamp'],
                    'proof': CurrentBlock['proof'],
                    'previous_hash': CurrentBlock['previous_hash'],
                    'transactions': CurrentBlock['transactions']}
        return response, 200


class GetChain(Resource):   # Getting the full blockchain
    def get(self):
        response = {'chain': blockchain.chain,
                    'length': len(blockchain.chain)}
        return response, 200


# Submission Transaction where the new connected node connect to all other nodes in the network
class NodeConnection(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id',
                        type=str,
                        required=True,
                        help='This field cannot be empty')

    def post(self):
        """
        Get the ID of the new connected node, check for the other connected nodes to the network, and make a connection
        between this new added node to all other nodes
        :return:
        """
        node_id = NodeConnection.parser.parse_args()
        itself = Node.load_port_from_db_by_ids(node_id['id'])
        active_nodes = Node.load_nodes_url_from_db()
        active_nodes.remove(itself)
        data = {'nodes': active_nodes}
        connected_nodes = data.get('nodes')
        if connected_nodes is None:
            return 'No Node is connected to the network', 400
        for address in connected_nodes:
            blockchain.add_node(address=address)
        response = {'message': 'All the nodes are now connected to the network. These nodes are:',
                    'total_nodes': list(blockchain.nodes)}
        return response, 201


class ChainValidity(Resource):    # Check the validity of the blockchain
    def get(self):
        if blockchain.is_chain_valid(blockchain.chain):
            response = {
                'message': "The Chain is VALID ...",
            }
        else:
            response = {
                'message': "WARNING ... The Chain is NOT VALID ...",
            }
        return response, 200


class TransactionTest(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id',
                        type=str,
                        required=True,
                        help='Sender of transaction should be known - This field cannot be empty')

    def get(self):
        data = AddTransaction.parser.parse_args()
        authorized_ID = AuthorizedUsers.fetch_authorized_id()
        unique_inf_CT = InfectedContacts.infected_ids(data.id)

        return {"transaction": [data.id, authorized_ID[0], unique_inf_CT]}



class AddTransaction(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id',
                        type=str,
                        required=True,
                        help='Sender of transaction should be known - This field cannot be empty')

    def post(self):
        data = AddTransaction.parser.parse_args()
        authorized_ID = AuthorizedUsers.fetch_authorized_id()
        trans_keys = ['sender', 'receiver', 'Contacts']
        if not all(key in data for key in trans_keys):
            return 'some elements of the transaction is missing', 400
        transaction_index = blockchain.add_transaction(data.id, data['receiver'], data['Contacts'])
        response = f'This transaction is confirmed to be added to block {transaction_index}'
        return {'message': response}, 201


class ReplaceLongChain(Resource):
    def get(self):
        is_longestChain_replaced = blockchain.replace_chain()
        if is_longestChain_replaced:
            response = {'message': 'There was another longest chain and it is replaced now',
                        'new_chain': blockchain.chain}
        else:
            response = {'message': 'We are good. Current chain is the longest one',
                        'current_chain': blockchain.chain}

        return response, 201








