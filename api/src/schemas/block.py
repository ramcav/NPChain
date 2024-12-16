from pydantic import BaseModel
from datetime import datetime
from typing import List
from .donation import DonationResponse

# Output schema for blocks
class StoredDonationBlockResponse(BaseModel):
    index: int
    timestamp: datetime
    previous_hash: str
    hash: str
    data: List[DonationResponse]

    class Config:
        orm_mode = True
