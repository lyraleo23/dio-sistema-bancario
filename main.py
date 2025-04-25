import csv
from Clientes import PessoaFisica
from Contas import ContaCorrente, Saque, Deposito
from operacoes import cadastrar_usuario, cadastrar_conta, mostrar_extrato


def main():
    print('Bem-vindo ao sistema bancário!')
    num_cpf = input('Digite seu cpf: ')
    num_conta = input('Digite sua conta: ')
    
    try:
        cliente = buscar_cliente(num_cpf)
        print(f'cliente: {cliente}')
        conta = obter_dados_conta_corrente(cliente, num_conta)
        print(f'conta:\n{conta}')

        if conta != None:
            show_menu_cc(cliente, conta)
        else:
            print(f'Dados não encontrados.')
            show_menu_novo_cliente(cliente)
    except Exception as e:
        print(f'Erro ao obter dados da conta: {e}')
        print(f'Saldo: {conta.saldo}')
        show_menu_novo_cliente(cliente)


def show_menu_novo_cliente(cliente):
    menu = '''

    [c] Cadastrar usuário
    [cc] Cadastrar conta
    [q] Sair

    => '''

    while True:
        opcao = input(menu)

        if opcao == 'c':
            cliente = cadastrar_usuario()
        elif opcao == 'cc':
            conta = cadastrar_conta(cliente)
        elif opcao == 'q':
            break


def show_menu_cc(cliente, conta):
    menu = f'''
    cliente: {cliente.nome}
    conta: {conta.numero}

    [d] Depositar
    [s] Sacar
    [e] Extrato
    [cc] Cadastrar conta
    [q] Sair

    => '''

    numero_saques = 0

    while True:
        opcao = input(menu)

        if opcao == 'd':
            valor_deposito = float(input('Informe o valor do deposito: '))
            transacao = Deposito(valor_deposito)
            cliente.realizar_transacao(conta, transacao)
            conta.atualizar_conta_corrente()
        elif opcao == 's':
            valor_saque = float(input('Informe o valor do saque: '))
            transacao = Saque(valor_saque)
            cliente.realizar_transacao(conta, transacao)
            conta.atualizar_conta_corrente()
        elif opcao == 'e':
            print('extrato')
            mostrar_extrato(conta)
        elif opcao == 'cc':
            cadastrar_conta(cliente)
        elif opcao == 'q':
            break
        else:
            print('Operação inválida, por favor selevione novamente a operação desejada.')


def buscar_cliente(num_cpf):
    try:
        with open('./data/Clientes.csv', 'r') as file:
            reader = csv.reader(file)
            for linha in reader:
                if linha[2] == num_cpf:
                    print('Cliente encontrado')

                    nome = linha[0]
                    data_nascimento = linha[1]
                    cpf = linha[2]
                    endereco = linha[3]
                    contas = linha[4]
                    
                    cliente = PessoaFisica(nome, data_nascimento, cpf, contas, endereco)
                    return cliente
            return None
    except FileNotFoundError:
        print('Arquivo de clientes não encontrado.')
    except Exception as e:
        print(f'Erro ao buscar cliente: {e}')
    return None


def obter_dados_conta_corrente(cliente, num_conta):
    num_cpf = cliente.cpf
    print(f'num_cpf: {num_cpf}')
    print(f'procurando num_conta: {num_conta}')

    try:
        with open('./data/Contas.csv', 'r') as file:
            reader = csv.reader(file)
            for linha in reader:
                print(linha)
                print(linha[0] == num_conta and linha[2] == num_cpf)
                if linha[0] == num_conta and linha[2] == num_cpf:
                    numero_conta = linha[0]
                    agencia = linha[1]
                    cliente = linha[2]
                    saldo = float(linha[3])
                    historico = linha[4]
                    limite = linha[5]
                    limite_saques = linha[6]

                    conta = ContaCorrente(cliente, limite, limite_saques, saldo, numero_conta, agencia)
                    return conta
            return None
    except FileNotFoundError:
        print('Arquivo de contas não encontrado.')
    except Exception as e:
        print(e)
    return None


main()
