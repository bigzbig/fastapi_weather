from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from core.db import get_db
from core.security import Hash, Token
from models.user import User
from sqlalchemy.orm import Session

router = APIRouter(tags=["Authentication"])


@router.post("/v1/auth-token")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect password")

    access_token = Token.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
