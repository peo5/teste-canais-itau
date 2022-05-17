
from account import Account

from error import InvalidInputError

from typing import Optional


class Agency:

    def __init__(self, agency_id: int) -> None:
        
        self.id = agency_id
        self.bank = None 
        self.accounts = {}


    def account_exists(self, account_id: int) -> bool:
        
        return account_id in self.accounts


    def add_account(self, account: Account) -> None:

        if self.account_exists(account.id):
            raise InvalidInputError('uma conta com o id {} já existe'.format(account.id))
        
        account.agency = self
        self.accounts[account.id] = account


    def get_account(self, account_id: int) -> Optional[Account]:
        
        if self.account_exists(account_id):
            return self.accounts[account_id]

        return None


