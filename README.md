# Teste Itaú

Pequeno programa que simula transações bancárias a partir de um arquivo de entrada

## Uso

O programa pode ser executado a partir do diretório raiz com o seguinte comando:

	python3 bank/main.py

É possível, também, especificar um arquivo de entrada alternativo:

	python3 bank/main.py bank/files/alt_input.txt
	
## Arquivo de entrada

O arquivo de entrada deve conter, em sua primeira linha, um cabeçalho com o nome dos campos de entrada separados por ` | `. Os dados dados devem ser separados por ` | ` e seguir a ordem definida no cabeçalho.

```
id_transferencia|valor_transferencia|tipo_transferencia|nome_emissor|agencia_emissor|conta_emissor|cpf_emissor|nome_receptor|agencia_receptor|conta_receptor|cpf_receptor

1|400|PIX|Ana|002|1335|112.113.114-15|Bruno|001|3333|123.123.123-13
``` 
```
Sua transferência foi realizada com sucesso!
Saldo do emissor: R$ -400.00
Saldo do receptor: R$ 400.00
```

Os dados devem apresentar o formato adequado:

```
id_transferencia|valor_transferencia|tipo_transferencia|nome_emissor|agencia_emissor|conta_emissor|cpf_emissor|nome_receptor|agencia_receptor|conta_receptor|cpf_receptor

1|500|PIX|Ana|-1|1234|123.123.123-12|Bruno|002|1335|112.113.114-15
1|500|PIX|Ana|001|1234|1231223-12|Bruno|002|1335|112.113.114-15
1|0.33333|PIX|Ana|001|1234|123.123.123-12|Bruno|002|1335|112.113.114-15
``` 
```
Sua transferência não foi completada pois o id da agência do emissor deve ser um número inteiro maior que zero 

Sua transferência não foi completada pois o cpf do emissor deve estar no formato DDD.DDD.DDD-DD

Sua transferência não foi completada pois o valor da transação deve ser um número positivo com até duas casas decimais

```

Seguindo esse formato, o arquivo de entrada pode apresentar algumas variações:
* A ordem dos campos pode ser alterada, contanto que ela seja obedecida no restante do arquivo
* Pode haver linhas que não apresentam a quantidade campos especificada no cabeçalho, as quais serão ignoradas
* Pode haver espaços entre os dados e os pipes ` | `

```
nome_emissor|agencia_emissor|conta_emissor|cpf_emissor|id_transferencia|valor_transferencia|tipo_transferencia|nome_receptor|agencia_receptor|conta_receptor|cpf_receptor

Lorem Ipsum
Ana|002|1335| 112.113.114-15 |1| 400  |PIX|Bruno|001|3333|123.123.123-13
foo|bar
Bruno|001|3333|123.123.123-13|2| 56.0|  PIX|Cleber| 3|5555|123.123.123-15

``` 
```
Sua transferência foi realizada com sucesso!
Saldo do emissor: R$ -400.00
Saldo do receptor: R$ 400.00

Sua transferência foi realizada com sucesso!
Saldo do emissor: R$ 344.00
Saldo do receptor: R$ 56.00
```
