
from typing import Generator

from error import InvalidInputError

import re


def read_entries(input_file_name: str) -> Generator[dict, None, None]:

    """Lê os registros de um arquivo

    os campos de cada registro devem ser separados por |
    o nome de cada campo deve ser especificado na primeira linha do arquivo
    a ordem dos campos deve corresponder à ordem dos dados 
    assim como os campos, os nomes devem ser separados por |
    """

    with open(input_file_name, 'r') as input_file: 

        row_names = [row_name.strip() for row_name in input_file.readline().split('|')]

        for input_line in input_file:
            
            split_line = input_line.split('|')

            if len(split_line) < len(row_names):
                continue
            
            named_fields = zip(row_names, split_line)
            entry = {row_name:data.strip() for row_name, data in named_fields}

            yield entry


def read_id(string: str, name: str = 'o valor') -> int:

    """Valida e processa uma string representando um id"""
     
    if re.match(r'^\d*[1-9]\d*$', string) is None:
        raise InvalidInputError('{} deve ser um número inteiro maior que zero'.format(name))

    return int(string)
    

def read_money(string: str, name: str = 'o valor') -> float:

    """Valida e processa uma string representando um valor monetário"""

    if re.match(r'^\d+(.\d{1,2})?$', string) is None:
        raise InvalidInputError('{} deve ser um número positivo com até duas casas decimais'.format(name))

    return float(string)


def read_cpf(string: str, name: str = 'o valor') -> float:

    """Valida uma string representando um cpf"""

    if re.match(r'^\d{3}.\d{3}.\d{3}-\d{2}$', string) is None:
        raise InvalidInputError('{} deve estar no formato DDD.DDD.DDD-DD'.format(name))

    return string


