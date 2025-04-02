from Usuario import Usuario
from Conta import Conta


def deposito(saldo, extrato):
    while True:
        valor_deposito = float(input('Informe o valor do deposito: '))

        if valor_deposito < 0:
            print('Valor inválido. Favor tente novamente.')
        else: 
            saldo += valor_deposito
            extrato += f'Depósito: R$ {valor_deposito:.2f}\\n'
            return saldo, extrato


def saque(saldo, extrato, numero_saques, limite, LIMITE_SAQUES):
    if numero_saques >= LIMITE_SAQUES:
        print('Número máximo de saques excedido.')
    else:
        valor_saque = float(input('Informe o valor do saque: '))

        if valor_saque > saldo:
            print('Saldo insuficiente.')
        elif valor_saque > limite:
            print('Valor acima do limite.')
        elif valor_saque < 0:
            print('Valor inválido.')
        else:
            saldo -= valor_saque
            extrato += f'Saque: R$ {valor_saque:.2f}\\n'
            numero_saques += 1
    
    return saldo, extrato, numero_saques


def mostrar_extrato(extrato, saldo):
    print('--- Extrato ---')
    extrato_formatado = extrato.replace('\\n', '\n')
    print(extrato_formatado + f'Saldo: R$ {saldo:.2f}')


def cadastrar_usuario():
    nome = input('Informe o nome: ')
    data_nascimento = input('Informe a data de nascimento: ')
    cpf = input('Informe o CPF: ')
    logradouro = input('Informe o logradouro: ')
    numero = input('Informe o número: ')
    bairro = input('Informe o bairro: ')
    cidade = input('Informe a cidade: ')
    uf = input('Informe a sigla do estado: ')

    usuario = Usuario(nome, data_nascimento, cpf, logradouro, numero, bairro, cidade, uf)
    print('Usuário cadastrado com sucesso!')

    return usuario.cpf


def cadastrar_conta(num_cpf):
    if num_cpf == None:
        print('Você precisa cadastrar um usuário antes de criar uma conta.')
        num_cpf = cadastrar_usuario()

    conta = Conta(num_cpf)
    print('Conta cadastrada com sucesso!')

    return conta.numero_conta