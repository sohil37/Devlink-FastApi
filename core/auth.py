from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt
import core.config as config
import bcrypt
bcrypt.__about__ = bcrypt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, config.ACCESS_TOKEN_SECRET_KEY, algorithm=config.TOKEN_ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=config.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, config.REFRESH_TOKEN_SECRET_KEY, algorithm=config.TOKEN_ALGORITHM)
    return encoded_jwt

def decode_token(token: str, secret_key):
    return jwt.decode(token, secret_key, algorithms=[config.TOKEN_ALGORITHM])