from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .config import Base

class StoredDonationBlock(Base):
    __tablename__ = "stored_donation_blocks"

    id = Column(Integer, primary_key=True, index=True)
    index = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    previous_hash = Column(String, nullable=False)
    hash = Column(String, nullable=False)

    # One-to-many relationship with Donation
    donations = relationship("Donation", back_populates="block")

class Donation(Base):
    __tablename__ = "donations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    sender = Column(String, nullable=False)
    receiver = Column(String, nullable=False)
    description = Column(String, nullable=False)
    transaction_id = Column(String, nullable=False)
    block_id = Column(Integer, ForeignKey("stored_donation_blocks.id"))

    # Back-populate relationship with StoredDonationBlock
    block = relationship("StoredDonationBlock", back_populates="donations")
