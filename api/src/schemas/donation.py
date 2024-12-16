from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Input schema for creating donations
class DonationCreate(BaseModel):
    name: str
    amount: int
    sender: str
    receiver: str
    description: str
    transaction_id: str


# Output schema for returning donations
class DonationResponse(BaseModel):
    name: str
    amount: int
    sender: str
    receiver: str
    description: str
    transaction_id: str

    class Config:
        orm_mode = True