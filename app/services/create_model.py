from app.models import Wallet, User
from app.enums import Currency
from app.helpers import generate_wallet_code
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


MAX_TRY_AMOUNT = 3


def create_wallet(session: Session, owner_id: int, currency: Currency, balance: int):
    
    for _ in range(MAX_TRY_AMOUNT):
            
        wallet = Wallet(
            identifier = generate_wallet_code(),
            owner_id = owner_id,
            currency = currency,
            balance = balance
        )
            
        try:
            session.add(wallet)
            session.commit()
            return wallet.identifier
            
        except IntegrityError:
            session.rollback()

    raise RuntimeError("Failed to generate unique wallet identifier")
    
        
def create_user(session: Session, username: str, email: str):
    
    try:
        user = User(
            username = username,
            email = email
        )
        
        session.add(user)
        session.commit()
        return user.username
    
    except:
        session.rollback()
        
    
