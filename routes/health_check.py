from fastapi import APIRouter, HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from db.session import engine

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK)
def health_check():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy"}
    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed"
        )