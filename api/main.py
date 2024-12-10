from fastapi import FastAPI

from src.blockchain.blockchain import DonationBlockchain
from src.blockchain.donation import Donation

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the Donation Blockchain API"}


@app.get("/test")
async def test():
    
    blockchain = DonationBlockchain()

    # Create a donation
    
    donation = Donation("ALICE", 100, "Donation 1")
    
    # Add the transaction to the blockchain
    blockchain.add_donation(donation)
    
    # Create another transaction
    
    donation2 = Donation("BOB", 50, "Donation 2")
    
    # Add the transaction to the blockchain
    
    blockchain.add_donation(donation2)
    
    # Print the blockchain
    
    for block in blockchain.chain:
        print(block.__dict__)
        
    print(blockchain.is_chain_valid())
    return {"message": "Test completed: " + "BLOCKCHAIN IS VALID" if str(blockchain.is_chain_valid()) else "BLOCKCHAIN IS INVALID"}