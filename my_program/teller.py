
from account import Account
from transaction import Transaction 
from bank import Bank

from error import InvalidInputError


class Teller:

    """Caixa
    
    Incluí métodos para a execução de transações entre contas
    É vinculado a um banco, no qual as transações serão registradas
    """
    
    def __init__(self, bank: Bank) -> None:

        self.bank = bank


    def __transfer(self, value: float, source: Account, receiver: Account) -> None:

        """Função base para a realização de transferências"""

        if value < 0:
            raise InvalidInputError('o valor para a transferência deve ser positivo')
            
        if source == receiver:
            raise InvalidInputError('a conta de origem e a de destino devem ser diferentes')

        if source is None or receiver is None:
            raise InvalidInputError('a conta de origem e a de destino devem ser especificadas')

        source.balance -= value
        receiver.balance += value


    def __transfer_pix(self, value: float, source: Account, receiver: Account) -> None:
        
        if value > 5000:
            raise InvalidInputError('o valor para a transferência PIX não deve exceder R$ 5000,00')

        self.__transfer(value, source, receiver)

        
    def __transfer_ted(self, value: float, source: Account, receiver: Account) -> None:
        
        if value <= 5000:
            raise InvalidInputError('o valor para a transferência TED deve ser superior a R$ 5000,00')

        if value > 10000:
            raise InvalidInputError('o valor para a transferência TED não deve exceder R$ 10000,00')

        self.__transfer(value, source, receiver)


    def __transfer_doc(self, value: float, source: Account, receiver: Account) -> None:
        
        if value <= 10000:
            raise InvalidInputError('o valor para a transferência DOC deve ser superior a R$ 10000,00')

        self.__transfer(value, source, receiver)


    def execute_transaction(self, transaction: Transaction) -> None:

        if transaction.id in self.bank.transaction_history:
            raise InvalidInputError('já existe uma transação com o id {}'.format(transaction.id))

        transfer_params = {
            'source': transaction.source,
            'receiver': transaction.receiver,
            'value': transaction.value
        }

        if(transaction.type == 'PIX'):
            self.__transfer_pix(**transfer_params)
        elif(transaction.type == 'TED'):
            self.__transfer_ted(**transfer_params)
        elif(transaction.type == 'DOC'):
            self.__transfer_doc(**transfer_params)
        else:
            raise InvalidInputError('o tipo da transação é inválido')

        self.bank.transaction_history[transaction.id] = transaction


