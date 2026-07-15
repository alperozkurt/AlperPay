from database import SessionLocal
from models import User, Wallet
import enums

session = SessionLocal()

user = User(username = "mert")

wallet1 = Wallet(
    owner_id = 9,
    currency = enums.Currency.TRY,
    balance = 200
)

wallet2 = Wallet(
    owner_id = 9,
    currency = enums.Currency.USD,
    balance = 40
)

# session.add(user)
session.add(wallet1)
session.add(wallet2)

"""
session.add(user)
session.refresh(user)
print(user.user_id,user.username,user.created_at,sep="\n")
"""
session.commit()
session.close()