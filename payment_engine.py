import models,enums

    
def sendPayment(sender: models.Wallet, receiver: models.Wallet, amount):
    
    request = models.Request(sender,receiver,amount)
    
    validationResult = validateRequest(request)
    
    if validationResult.valid:
        transferFunds(request)
        
        transaction = createCompletedTransactionLog(request)
        
        saveTransaction(transaction)
        
        returnResult(transaction)
        
    else:
        return validationResult.error

def validateRequest(request: models.Request):
    
    if request.sender.wallet_id == request.receiver.wallet_id: 
        return models.ValidationResult(enums.TransactionErrors.FAILED)
    
    elif request.sender.owner.status != enums.UserStatus.ACTIVE or request.receiver.owner.status != enums.UserStatus.ACTIVE:
        return models.ValidationResult(enums.TransactionErrors.USER_NOT_ACTIVE)
    
    elif request.sender.status != enums.WalletStatus.ACTIVE or request.receiver.status != enums.WalletStatus.ACTIVE:
        return models.ValidationResult(enums.TransactionErrors.WALLET_NOT_ACTIVE)
    
    elif request.sender.currency != request.receiver.currency:
        return models.ValidationResult(enums.TransactionErrors.WALLET_CURRENCY)
    
    elif request.sender.balance < request.amount:
        return models.ValidationResult(enums.TransactionErrors.FUNDS)
    
    else:
        return models.ValidationResult()

def transferFunds(request: models.Request):
    request.sender.balance -= request.amount
    request.receiver.balance += request.amount
    
def createCompletedTransactionLog(request: models.Request):
    return models.Transaction(
        transaction_id=1,
        sender=request.sender,
        receiver=request.receiver,
        amount=request.amount,
        status=enums.TransactionStatus.COMPLETED,
        payment_channel=enums.PaymentChannel.WALLET)

def saveTransaction(transaction: models.Transaction):
    return

def returnResult():
    return