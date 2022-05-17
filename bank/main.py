
import sys
import os

from bank import Bank
from file_teller import FileTeller


if __name__ == '__main__':

    file_path = os.path.join(os.path.dirname(__file__), 'files/entrada.txt')

    if len(sys.argv) > 1:
        file_path = sys.argv[1]

    bank = Bank()
    teller = FileTeller(bank)
    teller.execute_transaction_file(file_path)


