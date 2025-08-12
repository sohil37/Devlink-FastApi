from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from routes import auth, health_check
app = FastAPI(title="Devlink API")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Dependency to get the token
def get_access_token(access_token: str = Depends(oauth2_scheme)):
    return access_token

# Routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(health_check.router, prefix="/health_check", tags=["Health Check"])

