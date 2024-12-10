import time

class Donation:
    def __init__(self, sender: str, amount: float, description: str):
        self.sender = sender
        self.amount = amount
        self.description = description
        self.timestamp = time.time()
    
    def __str__(self):
        return f"{self.sender}-{self.amount}-{self.description}"
    