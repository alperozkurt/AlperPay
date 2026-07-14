import models, enums, payment_engine

# init 2 users -> init 2 wallets with same currency and some balance -> test a transaction

alper = models.User(1,"alper")
mert = models.User(2,"mert")

alper_wallet = models.Wallet(1,alper,enums.Currency.TRY,800)
mert_wallet = models.Wallet(2,mert,enums.Currency.TRY,200)


print("Before payment",alper_wallet.balance,mert_wallet.balance,sep="\n")

payment_engine.sendPayment(alper_wallet,mert_wallet,200)

print("After payment",alper_wallet.balance,mert_wallet.balance,sep="\n")