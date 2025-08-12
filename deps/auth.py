from jwt import ExpiredSignatureError, InvalidTokenError
from fastapi import Depends, HTTPException, status
from core import config
from core.auth import decode_token
from deps.base import oauth2_scheme

def get_user_id_from_access_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token, config.ACCESS_TOKEN_SECRET_KEY)
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    if payload.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
    try:
        return int(payload.get("sub"))
    except (TypeError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user ID in token")
