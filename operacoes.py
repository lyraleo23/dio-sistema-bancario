from Clientes import PessoaFisica
from Contas import ContaCorrente
import re


def cadastrar_usuario():
    nome = input('Informe o nome: ')
    data_nascimento = input('Informe a data de nascimento: ')
    cpf = input('Informe o CPF: ')
    logradouro = input('Informe o logradouro: ')
    numero = input('Informe o número: ')
    bairro = input('Informe o bairro: ')
    cidade = input('Informe a cidade: ')
    uf = input('Informe a sigla do estado: ')
    contas = []

    print(cpf)
    cpf = re.sub(r'\D', '', cpf)
    cpf = PessoaFisica.verificar_cpf_unico(cpf)  # Pass the required second argument

    cliente = PessoaFisica(nome, data_nascimento, cpf, contas, logradouro, numero, bairro, cidade, uf)
    cliente.salvar_cliente()
    print('Usuário cadastrado com sucesso!')
    return cliente


def cadastrar_conta(cliente):
    print('=== Cadastro de Conta Corrente ===')
    print(cliente)
    num_cpf = cliente.cpf

    if num_cpf == None:
        print('Você precisa cadastrar um usuário antes de criar uma conta.')
        num_cpf = cadastrar_usuario()

    try:
        conta = ContaCorrente(num_cpf)
        conta.salvar_conta_corrente()
        print('Conta cadastrada com sucesso!')
        print(conta)
    except Exception as e:
        print(f'Erro ao cadastrar conta: {e}')
        conta = None

    return conta


def deposito(saldo, extrato):
    while True:
        valor_deposito = float(input('Informe o valor do deposito: '))

        if valor_deposito < 0:
            print('Valor inválido. Favor tente novamente.')
        else: 
            saldo += valor_deposito
            extrato += f'Depósito: R$ {valor_deposito:.2f}\\n'
            return saldo, extrato


def mostrar_extrato(conta):
    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")

