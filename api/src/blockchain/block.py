import hashlib
from .donation import Donation

import time

class Block:
    def __init__(self, index: int, data: Donation, previous_hash=''):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self._create_hash()
        
    def _create_hash(self) -> str:
        # Convert all properties into a string and encode it
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{str(self.data)}".encode()
        # Return the hash of this string using SHA-256
        return hashlib.sha256(block_string).hexdigest()
        