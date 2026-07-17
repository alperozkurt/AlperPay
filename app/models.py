from __future__ import annotations
from datetime import datetime
from dataclasses import dataclass   
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, Enum, Integer, String, Identity, ForeignKey
from app.enums import UserStatus, Currency, WalletStatus, TransactionStatus, PaymentChannel, TransactionErrors

    
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
    
    email: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True
    )
    
    status: Mapped[UserStatus] = mapped_column(
        Enum(UserStatus),
        default=UserStatus.ACTIVE,
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
    
    identifier: Mapped[str] = mapped_column(
        String(8),
        unique=True,
        nullable=False,
    )
    
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"),
        nullable=False
    )
    
    owner: Mapped[User] = relationship(
        back_populates="wallets"
    ) 
    
    currency: Mapped[Currency] = mapped_column(
        Enum(Currency),
        nullable=False
    )
    
    balance: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )
    
    status: Mapped[WalletStatus] = mapped_column(
        Enum(WalletStatus),
        default=WalletStatus.ACTIVE,
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
    
    status: Mapped[TransactionStatus] = mapped_column(
        Enum(TransactionStatus),
        default=TransactionStatus.COMPLETED,
        nullable=False
    )
    
    payment_channel: Mapped[PaymentChannel] = mapped_column(
        Enum(PaymentChannel),
        default=PaymentChannel.WALLET,
        nullable=False
    )
    
    currency: Mapped[Currency] = mapped_column(
        Enum(Currency),
        nullable=False
    )
    
    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False
    )
     
@dataclass
class ValidationResult:
    error: TransactionErrors = TransactionErrors.NONE
    @property
    def valid(self):
        return self.error == TransactionErrors.NONE # If no error return true
    
@dataclass
class Request:
    sender: Wallet
    receiver: Wallet
    amount: int