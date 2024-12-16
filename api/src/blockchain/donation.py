import time

class Donation:
    def __init__(self, sender: str, receiver: str, amount: float, description: str, transaction_id: str):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.description = description
        self.timestamp = time.time()
        self.transaction_id = self.transaction_id
    
    def __str__(self):
        return f"{self.sender}-{self.amount}-{self.description}"
    