from app.models import Wallet, Request, Transaction, ValidationResult
from app.enums import TransactionErrors, UserStatus, TransactionStatus, WalletStatus, PaymentChannel
from sqlalchemy.orm import Session
    
def create_transfer(session: Session, sender_id: int, receiver_id: int, amount):
    
    sender_wallet = session.get(Wallet, sender_id)
    receiver_wallet = session.get(Wallet, receiver_id)
    if sender_wallet == None or receiver_wallet == None: return TransactionErrors.WALLET_EXIST

    request = Request(
        sender_wallet,
        receiver_wallet,
        amount)
    
    validationResult = validateRequest(request)
    
    if validationResult.valid:
        
        try:
            transferFunds(request)
            
            session.add(createCompletedTransactionLog(request))
            
            session.commit()
            
            return TransactionErrors.SUCCESS
        
        except:
            session.rollback()
            raise
        
    else:
        return validationResult.error

def validateRequest(request: Request):
    
    if request.sender.wallet_id == request.receiver.wallet_id: 
        return ValidationResult(TransactionErrors.FAILED)
    
    elif request.sender.owner.status != UserStatus.ACTIVE or request.receiver.owner.status != UserStatus.ACTIVE:
        return ValidationResult(TransactionErrors.USER_NOT_ACTIVE)
    
    elif request.sender.status != WalletStatus.ACTIVE or request.receiver.status != WalletStatus.ACTIVE:
        return ValidationResult(TransactionErrors.WALLET_NOT_ACTIVE)
    
    elif request.sender.currency != request.receiver.currency:
        return ValidationResult(TransactionErrors.WALLET_CURRENCY)
    
    elif request.sender.balance < request.amount:
        return ValidationResult(TransactionErrors.FUNDS)
    
    elif request.amount <= 0:
        return ValidationResult(TransactionErrors.INVALID_AMOUNT)
    
    else:
        return ValidationResult()

def transferFunds(request: Request):
    request.sender.balance -= request.amount
    request.receiver.balance += request.amount
    
def createCompletedTransactionLog(request: Request):
    return Transaction(
        sender=request.sender,
        receiver=request.receiver,
        amount=request.amount,
        currency=request.sender.currency,
        status=TransactionStatus.COMPLETED,
        payment_channel=PaymentChannel.WALLET)
