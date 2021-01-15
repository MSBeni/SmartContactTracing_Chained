from flask import Flask, jsonify, request
from uuid import uuid4
from .blockchain import Blockchain

# Create the Web App
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Create an add address for the node 5000
node_address = str(uuid4()).replace('-', '')

# Create Blockchain
blockchain = Blockchain()


# Mining a new block
@app.route("/mine_block", methods=['GET'])
def mine_block():
    """
    the app route to mine the new block
    :return: json file of the mined block and the success http code 200
    """
    PreviousBlock = blockchain.get_previous_block()
    PreviousProof = PreviousBlock['proof']
    CurrentProof = blockchain.proof_of_work(PreviousProof)
    PreviousHash = blockchain.hash_calc(PreviousBlock)
    blockchain.add_transaction(sender=node_address, receiver='Arash', trace='near')
    CurrentBlock = blockchain.create_block(CurrentProof, PreviousHash)
    response = {'message': 'Congrats, You Mined this Block !!!...',
                'index': CurrentBlock['index'],
                'timestamp': CurrentBlock['timestamp'],
                'proof': CurrentBlock['proof'],
                'previous_hash': CurrentBlock['previous_hash'],
                'transactions': CurrentBlock['transactions']}
    return jsonify(response), 200


# Getting the full blockchain
@app.route("/get_chain", methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200


# Check the validity of the blockchain
@app.route("/validity", methods=['GET'])
def is_chain_valid():

    if blockchain.is_chain_valid(blockchain.chain):
        response = {
            'message': "The Chain is VALID ...",
        }
    else:
        response = {
            'message': "WARNING ... The Chain is NOT VALID ...",
        }
    return jsonify(response), 200


# Added the transaction which is mined to the blockchain
@app.route("/add_transaction", methods=['POST'])
def add_transaction():
    _json_ = request.get_json()
    trans_keys = ['sender', 'receiver', 'amount']
    if not all(key in _json_ for key in trans_keys):
        return 'some elements of the transaction is missing', 400
    _index_ = blockchain.add_transaction(_json_['sender'], _json_['receiver'], _json_['amount'])
    response = f'This transaction is confirmed to be added to block {_index_}'
    return jsonify(response), 201


# Connecting all the nodes in the network
@app.route("/connect_nodes", methods=['POST'])
def node_connection():
    _json = request.get_json()
    connected_nodes = _json.get('nodes')
    if connected_nodes is None:
        return 'No Node is connected to the network', 400
    for address in connected_nodes:
        blockchain.add_node(address=address)
    response = {'message': 'All the nodes are now connected to the network. These nodes are:',
                'total_nodes': list(blockchain.nodes)}
    return jsonify(response), 201


# Check the longest chain and replace it if necessary
@app.route('/LongChain_replace', methods=['GET'])
def replace_long_chain():
    is_longestChain_replaced = blockchain.replace_chain()
    if is_longestChain_replaced:
        response = {'message': 'There was another longest chain and it is replaced now',
                    'new_chain': blockchain.chain}
    else:
        response = {'message': 'We are good. Current chain is the longest one',
                    'current_chain': blockchain.chain}

    return jsonify(response), 201


# running the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
