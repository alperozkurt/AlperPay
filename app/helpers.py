import secrets

ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ" # I and O is removed for clarity
RNG = secrets.SystemRandom()

def generate_wallet_code() -> str:  
    letters = ''.join(RNG.sample(ALPHABET, 4))
    numbers = f"{secrets.randbelow(10000):04d}"
    return letters+numbers