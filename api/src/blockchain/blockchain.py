from .block import Block
from .donation import Donation

class DonationBlockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]  # Initialize the chain with the genesis block
    
    def create_genesis_block(self):
        data = {
            'name': "Genesis Block Transaction",
            "amount": 0,
            "sender": "0",
            "recipient": "0",
            "description": "The first block in the blockchain",
            "transaction_id": "0"
        }
        genesis_block = Block(0, data, '0')
        genesis_block.hash = genesis_block._create_hash()  # Ensure the hash is computed
        return genesis_block
    
    def get_last_block(self):
        return self.chain[-1]
    
    def add_donation(self, donation: Donation):
        previous_block = self.get_last_block()
        new_block = Block(
            index=previous_block.index + 1,
            data=donation,
            previous_hash=previous_block.hash
        )
        self.chain.append(new_block)
    
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
    
            if current_block.hash != current_block._create_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True
