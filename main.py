from operacoes import deposito, saque, mostrar_extrato

menu = '''

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> '''

saldo = 0
limite = 500
extrato = ''
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    opcao = input(menu)

    if opcao == 'd':
        saldo, extrato = deposito(saldo, extrato)
    elif opcao == 's':
        saldo, extrato, numero_saques = saque(saldo, extrato, numero_saques, limite, LIMITE_SAQUES)
    elif opcao == 'e':
        mostrar_extrato(extrato, saldo)
    elif opcao == 'q':
        break
    else:
        print('Operação inválida, por favor selevione novamente a operação desejada.')


