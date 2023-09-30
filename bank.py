from datetime import datetime, timedelta

class Account:
    def __init__(self, name, balance, password, bankCode, branckCode, accountNumber):
        self.name = name
        self.balance = int(balance)
        self.password = password
        self.bankCode = bankCode
        self.branckCode = branckCode
        self.accountNumber = accountNumber
        self.transactions = []  # Para o rastreio do historico de translacoes 


    def deposit(self, amountToDeposit, password):
        if password != self.password:
            print('Sorry, incorrect password')
            return None

        if amountToDeposit < 0:
            print('You cannot deposit a negative amount')
            return None

        if amountToDeposit > self.balance:
            print('You cannot transfer a negative amount')
        
        self.balance +=amountToDeposit
        self.transactions.append(f'Deposit:  +{amountToDeposit}')
        return self.balance
     
    def receiveTransfer(self, amount): #Conta em que ira receber a transferencia
        self.balance += amount
        self.transactions.append(f'Received transfer: +{amount}')

    def withdraw(self, amountToWithdraw, password):
        if password != self.password:
            print('Incorrect password for this account')
            return None

        if amountToWithdraw <= 0:
            print('You cannot withdraw a negative amount')
            return None

        if amountToWithdraw > self.balance:
            print('You cannot withdraw more than you have in your account')
            return None
        
        self.balance -= amountToWithdraw
        self.transactions.append(f'Withdrwal: -{amountToWithdraw}')
        return self.balance

    def transfer(self, amount, password, recipientAccount,tranferType, pixKey=None): #Funcao para transferencia 
        if password != self.password:
            print('Sorry, Incorrect password.')
            return None
        
        if amount <=0:
            print('You do not have a positive amount in your account')
            return None
        
        if amount > self.balance:
            print('You do not have sufficient balance for this transfer')
            return None
        
        if tranferType == "TED": #Transferencia TED 
            today = datetime.now() # verifica qual e o dia da semana 
            if today.weekday() <5: # se for antes de sexta 
                if today.hour <17: # se for antes das 17 horas 
                    fee = 0 # taxa
                    if self.bankCode != recipientAccount.bankCode:
                        fee = 10
                    self.balance -= (amount + fee)
                    recipientAccount.receiveTransfer(amount)
                    self.transactions.append(f'TED to {recipientAccount.name}: - {amount}')
                    return self.balance
                else:
                    print('TED transfer must be initiated before 17:00 hour')
            else:
                print('TED transfers are only available on business days (Monday to Friday)')

        elif tranferType == "DOC": #Transferencia DOC 
            now = datetime.now()
            endOfDay = datetime(now.year, now.month, now.day, 17,0)  #Verifica se eo fim do dia util
            if now > endOfDay:
                processingDate = now + timedelta(days=2)
            else:
                processingDate = now + timedelta(days=1)

            fee = 0 #sem taxa
            if self.bankCode != recipientAccount.bankCode:
                fee = 20 #taxa para outros bancos
        
            print(f'DOC transfer  of {amount} will be processed on {processingDate.strftime("%Y-%m_%d")}')
            print(f'Fee for DOC transfer: R${fee}')
            self.balance -= (amount + fee)
            recipientAccount.receiveTransfer(amount)
            self.transactions.append(f'DOC to {recipientAccount.name}: -{amount} (Fee: -{fee})')
            return self.balance
        
        elif tranferType == "PIX": #transferencia PIX
            if pixKey is None:
                print('PIX transfer requires a valid PIX key')
                return None
            
            fee = 0
            self.balance -= (amount + fee)
            recipientAccount.receiveTransfer(amount)
            self.transactions.append(f'PIX to {recipientAccount.name}: -{amount} (Fee: {fee})')
            return self.balance
        else:
            print('Invalid transfer type')


    def validPixkey(self, pixKey):
        if len(pixKey) >= 9:
            return True
        else:
            return False

    def getBalance(self, password):
        if password != self.password:
            print('Sorry, incorrect password')
            return None
        return self.balance

    def show(self):
        print(' Name:', self.name)
        print(' Balance:', self.balance)
        print(' Password:', self.password)
        print(' Code bank:', self.bankCode)#codigo do banco 
        print(' Account: ', self.accountNumber) #o numero da conta
        print(' Transaction:',self.transactions) #vai mostrar o historico de translacoes na conta
        print(' ')


   #exemplo de uso      
oAccount = Account('Joe Schmoe', 1000, 'magic','123','456', '789')
oAccount2 = Account('Mary Olsen', 500, 'm222', '123', '897', '234')
transfer =200
transferType = "PIX"
password = 'magic'
pix_key = 'valid_pix_key_here'
oAccount.transfer(transfer,password,oAccount2,'PIX', pix_key)
oAccount2.transfer(transfer,password,oAccount, 'TED')
oAccount.show()
oAccount.getBalance("magic")

oAccount2.show()
print(f'Balance of {oAccount.name}: {oAccount.balance}')
print(f'Balance of {oAccount2.name}: {oAccount2.balance}')
print(' ')
oAccount3 = Account('Joe Jonas', 10000, 'magi','1239','4568', '7896')
oAccount4 = Account('Mary mech', 5000, 'm2227', '1236', '8970', '2344')

oAccount3.show()
oAccount4.show()

transfer = 400
tranferType = 'DOC'
password = 'magi'
oAccount3.transfer(transfer,password,oAccount4,'DOC')

print(f'Balance of {oAccount4.name}: {oAccount4.balance}')
print(f'Balance of {oAccount3.name}: {oAccount3.balance}')
print('')
oAccount5 = Account('Jonas', 10000, 'mag','1239','4568', '7896')
oAccount6 = Account(' mech ', 5000, 'm2227', '1236', '8970', '2344')

oAccount3.show()
oAccount4.show()

transfer = 400
tranferType = 'TED'
password = 'mag'
oAccount5.transfer(transfer,password,oAccount6,'TED')

print(f'Balance of {oAccount6.name}: {oAccount6.balance}')
print(f'Balance of {oAccount5.name}: {oAccount5.balance}')