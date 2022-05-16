from account import Account
from transaction import Transaction 
from bank import Bank

class Teller:
    
    def __init__(self, bank: Bank):

        self.bank = bank

    def __transfer(self, value: float, source: Account, receiver: Account):

        """Função base para a realização de transferências"""

        if value < 0:
            raise Exception('o valor para a transferência deve ser positivo')
            
        if source == receiver:
            raise Exception('a conta de origem e a de destino devem ser diferentes')

        if source is None or receiver is None:
            raise Exception('a conta de origem e a de destino devem ser especificadas')

        source.balance -= value
        receiver.balance += value

    def __transfer_pix(self, value: float, source: Account, receiver: Account):
        
        if value > 5000:
            raise Exception('o valor para a transferência PIX não deve exceder R$ 5000,00')

        self.__transfer(value, source, receiver)
        
    def __transfer_ted(self, value: float, source: Account, receiver: Account):
        
        if value <= 5000:
            raise Exception('o valor para a transferência TED deve ser superior a R$ 5000,00')

        if value > 10000:
            raise Exception('o valor para a transferência TED não deve exceder R$ 10000,00')

        self.__transfer(value, source, receiver)


    def __transfer_doc(self, value: float, source: Account, receiver: Account):
        
        if value <= 10000:
            raise Exception('o valor para a transferência DOC deve ser superior a R$ 10000,00')

        self.__transfer(value, source, receiver)

    def execute_transaction(self, transaction: Transaction):

        if transaction.id in self.bank.transaction_history:
            raise Exception('já existe uma transação com o id {}'.format(transaction.id))

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
            raise Exception('o tipo da transação é inválido')

        self.bank.transaction_history[transaction.id] = transaction
