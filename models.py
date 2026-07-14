from datetime import datetime
from dataclasses import dataclass, field
import enums
    
@dataclass
class User:
    user_id: int
    username: str
    status: enums.UserStatus = enums.UserStatus.ACTIVE
    created_at: datetime = field(default_factory=datetime.now) 
              
@dataclass
class Wallet:
    wallet_id: int
    owner: User 
    currency: enums.Currency
    balance: int = 0
    status: enums.WalletStatus = enums.WalletStatus.ACTIVE
    created_at: datetime = field(default_factory=datetime.now) 
    

@dataclass     
class Transaction:
    transaction_id: int
    sender: Wallet
    receiver: Wallet
    amount: int
    status: enums.TransactionStatus
    payment_channel: enums.PaymentChannel
    @property
    def currency(self):
        return self.sender.currency
    timestamp: datetime = field(default_factory=datetime.now) 
    
    
@dataclass
class ValidationResult:
    error: enums.TransactionErrors = enums.TransactionErrors.NONE
    @property
    def valid(self):
        return self.error == enums.TransactionErrors.NONE # If no error return true
    
@dataclass
class Request:
    sender: Wallet
    receiver: Wallet
    amount: int