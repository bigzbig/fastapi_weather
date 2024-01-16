from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from core.config import settings
from schemas.auth import TokenData
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


class Hash:
    pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def bcrypt(cls, password: str):
        return cls.pwd_cxt.hash(password)

    @classmethod
    def verify(cls, hashed_password, plain_password):
        return cls.pwd_cxt.verify(plain_password, hashed_password)


class Token:
    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str, credentials_exception):
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
            token_data = TokenData(email=email)
        except JWTError:
            raise credentials_exception


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth-token")


def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return Token.verify_token(data, credentials_exception)
