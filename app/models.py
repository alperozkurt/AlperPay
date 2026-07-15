from __future__ import annotations
from datetime import datetime
from dataclasses import dataclass   
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
        nullable=True,
        unique=True
    )
    
    email: Mapped[str] = mapped_column(
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
        back_populates="owner",
        cascade="all, delete-orphan"
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
    
class Transaction(Base):
    __tablename__ = "transactions"
    
    transaction_id: Mapped[int] = mapped_column(
        Integer,
        Identity(start=1),
        primary_key=True
    )
    
    sender_wallet_id: Mapped[int] = mapped_column(
        ForeignKey("wallets.wallet_id"),
        nullable=False
    )
    
    sender: Mapped[Wallet] = relationship(
        "Wallet",
        foreign_keys=[sender_wallet_id]
    )
    
    receiver_wallet_id: Mapped[int] = mapped_column(
        ForeignKey("wallets.wallet_id"),
        nullable=False
    )
    
    receiver: Mapped[Wallet] = relationship(
        "Wallet",
        foreign_keys=[receiver_wallet_id]
    )
    
    amount: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    
    status: Mapped[enums.TransactionStatus] = mapped_column(
        Enum(enums.TransactionStatus),
        default=enums.TransactionStatus.COMPLETED,
        nullable=False
    )
    
    payment_channel: Mapped[enums.PaymentChannel] = mapped_column(
        Enum(enums.PaymentChannel),
        default=enums.PaymentChannel.WALLET,
        nullable=False
    )
    
    currency: Mapped[enums.Currency] = mapped_column(
        Enum(enums.Currency),
        nullable=False
    )
    
    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False
    )
     
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