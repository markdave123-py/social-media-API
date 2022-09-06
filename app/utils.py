from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated= "auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify(attempt_password,main_password):
    return pwd_context.verify(attempt_password,main_password)
