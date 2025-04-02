import csv
import os
import re

class Usuario:
    def __init__(self, nome, data_nascimento, cpf, logradouro, numero, bairro, cidade, uf):
        try:
            cpf = re.sub(r'\D', '', cpf)  # Remove qualquer caractere que não seja número
            self.cpf = self.verificar_cpf(cpf)
        except ValueError as e:
            print('Não foi possível cadastrar o usuário: Usuário já cadastrado.')
            return
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.endereco = self.novo_endereco(logradouro, numero, bairro, cidade, uf)

        self.salvar_usuario()


    def verificar_cpf(self, cpf):
        arquivo = 'usuarios.csv'
        if os.path.exists(arquivo):
            with open(arquivo, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)  # Pula o cabeçalho
                for linha in reader:
                    if linha[2] == cpf:  # Verifica se o CPF já existe
                        raise ValueError("CPF já cadastrado.")
        return cpf


    def novo_endereco(self, logradouro, numero, bairro, cidade, uf):
        return f'{logradouro}, {numero} - {bairro} - {cidade}/{uf}'

    def salvar_usuario(self, arquivo='usuarios.csv'):
        usuario_dados = [self.nome, self.data_nascimento, self.cpf, self.endereco]
        arquivo_existe = os.path.exists(arquivo)

        with open(arquivo, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not arquivo_existe:
                # Escreve o cabeçalho se o arquivo não existir
                writer.writerow(['Nome', 'Data de Nascimento', 'CPF', 'Endereço'])
            writer.writerow(usuario_dados)

    def __str__(self):
        return f'Nome: {self.nome}, Data de Nascimento: {self.data_nascimento}, CPF: {self.cpf}, Endereço: {self.endereco}'
