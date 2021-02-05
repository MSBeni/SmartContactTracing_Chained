from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from ..extraction.user import User
from uuid import uuid4
from .node import Node
from .blockchain import Blockchain
from ..authentication.IUP_Definition import InfectedUsersPool
from ..authentication.authentication_IUP import AuthorizedUsers
from ..authentication.infected_contacts import InfectedContacts


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
        authorized_ID = AuthorizedUsers.fetch_authorized_id()
        PreviousBlock = blockchain.get_previous_block()
        PreviousProof = PreviousBlock['proof']
        CurrentProof = blockchain.proof_of_work(PreviousProof)
        PreviousHash = blockchain.hash_calc(PreviousBlock)
        # Previously Announced Infected Contacts of the Covid Positive Users
        # All_Previously_Published_Contacts = blockchain.last_block_of_infected_nodes_contact_transactions()
        # Adding the transactions of the infected node who is verified in the IUP
        blockchain.mining_infected_nodes_input_transactions()
        blockchain.add_transaction(sender=authorized_ID[0], receiver=authorized_ID[0],
                                   contacts=['Mining Transaction: No Reward is Granted'])

        blockchain.cleaning_local_transaction_list()
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


class GetLocalLedger(Resource):   # Getting the local ledger of a node
    def get(self):
        response = {'chain': blockchain.transactions,
                    'length': len(blockchain.transactions)}
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


class TransactionCloseContacts(Resource):
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
        unique_inf_CT = InfectedContacts.infected_ids(data.id)
        if (authorized_ID[0] is None) or (data.id is None) or (unique_inf_CT is None):
            return 'some elements of the transaction is missing', 400

        transaction_index = blockchain.add_transaction(data.id, authorized_ID[0], unique_inf_CT)
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
        # Clear the transactions list of each node after each mining session
        blockchain.transactions = []
        return response, 201


# Send Alert function to probable infected users diagnosed from a mined transaction
class SendAlert(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('alert',
                        type=str,
                        required=True,
                        help='This field cannot be empty')

    @jwt_required()
    def post(self):
        """
        This function send an alert to the nodes who are probably infected by Covid-19
        :return:
        """
        Alert = SendAlert.parser.parse_args()
        unique_inf_CT = InfectedContacts.infected_ids(Alert)
        return {'infected users': unique_inf_CT}, 200




