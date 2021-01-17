from flask import Flask, jsonify, request
from uuid import uuid4
import requests
from .blockchain import Blockchain

# Create the Web App
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Create an add address for the node 5000
node_address = str(uuid4()).replace('-', '')


class Node:

    # Create Blockchain
    blockchain = Blockchain()

    # Mining a new block
    @classmethod
    @app.route("/mine_block", methods=['GET'])
    def mine_block(cls, node_address):
        """
        the app route to mine the new block
        :return: json file of the mined block and the success http code 200
        """
        PreviousBlock = cls.blockchain.get_previous_block()
        PreviousProof = PreviousBlock['proof']
        CurrentProof = cls.blockchain.proof_of_work(PreviousProof)
        PreviousHash = cls.blockchain.hash_calc(PreviousBlock)
        cls.blockchain.add_transaction(sender=node_address, receiver='MSBeni', trace='immediate')
        CurrentBlock = cls.blockchain.create_block(CurrentProof, PreviousHash)
        response = {'message': 'Congrats, You Mined this Block !!!...',
                    'index': CurrentBlock['index'],
                    'timestamp': CurrentBlock['timestamp'],
                    'proof': CurrentBlock['proof'],
                    'previous_hash': CurrentBlock['previous_hash'],
                    'transactions': CurrentBlock['transactions']}
        return jsonify(response), 200

    # Getting the full blockchain
    @classmethod
    @app.route("/get_chain", methods=['GET'])
    def get_chain(cls):
        response = {'chain': cls.blockchain.chain,
                    'length': len(cls.blockchain.chain)}
        return jsonify(response), 200

    # Check the validity of the blockchain
    @classmethod
    @app.route("/validity", methods=['GET'])
    def is_chain_valid(cls):

        if cls.blockchain.is_chain_valid(cls.blockchain.chain):
            response = {
                'message': "The Chain is VALID ...",
            }
        else:
            response = {
                'message': "WARNING ... The Chain is NOT VALID ...",
            }
        return jsonify(response), 200

    # Added the transaction which is mined to the blockchain
    @classmethod
    @app.route("/add_transaction", methods=['POST'])
    def add_transaction(cls):
        _json_ = request.get_json()
        trans_keys = ['sender', 'receiver', 'trace']
        if not all(key in _json_ for key in trans_keys):
            return 'some elements of the transaction is missing', 400
        _index_ = cls.blockchain.add_transaction(_json_['sender'], _json_['receiver'], _json_['trace'])
        response = f'This transaction is confirmed to be added to block {_index_}'
        return jsonify(response), 201

    # Connecting all the nodes in the network
    @classmethod
    @app.route("/connect_nodes", methods=['POST'])
    def node_connection(cls):
        _json = request.get_json()
        connected_nodes = _json.get('nodes')
        if connected_nodes is None:
            return 'No Node is connected to the network', 400
        for address in connected_nodes:
            cls.blockchain.add_node(address=address)
        response = {'message': 'All the nodes are now connected to the network. These nodes are:',
                    'total_nodes': list(cls.blockchain.nodes)}
        return jsonify(response), 201

    # Check the longest chain and replace it if necessary
    @classmethod
    @app.route('/LongChain_replace', methods=['GET'])
    def replace_long_chain(cls):
        is_longestChain_replaced = cls.blockchain.replace_chain()
        if is_longestChain_replaced:
            response = {'message': 'There was another longest chain and it is replaced now',
                        'new_chain': cls.blockchain.chain}
        else:
            response = {'message': 'We are good. Current chain is the longest one',
                        'current_chain': cls.blockchain.chain}

        return jsonify(response), 201


# running the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

