from datetime import datetime
from dataclasses import dataclass, field
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, Enum, Integer, String, Identity, ForeignKey
import enums
    
class User(Base):
    __tablename__ = "users"
    
    user_id: Mapped[int] = mapped_column(
        Integer,
        Identity(start=1),
        primary_key=True
    )
    
    username: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True
    )
    
    status: Mapped[enums.UserStatus] = mapped_column(
        Enum(enums.UserStatus),
        default=enums.UserStatus.ACTIVE,
        nullable=False
    )
    
    wallets: Mapped[list[Wallet]] = relationship(
        back_populates="owner"
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False
    ) 
              
class Wallet(Base):
    __tablename__ = "wallets"
    
    wallet_id: Mapped[int] = mapped_column(
        Integer,
        Identity(start=1),
        primary_key=True
    )
    
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"),
        nullable=False
    )
    
    owner: Mapped[User] = relationship(
        back_populates="wallets"
    ) 
    
    currency: Mapped[enums.Currency] = mapped_column(
        Enum(enums.Currency),
        nullable=False
    )
    
    balance: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    
    status: Mapped[enums.WalletStatus] = mapped_column(
        Enum(enums.WalletStatus),
        default=enums.WalletStatus.ACTIVE,
        nullable=False
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False
    )
    

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