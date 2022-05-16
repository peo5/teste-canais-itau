class Account:

    def __init__(self, account_id: int, name: str, cpf: str):

        self.id = account_id
        self.name = name
        self.cpf = cpf
        self.agency = None 
        self.balance = 0.0


class Transaction:
    
    def __init__(self, transaction_id: int, transaction_type: str, 
        transaction_value: float, source: Account, receiver: Account):

        self.id = transaction_id
        self.type = transaction_type 
        self.value = transaction_value
        self.source = source
        self.receiver = receiver


class Agency:

    def __init__(self, agency_id: int):
        
        self.id = agency_id
        self.bank = None 
        self.accounts = {}

    def account_exists(self, account_id: int):
        
        return account_id in self.accounts

    def add_account(self, account: Account):

        if self.account_exists(account.id):
            raise Exception('uma conta com o id {} já existe'.format(account.id))
        
        account.agency = self
        self.accounts[account.id] = account

    def get_account(self, account_id: int):
        
        if self.account_exists(account_id):
            return self.accounts[account_id]

        return None


class Bank:
    
    def __init__(self):
        
        self.agencies = {}

    def agency_exists(self, agency_id: int):

        return agency_id in self.agencies

    def add_agency(self, agency: Agency):

        """Adiciona uma agência ao banco"""
        
        if self.agency_exists(agency.id):
            raise Exception('uma agência com o id {} já existe'.format(agency.id))

        agency.bank = self
        self.agencies[agency.id] = agency

    def get_agency(self, agency_id: int):
        
        if self.agency_exists(agency_id):
            return self.agencies[agency_id]

        return None

    def account_exists(self, account_id: int, agency_id: int):
        
        if not self.agency_exists(agency_id):
            return False

        return self.get_agency(agency_id).account_exists(account_id)

    def add_account(self, account: Account, agency_id: int):
        
        """Adiciona uma conta à agência especificada
            caso a agência não exista, ela é criada"""
        
        if not self.agency_exists(agency_id):
            self.add_agency(Agency(agency_id))

        agency = self.get_agency(agency_id)

        agency.add_account(account)

    def get_account(self, account_id: int, agency_id: int):
        
        if self.account_exists(account_id, agency_id):
            return self.get_agency(agency_id).get_account(account_id)

        return None

    def get_or_create_account(self, account_id: int, name: str, cpf: str, agency_id: int):

        account = self.get_account(account_id, agency_id)
        
        if account is None:
            account = Account(account_id, name, cpf)
            self.add_account(account, agency_id)

        return account


def transfer(value: float, source: Account, receiver: Account):

    """Função base para a realização de transferências"""

    if value < 0:
        raise Exception('o valor para a transferência deve ser positivo')
        
    if source == receiver:
        raise Exception('a conta de origem e a de destino devem ser diferentes')

    if source is None or receiver is None:
        raise Exception('a conta de origem e a de destino devem ser especificadas')

    source.balance -= value
    receiver.balance += value


def transfer_pix(value: float, source: Account, receiver: Account):
    
    if value > 5000:
        raise Exception('o valor para a transferência PIX não deve exceder R$ 5000,00')

    transfer(value, source, receiver)
        

def transfer_ted(value: float, source: Account, receiver: Account):
    
    if value <= 5000:
        raise Exception('o valor para a transferência TED deve ser superior a R$ 5000,00')

    if value > 10000:
        raise Exception('o valor para a transferência TED não deve exceder R$ 10000,00')

    transfer(value, source, receiver)


def transfer_doc(value: float, source: Account, receiver: Account):
    
    if value <= 10000:
        raise Exception('o valor para a transferência DOC deve ser superior a R$ 10000,00')

    transfer(value, source, receiver)


def read_entries(input_file_name: str): 

    """Lê os registros de um arquivo
        os campos de cada registro devem ser separados por |
        o nome de cada campo deve ser especificado na primeira linha do arquivo
        os nomes devem estar ordenados e separados por |
        """

    with open(input_file_name, 'r') as input_file: 

        row_names = [row_name.strip() for row_name in input_file.readline().split('|')]

        for input_line in input_file:
            
            if(input_line == '\n'):
                continue
            
            split_line = input_line.split('|')
            named_data = zip(row_names, split_line)
            data = {row_name:data.strip() for row_name, data in named_data}

            yield data


def execute_transaction(transaction: Transaction):

    transfer_params = {
        'source': transaction.source,
        'receiver': transaction.receiver,
        'value': transaction.value
    }

    if(transaction.type == 'PIX'):
        transfer_pix(**transfer_params)
    elif(transaction.type == 'TED'):
        transfer_ted(**transfer_params)
    elif(transaction.type == 'DOC'):
        transfer_doc(**transfer_params)
    else:
        raise Exception('o tipo da transação é inválido')


def process_transaction_entry(entry: dict, bank: Bank):

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
        'source': bank.get_or_create_account(**source_params),
        'receiver': bank.get_or_create_account(**receiver_params)
    }

    return Transaction(**transaction_params)


def execute_transaction_file(input_file_name, bank):

    for entry in read_entries(input_file_name):

        try:
            transaction = process_transaction_entry(entry, bank)
            execute_transaction(transaction)
        except Exception as error:
            print('não foi possível realizar a transação pois {}'.format(error)) 

        print('transação efetuada com sucesso!')
        print('saldo do emissor: {}'.format(transaction.source.balance))
        print('saldo do receptor: {}'.format(transaction.receiver.balance))


bank = Bank()
execute_transaction_file('my_program/entrada.txt', bank)
