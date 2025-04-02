import csv
import os

class Conta:
    def __init__(self, cpf):
        self.numero_conta = self.novo_numero_conta()
        self.agencia = '0001'
        self.usuario = cpf
        self.saldo = 0
        self.extrato = ''

        self.salvar_conta()

    def novo_numero_conta(self):
        try:
            with open('contas.csv', 'r') as file:
                return sum(1 for _ in file)
        except FileNotFoundError:
            return 1

    def salvar_conta(self, arquivo='contas.csv'):
        conta_dados = [self.numero_conta, self.agencia, self.usuario, self.saldo, self.extrato]
        arquivo_existe = os.path.exists(arquivo)

        with open('contas.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not arquivo_existe:
                # Escreve o cabeçalho se o arquivo não existir
                writer.writerow(['Número da Conta', 'Agência', 'Usuário', 'Saldo', 'Extrato'])
            writer.writerow(conta_dados)
