
from transaction import Transaction
from teller import Teller

from error import InvalidInputError

from file_processing import read_entries, read_id, read_money, read_cpf


class FileTeller(Teller):


    def process_transaction_entry(self, entry: dict) -> Transaction:

        source_params = {
            'name': entry['nome_emissor'],
            'account_id': read_id(entry['conta_emissor'], 'o id da conta do emissor'),
            'agency_id': read_id(entry['agencia_emissor'], 'o id da agência do emissor'),
            'cpf': read_cpf(entry['cpf_emissor'], 'o cpf do emissor'),
        }

        receiver_params = {
            'name': entry['nome_receptor'], 
            'agency_id': read_id(entry['agencia_receptor'], 'o id da conta do receptor'),
            'account_id': read_id(entry['conta_receptor'], 'o id da agência do receptor'),
            'cpf': read_cpf(entry['cpf_receptor'], 'o cpf do receptor'),
        }

        transaction_params = {
            'transaction_id': read_id(entry['id_transferencia']),
            'transaction_type': entry['tipo_transferencia'],
            'transaction_value': read_money(entry['valor_transferencia'], 'o valor da transação'),
            'source': self.bank.get_or_create_account(**source_params),
            'receiver': self.bank.get_or_create_account(**receiver_params)
        }

        return Transaction(**transaction_params)


    def execute_transaction_file(self, input_file_name) -> None:

        for entry in read_entries(input_file_name):

            try:

                transaction = self.process_transaction_entry(entry)
                self.execute_transaction(transaction)

                print('Sua transferência foi realizada com sucesso!')
                print('Saldo do emissor: R$ {:.2f}'.format(transaction.source.balance))
                print('Saldo do receptor: R$ {:.2f}'.format(transaction.receiver.balance))
                print()

            except InvalidInputError as error:

                print('Sua transferência não foi completada pois {}'.format(error)) 
                print()


