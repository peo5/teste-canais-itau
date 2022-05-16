
from account import Account


class Transaction:
    
    def __init__(self, transaction_id: int, transaction_type: str, 
        transaction_value: float, source: Account, receiver: Account) -> None:

        self.id = transaction_id
        self.type = transaction_type 
        self.value = transaction_value
        self.source = source
        self.receiver = receiver


