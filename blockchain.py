import hashlib
import time
import json
from web3 import Web3


class Block:
    def __init__(self, index, previous_hash, transactions, timestamp=None):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions  # Now it's a list of structured transactions
        self.timestamp = timestamp or time.time()
        self.nonce = 0
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.compute_hash()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = 2
        self.pending_transactions = []  # This will store transactions waiting to be mined
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, "0", [], time.time())
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)

    def add_block(self):
        last_block = self.chain[-1]
        new_block = Block(len(self.chain), last_block.hash, self.pending_transactions)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.pending_transactions = []  # Clear the pending transactions after adding to the block

    def add_transaction(self, sender, receiver, amount, ticket_id):
        transaction = {
            'sender': sender,
            'receiver': receiver,
            'amount': amount,
            'ticket_id': ticket_id,
            'timestamp': time.time()
        }
        self.pending_transactions.append(transaction)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.compute_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True
# Initialize blockchain
my_blockchain = Blockchain()

# Add some structured transactions
my_blockchain.add_transaction("User1", "User2", 5, "TICKET123")
my_blockchain.add_transaction("User3", "User4", 10, "TICKET456")

# Mine a block with the transactions
my_blockchain.add_block()

# Check if the blockchain is valid
print("Blockchain is valid:", my_blockchain.is_chain_valid())

# Print out the blockchain details
for block in my_blockchain.chain:
    print(f"Block {block.index} has the following transactions:")
    for transaction in block.transactions:
        print(transaction)
    print(f"Hash: {block.hash}")
    print("-----------")

def connect_to_blockchain():
    infura_url = "HTTP://127.0.0.1:7545"  
    web3 = Web3(Web3.HTTPProvider(infura_url))
    
    if web3.is_connected():
        print("Connected to blockchain!")
    else:
        print("Failed to connect to blockchain.")
    
    return web3