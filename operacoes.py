def deposito(saldo, extrato):
    while True:
        valor_deposito = float(input('Informe o valor do deposito: '))

        if valor_deposito < 0:
            print('Valor inválido. Favor tente novamente.')
        else: 
            saldo += valor_deposito
            extrato += f'Depósito: R$ {valor_deposito:.2f}\n'
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
            extrato += f'Saque: R$ {valor_saque:.2f}\n'
            numero_saques += 1
    
    return saldo, extrato, numero_saques


def mostrar_extrato(extrato, saldo):
    print('--- Extrato ---')
    print(extrato + f'Saldo: R$ {saldo:.2f}')
