import csv
from operacoes import deposito, saque, mostrar_extrato, cadastrar_usuario, cadastrar_conta


def show_menu_cc(cc):
    menu = '''

    [d] Depositar
    [s] Sacar
    [e] Extrato
    [cc] Cadastrar conta
    [q] Sair

    => '''

    saldo = cc['saldo']
    limite = 500
    extrato = cc['extrato']
    numero_saques = 0
    LIMITE_SAQUES = 3

    while True:
        opcao = input(menu)

        if opcao == 'd':
            saldo, extrato = deposito(saldo, extrato)
            atualizar_conta(cc['numero_conta'], cc['agencia'], cc['usuario'], saldo, extrato)
        elif opcao == 's':
            saldo, extrato, numero_saques = saque(saldo, extrato, numero_saques, limite, LIMITE_SAQUES)
            atualizar_conta(cc['numero_conta'], cc['agencia'], cc['usuario'], saldo, extrato)
        elif opcao == 'e':
            mostrar_extrato(extrato, saldo)
        elif opcao == 'cc':
            cadastrar_conta(cc['usuario'])
        elif opcao == 'q':
            break
        else:
            print('Operação inválida, por favor selevione novamente a operação desejada.')


def show_menu_non_cc(num_cpf):
    menu = '''

    [c] Cadastrar usuário
    [cc] Cadastrar conta
    [q] Sair

    => '''

    while True:
        opcao = input(menu)

        if opcao == 'c':
            cadastrar_usuario()
        elif opcao == 'cc':
            cadastrar_conta(num_cpf)
        elif opcao == 'q':
            break


def obter_dados_cc(num_cpf, num_cc):
    try:
        with open('./data/contas.csv', 'r') as file:
            reader = csv.reader(file)
            for linha in reader:
                if linha[0] == num_cc and linha[2] == num_cpf:
                    # print(f'Conta: {linha[0]}, Agência: {linha[1]}, Usuário: {linha[2]}, Saldo: {linha[3]}')
                    cc = {
                        'numero_conta': linha[0],
                        'agencia': linha[1],
                        'usuario': linha[2],
                        'saldo': float(linha[3]),
                        'extrato': linha[4]
                    }
                    return cc
    except FileNotFoundError:
        print('Arquivo de contas não encontrado.')


def atualizar_conta(num_cc, agencia, usuario, saldo, extrato):
    try:
        with open('./data/contas.csv', 'r') as file:
            reader = list(csv.reader(file))
        
        with open('./data/contas.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for linha in reader:
                if linha[0] == num_cc and linha[2] == usuario:
                    linha[3] = str(saldo)
                    linha[4] = extrato
                writer.writerow(linha)
    except FileNotFoundError:
        print('Arquivo de contas não encontrado.')


def main():
    print('Bem-vindo ao sistema bancário!')
    num_cpf = input('Digite seu cpf: ')
    num_cc = input('Digite sua conta: ')
    
    try:
        cc = obter_dados_cc(num_cpf, num_cc)
        show_menu_cc(cc)
    except Exception as e:
        print(f'Erro ao obter dados da conta')
        show_menu_non_cc(num_cpf)


main()