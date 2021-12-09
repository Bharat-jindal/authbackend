import bcrypt
import jwt
from .config import SECRET_KEY

def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(plain_text_password, hashed_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))

def generatetoken(user):
    #Will generate toke with load as user
    return jwt.encode(user,SECRET_KEY)

def verifytoken(token):
    #Verify the token for each request
    try:
        user = jwt.decode(token,SECRET_KEY, algorithms=["HS256"])
        return user
    except Exception as error:
        print(error)
        return None