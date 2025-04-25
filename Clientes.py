import os
import csv
import re
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Cliente:
    def __init__(self, endereco, contas=[]):
        self.endereco = endereco
        self.contas = contas

    def novo_endereco(self, logradouro, numero, bairro, cidade, uf):
        return f'{logradouro}, {numero} - {bairro} - {cidade}/{uf}'
    
    def salvar_cliente(self, arquivo='./data/Clientes.csv'):
        usuario_dados = [self.nome, self.data_nascimento, self.cpf, self.endereco, self.contas]
        arquivo_existe = os.path.exists(arquivo)

        with open(arquivo, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not arquivo_existe:
                # Escreve o cabeçalho se o arquivo não existir
                writer.writerow(['Nome', 'Data de Nascimento', 'CPF', 'Endereço', 'Contas'])
            writer.writerow(usuario_dados)

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def __str__(self):
        return f'Nome: {self.nome}, CPF: {self.cpf}, Endereço: {self.endereco}'


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, contas, *args, **kwargs):
        print('Iniciando usuário... ')
        if len(args) == 1 and isinstance(args[0], str):  # Caso tenha apenas o endereço completo
            self.endereco = args[0]
        elif len(args) == 5:  # Caso tenha logradouro, número, bairro, cidade e UF
            logradouro, numero, bairro, cidade, uf = args
            self.endereco = self.novo_endereco(logradouro, numero, bairro, cidade, uf)
        else:
            raise ValueError("Argumentos inválidos para inicialização do endereço.")

        super().__init__(self.endereco, contas)
        try:
            cpf = re.sub(r'\D', '', cpf)  # Remove qualquer caractere que não seja número
            self.cpf = cpf
        except ValueError as e:
            print('Não foi possível cadastrar o usuário: Usuário já cadastrado.')
            return
        self.nome = nome
        self.data_nascimento = data_nascimento


    def verificar_cpf_unico(cpf):
        arquivo = './data/Clientes.csv'
        if os.path.exists(arquivo):
            with open(arquivo, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)  # Pula o cabeçalho
                for linha in reader:
                    if linha[2] == cpf:  # Verifica se o CPF já existe
                        raise ValueError("CPF já cadastrado.")
        return cpf

