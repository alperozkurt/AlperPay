from enum import Enum

class Currency(Enum):
    TRY = ("TRY", "Turkish Lira", 2)
    USD = ("USD", "US Dollar", 2)
    EUR = ("EUR", "Euro", 2)
    GBP = ("GBP", "Sterling", 2)
    JPY = ("JPY", "Japanese Yen", 0)
    
    def __init__(self,code,full_name,decimal_places):
        self.code = code
        self.full_name = full_name
        self.decimal_places = decimal_places
        
class UserStatus(Enum):
    ACTIVE = "Active"
    PENDING = "Pending"
    DEACTIVATED = "Deactivated"
    DELETED = "Deleted"
    
class WalletStatus(Enum):
    ACTIVE = "Active"
    LOCKED = "Locked"
    FROZEN = "Frozen"
    CLOSED = "Closed"
    
class TransactionStatus(Enum):
    PENDING = "Pending"
    PROCESSING = "Processing"
    COMPLETED = "Completed"
    FAILED = "Failed"
    CANCELLED = "Cancelled"
    REFUNDED = "Refunded"
    
class TransactionErrors(Enum):
    SUCCESS = "Success"
    NONE = "No error."
    FAILED = "Transaction failed."
    FUNDS = "Not enough funds."
    WALLET_CURRENCY = "Wallet currency mismatch."
    WALLET_EXIST = "Wallet does not exist."
    WALLET_NOT_ACTIVE = "Wallet is not active."
    USER_NOT_ACTIVE = "User is not active."
    INVALID_AMOUNT = "Invalid amount."
    
class PaymentChannel(Enum):
    WALLET = "Wallet number"
    QR_CODE = "Qr code"
    NFC = "NFC"