class Account:

    def __init__(self, account_id: int, name: str, cpf: str):

        self.id = account_id
        self.name = name
        self.cpf = cpf
        self.agency = None 
        self.balance = 0.0


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


def read_data(input_file_name: str): 

    """Lê os dados de um arquivo de transações"""

    with open(input_file_name, 'r') as input_file: 

        row_names = [row_name.strip() for row_name in input_file.readline().split('|')]

        for input_line in input_file:
            
            if(input_line == '\n'):
                continue
            
            split_line = input_line.split('|')
            named_data = zip(row_names, split_line)
            data = {row_name:data.strip() for row_name, data in named_data}

            yield data

def process_transactions(input_file_name):

    bank = Bank()

    for data in read_data(input_file_name):

        transaction_id = int(data['id_transferencia'])
        transaction_type = data['tipo_transferencia'].strip()

        transaction_params = {
            'value': float(data['valor_transferencia'])
        }

        source_params = {
            'name': data['nome_emissor'].strip(),
            'account_id': int(data['conta_emissor']),
            'agency_id': int(data['agencia_emissor']),
            'cpf': data['cpf_emissor'].strip(),
        }

        receiver_params = {
            'name': data['nome_receptor'].strip(), 
            'agency_id': int(data['agencia_receptor']),
            'account_id': int(data['conta_receptor']),
            'cpf': data['cpf_receptor'].strip(),
        }

        # recupera as contas

        transaction_params['source'] = bank.get_or_create_account(**source_params)
        transaction_params['receiver'] = bank.get_or_create_account(**receiver_params)
        
        # processa a transação

        if(transaction_type == 'PIX'):
            transfer_pix(**transaction_params)
        elif(transaction_type == 'TED'):
            transfer_ted(**transaction_params)
        elif(transaction_type == 'DOC'):
            transfer_doc(**transaction_params)
        else:
            raise Exception('o tipo da transação é inválido')

        print('transação efetuada com sucesso!')
        print('saldo do emissor: {}'.format(transaction_params['source'].balance))
        print('saldo do receptor: {}'.format(transaction_params['receiver'].balance))


process_transactions('my_program/entrada.txt')
