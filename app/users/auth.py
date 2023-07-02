from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.config import settings
from app.exceptions import IncorrectEmailOrPasswordException
from app.users.dao import UsersDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    token_expiration = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": token_expiration})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, settings.JWT_ENCODING)
    return encoded_jwt


async def auth_user(email: EmailStr, password: str):
    user = await UsersDAO.find_one_or_none(email=email)
    # Check if credentials exist
    if not (user and verify_password(password, user.hashed_password)):
        raise IncorrectEmailOrPasswordException
    return user
