from sqlalchemy.orm import Session
from ..database.models import StoredDonationBlock, Donation
from .block import Block
from datetime import datetime


class DonationBlockchain:
    def __init__(self, db: Session):
        self.db = db
        self.chain = self.load_chain_from_db()
        
    def create_genesis_block(self):
        """Create and store the genesis block."""
        data = [
            Donation(
                sender="0",
                receiver="0",
                amount=0,
                description="The first block in the blockchain",
                name="Genesis Block Transaction",
                transaction_id="0",
            )
        ]

        genesis_block = Block(index=0, data=data, previous_hash="0" * 64)
        genesis_block.hash = genesis_block._create_hash()

        # Store the genesis block in the database
        db_block = StoredDonationBlock(
            index=genesis_block.index,
            timestamp=datetime.now(),
            previous_hash=genesis_block.previous_hash,
            hash=genesis_block.hash,
        )
        
        self.db.add(db_block)
        
        self.db.commit()
        
        print("GENESIS BLOCK CREATED")

        return genesis_block

    def load_chain_from_db(self):
        """Reconstruct the blockchain from the database."""
        stored_blocks = (
            self.db.query(StoredDonationBlock)
            .order_by(StoredDonationBlock.index)
            .all()
        )
        
        if not stored_blocks:
            return [self.create_genesis_block()]
        
        return [
            Block(
                index=block.index,
                data=[
                    Donation(
                        name=donation.name,
                        sender=donation.sender,
                        receiver=donation.receiver,
                        amount=donation.amount,
                        description=donation.description,
                        transaction_id=donation.transaction_id,
                    )
                    for donation in block.donations
                ],
                previous_hash=block.previous_hash,
            )
            for block in stored_blocks
        ]

    def add_block(self, data: list[Donation]):
        """Add a block to the blockchain."""
        
        
        print("Previous block", self.chain[-1].data)
        print("Previous block hash", self.chain[-1].hash)
        
        previous_block = self.chain[-1] if self.chain else None
        previous_hash = previous_block.hash if previous_block else "0" * 64

        # Create a new block
        new_block = Block(
            index=len(self.chain),
            data=data,
            previous_hash=previous_hash,
        )

        # Store the block in the database
        db_block = StoredDonationBlock(
            index=new_block.index,
            timestamp=datetime.now(),
            previous_hash=new_block.previous_hash,
            hash=new_block.hash,
        )
        self.db.add(db_block)
        self.db.commit()

        # Store each donation in the block
        for donation in data:
            db_donation = Donation(
                block_id=db_block.id,
                name=donation.name,
                amount=donation.amount,
                sender=donation.sender,
                receiver=donation.receiver,
                description=donation.description,
                transaction_id=donation.transaction_id,
            )
            self.db.add(db_donation)
        self.db.commit()

        # Append the new block to the in-memory chain
        self.chain.append(new_block)

    def is_chain_valid(self):
        """Validate the blockchain."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            print(f"Checking block with hash {current_block.hash}")
            print(f"Checking previous hash {current_block.previous_hash}")
            
            print("Previous block hash", previous_block.hash)
            

            if current_block.hash != current_block._create_hash():
                print(f"Block {current_block.index} hash is invalid")
                return False
            if current_block.previous_hash != previous_block.hash:
                print(f"Block {current_block.index} previous hash is invalid")
                return False
            
        return True
