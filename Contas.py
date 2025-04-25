import os
import csv
from datetime import datetime
from abc import ABC, abstractclassmethod, abstractproperty

class Conta:
    def __init__(self, cliente, saldo=0, numero_conta=None, agencia='0001'):
        self._saldo = saldo
        if numero_conta == None:
            self._numero_conta = self.novo_numero_conta()
        else:
            self._numero_conta = numero_conta
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()

    def novo_numero_conta(self):
        try:
            with open('./data/Contas.csv', 'r') as file:
                return sum(1 for _ in file)
        except FileNotFoundError:
            return 1
        
    def salvar_conta(self, arquivo='./data/Contas.csv'):
        conta_dados = [self._numero_conta, self._agencia, self._cliente, self._saldo, self._historico]
        arquivo_existe = os.path.exists(arquivo)
        print(arquivo_existe)

        with open('./data/Contas.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not arquivo_existe:
                # Escreve o cabeçalho se o arquivo não existir
                writer.writerow(['Número da Conta', 'Agência', 'Cliente', 'Saldo', 'Extrato'])
            writer.writerow(conta_dados)

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero_conta

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        return True

    def __str__(self):
        return f"""\
            Agência:\t{self._agencia}
            C/C:\t\t{self._numero_conta}
            Titular:\t{self._cliente}
            Saldo:\t\t{self._saldo:.2f}
        """


class ContaCorrente(Conta):
    def __init__(self, num_cpf, limite=500, limite_saques=3, saldo=0, numero_conta=None, agencia='0001'):
        super().__init__(num_cpf, saldo, numero_conta, agencia)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico._transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = float(valor) > float(self.limite)
        excedeu_saques = float(numero_saques) >= float(self.limite_saques)

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        else:
            return super().sacar(valor)

        return False

    def salvar_conta_corrente(self, arquivo='./data/Contas.csv'):
        conta_dados = [self._numero_conta, self._agencia, self._cliente, self._saldo, self._historico, self.limite, self.limite_saques]
        arquivo_existe = os.path.exists(arquivo)
        print(arquivo_existe)

        with open('./data/Contas.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not arquivo_existe:
                # Escreve o cabeçalho se o arquivo não existir
                writer.writerow(['Número da Conta', 'Agência', 'Cliente', 'Saldo', 'Extrato', 'Limite', 'Limite Saques'])
            writer.writerow(conta_dados)

    def atualizar_conta_corrente(self, arquivo='./data/Contas.csv'):
        conta_dados = [self._numero_conta, self._agencia, self._cliente, self._saldo, self._historico, self.limite, self.limite_saques]

        try:
            with open('./data/Contas.csv', 'r') as file:
                reader = list(csv.reader(file))
            
            with open('./data/Contas.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                for linha in reader:
                    if linha[0] == conta_dados[0] and linha[2] == conta_dados[2]:
                        linha[3] = str(conta_dados[3])
                    writer.writerow(linha)
        except FileNotFoundError:
            print('Arquivo de contas não encontrado.')


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

