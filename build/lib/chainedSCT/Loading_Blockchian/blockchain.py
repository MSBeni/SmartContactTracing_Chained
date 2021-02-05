# Module One Create Blockchain
# Needed to be installed: pip install Flask==0.12.2
# Postman HTTP client on the website https://getpostman.com
import datetime
import hashlib
import json
from urllib.parse import urlparse
import requests
from .node import Node
from ..authentication.authentication_IUP import IUP


# Building a Blockchain
class Blockchain:
    def __init__(self):
        self.chain = []
        # This is a list which keep the list of all transactions waiting to be added to the blockchain
        self.transactions = list()
        self.create_block(proof=1, previous_hash='0')
        self.nodes = set()

    def create_block(self, proof, previous_hash):
        """
        :param proof: the proof which is mined in order to signed the block
        :param previous_hash: the hash of the previously signed block
        :return: return the built block while adding it to the chain of the signed blocks
        """
        block = {'index': len(self.chain)+1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions': self.transactions}
        # After adding the transactions to the block we will make the transaction list empty
        self.transactions = []
        self.chain.append(block)
        return block

    def get_previous_block(self):
        """
        :return: return the previous block in the blockchain
        """
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        """
        :param previous_proof: the previous proof used to signed the previous block
        :return: return the new proof to sign the block --- brute force approach --- Proof of Work Consensus protocol
        """
        new_proof = 1
        mined_proof = False
        while mined_proof is False:
            calculated_hash = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if calculated_hash[:4] == '0000':
                mined_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash_calc(self, block_):
        """
        The hash function to return the hash of a block
        :param block_: the block we ought to get hashed
        :return: the SHA256 hashed format of the block
        """
        block_encoded = json.dumps(block_, sort_keys=True).encode()
        return hashlib.sha256(block_encoded).hexdigest()

    def is_chain_valid(self, chain_):
        """
        The function to check whether a blockchain whole blocks are valid and mined correctly. This section check has
        two main steps: 1- check if the hash of the previous block is equal to the previous hash in current block and
        2- checking whether all the blocks are mined correctly, this mean that in all of them the current block proof
         minus the previous one has a hashed value which meet the '0000' condition
        :param chain_: the whole blockchain
        :return: True if the chain is correct and False if it has any problem
        """
        previous_block = chain_[0]
        block_current_idx = 1
        while block_current_idx < len(chain_):
            # check if the hash of the previous block is equal to the previous hash in current block
            current_block = chain_[block_current_idx]
            if current_block['previous_hash'] != self.hash_calc(previous_block):
                return False
            # checking whether all the blocks are mined correctly, and their proof check meet the '0000' condition
            proof_hash = hashlib.sha256(str(current_block['proof']**2 - previous_block['proof']**2).encode()).\
                hexdigest()
            if proof_hash[:4] != '0000':
                return False
            previous_block = current_block
            block_current_idx += 1
        return True

    def add_transaction(self, sender, receiver, contacts):
        """
        The function to add the new transaction to the transaction list
        :param contacts:
        :param sender: the node sending a trace
        :param receiver: the node receiving a trace
        :param trace: the trace of the proximity which is sent from one node to another
        :return: the index of the block which the tranaaction is added to
        """
        self.transactions.append({
            'sender': sender,
            'receiver': receiver,
            'contacts': contacts
        })
        return self.get_previous_block()['index'] + 1

    def add_node(self, address):
        """
        Adding the nodes to the blockchain
        :param address: the URL address of the node e.g., http://127.0.0.1:5000/
        :return: updated set of nodes, added the node url e.g., '127.0.0.1:5000'
        """
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self):
        """
        Check wether there is a longest chain in our nodes version and replace it
        :return: the validity of the existence of a longer chain and consequent replacement
        """
        current_network = self.nodes
        LongestChain = None
        LenMaxCHAIN = len(self.chain)
        for node in current_network:
            rep = requests.get(f'http://{node}/get_chain')
            # print(rep)
            if rep.status_code == 200:
                _Len_ = rep.json()['length']
                _Chain_ = rep.json()['chain']
                if _Len_ > LenMaxCHAIN and self.is_chain_valid(_Chain_):
                    LenMaxCHAIN = _Len_
                    LongestChain = _Chain_
        if LongestChain:
            self.chain = LongestChain
            return True
        return False

    def mining_nodes_input_transactions(self):
        """
        Check whether there is a longest chain in our nodes version and replace it
        :return: the validity of the existence of a longer chain and consequent replacement
        """
        current_network = self.nodes
        for node in current_network:
            rep = requests.get(f'http://{node}/get_local_ledger')
            if rep.status_code == 200:
                for transaction in rep.json()['chain']:
                    if transaction not in self.transactions:
                        self.transactions.append(transaction)

    def mining_infected_nodes_input_transactions(self):
        """
        Check whether there is a longest chain in our nodes version and replace it
        :return: the validity of the existence of a longer chain and consequent replacement
        """
        current_network = self.nodes
        infected_users_ID = IUP.fetch_iup_ids()
        for node in current_network:
            node_id = Node.load_id_from_db_by_port(node[-4:])
            if (node_id in infected_users_ID) or (node_id in self.last_block_of_infected_nodes_contact_transactions()):
                rep = requests.get(f'http://{node}/get_local_ledger')
                if rep.status_code == 200:
                    for transaction in rep.json()['chain']:
                        if transaction not in self.transactions:
                            self.transactions.append(transaction)

    def last_block_of_infected_nodes_contact_transactions(self):
        """
        Check which nodes are published as a infected nodes and send alert and add Request Transaction
        :return: list of the contact ids who are infected based on the published transactions
        """
        all_announced_infected_ids = list()
        latest_mined_block = self.chain[-1:][0]
        for transaction in latest_mined_block['transactions']:
            all_announced_infected_ids.extend(transaction['contacts'])

        all_announced_infected_ids = list(set(all_announced_infected_ids))

        return all_announced_infected_ids


