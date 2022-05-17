
from account import Account
from agency import Agency

from error import InvalidInputError

from typing import Optional


class Bank:
    
    """Banco

    Mantém um dicionário com o registro das agências adicionadas
    Incluí métodos para gerenciar agências e contas
    """
    
    def __init__(self) -> None:
        
        self.agencies = {}
        self.transaction_history = {}


    def agency_exists(self, agency_id: int) -> bool:

        """Verifica se a agência especificada pelo id existe"""

        return agency_id in self.agencies


    def add_agency(self, agency: Agency) -> None:

        """Adiciona uma agência ao banco"""
        
        if self.agency_exists(agency.id):
            raise InvalidInputError('uma agência com o id {} já existe'.format(agency.id))

        agency.bank = self
        self.agencies[agency.id] = agency


    def get_agency(self, agency_id: int) -> Optional[Agency]:

        """Recupera uma agência pelo id

        Caso ela não exista, retorna None
        """
        
        if self.agency_exists(agency_id):
            return self.agencies[agency_id]

        return None


    def account_exists(self, account_id: int, agency_id: int) -> bool:

        """Verifica se a conta especificada existe na agência especificada
        
        A conta e a agência são especificadas pelos seus respectivos ids
        """
        
        if not self.agency_exists(agency_id):
            return False

        return self.get_agency(agency_id).account_exists(account_id)


    def add_account(self, account: Account, agency_id: int) -> None:
        
        """Adiciona uma conta à agência especificada
        
        Caso a agência não exista, ela é criada
        """
        
        if not self.agency_exists(agency_id):
            self.add_agency(Agency(agency_id))

        agency = self.get_agency(agency_id)

        agency.add_account(account)


    def get_account(self, account_id: int, agency_id: int) -> Optional[Account]:
        
        if self.account_exists(account_id, agency_id):
            return self.get_agency(agency_id).get_account(account_id)

        return None


    def get_or_create_account(self, account_id: int, name: str, cpf: str, agency_id: int) -> Account:

        account = self.get_account(account_id, agency_id)
        
        if account is None:
            account = Account(account_id, name, cpf)
            self.add_account(account, agency_id)

        return account


