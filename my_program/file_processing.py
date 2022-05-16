def read_entries(input_file_name: str): 

    """Lê os registros de um arquivo
        os campos de cada registro devem ser separados por |
        o nome de cada campo deve ser especificado na primeira linha do arquivo
        a ordem dos campos deve corresponder à ordem dos dados 
        assim como os campos, os nomes devem ser separados por |
        """

    with open(input_file_name, 'r') as input_file: 

        row_names = [row_name.strip() for row_name in input_file.readline().split('|')]

        for input_line in input_file:
            
            if(input_line == '\n'):
                continue
            
            split_line = input_line.split('|')
            named_fields = zip(row_names, split_line)
            entry = {row_name:data.strip() for row_name, data in named_fields}

            yield entry

