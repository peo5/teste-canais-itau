
class Account:

    def __init__(self, account_id: int, name: str, cpf: str) -> None:

        self.id = account_id
        self.name = name
        self.cpf = cpf
        self.agency = None 
        self.balance = 0.0

