from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from routes import auth, health_check

app = FastAPI(title="Devlink API")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(health_check.router, prefix="/health_check", tags=["Health Check"])

