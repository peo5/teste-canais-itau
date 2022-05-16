from bank import Bank
from file_teller import FileTeller

bank = Bank()
teller = FileTeller(bank)
teller.execute_transaction_file('my_program/files/entrada.txt')

