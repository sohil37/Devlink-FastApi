from fastapi import FastAPI
from routes import auth, user, health_check
app = FastAPI(title="Devlink API")

# Routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(health_check.router, prefix="/health_check", tags=["Health Check"])

# For debugging
import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)