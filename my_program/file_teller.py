from transaction import Transaction
from bank import Bank
from teller import Teller

from file_processing import read_entries

class FileTeller(Teller):

    def process_transaction_entry(self, entry: dict):

        source_params = {
            'name': entry['nome_emissor'].strip(),
            'account_id': int(entry['conta_emissor']),
            'agency_id': int(entry['agencia_emissor']),
            'cpf': entry['cpf_emissor'].strip(),
        }

        receiver_params = {
            'name': entry['nome_receptor'].strip(), 
            'agency_id': int(entry['agencia_receptor']),
            'account_id': int(entry['conta_receptor']),
            'cpf': entry['cpf_receptor'].strip(),
        }

        transaction_params = {
            'transaction_id': int(entry['id_transferencia']),
            'transaction_type': entry['tipo_transferencia'].strip(),
            'transaction_value': float(entry['valor_transferencia']),
            'source': self.bank.get_or_create_account(**source_params),
            'receiver': self.bank.get_or_create_account(**receiver_params)
        }

        return Transaction(**transaction_params)

    def execute_transaction_file(self, input_file_name):

        for entry in read_entries(input_file_name):

            try:
                transaction = self.process_transaction_entry(entry)
                self.execute_transaction(transaction)
            except Exception as error:
                print('não foi possível realizar a transação pois {}'.format(error)) 

            print('transação efetuada com sucesso!')
            print('saldo do emissor: {}'.format(transaction.source.balance))
            print('saldo do receptor: {}'.format(transaction.receiver.balance))

