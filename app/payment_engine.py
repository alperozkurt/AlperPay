import models,enums
from database import SessionLocal

session = SessionLocal()
    
def sendPayment(sender_id: int, receiver_id: int, amount):
    
    sender_wallet = session.query(models.Wallet).get(sender_id)
    receiver_wallet = session.query(models.Wallet).get(receiver_id)
    if sender_wallet == None or receiver_wallet == None: return

    request = models.Request(
        sender_wallet,
        receiver_wallet,
        amount)
    
    validationResult = validateRequest(request)
    
    if validationResult.valid:
        transferFunds(request)
        
        createCompletedTransactionLog(request)
        
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
    transaction = models.Transaction(
        sender=request.sender,
        receiver=request.receiver,
        amount=request.amount,
        currency=request.sender.currency,
        status=enums.TransactionStatus.COMPLETED,
        payment_channel=enums.PaymentChannel.WALLET)
    session.add(transaction)
    session.commit()
    session.close()
