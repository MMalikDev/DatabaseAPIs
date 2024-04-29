from typing import Optional

import jwt as WebToken
from configs.core import settings
from database.dal.model.users import UserDal
from database.setup import get_db
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from models.tokens import TokenPayload
from models.users import Users
from pydantic import ValidationError
from sqlalchemy.orm import Session

user_db = UserDal()
tokenUrl = "http://fastapi.localhost/login/access-token"
reusable_oauth2 = OAuth2PasswordBearer(tokenUrl)


def send_reset_password_email(name, token):
    msg = "Sending email to %s with the following reset token: %s" % (name, token)
    print(msg)


def get_payload(token: str) -> Optional[TokenPayload]:
    try:
        payload = WebToken.decode(token, settings.SECRET_KEY, [settings.ALGORITHM])
        return TokenPayload(**payload)
    except (WebToken.PyJWTError, ValidationError):
        None


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> Users:
    if not (payload := get_payload(token)):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Could not validate credentials")
    if not (user := user_db.read_1(db, payload.id)):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    return user


def get_current_active_user(user: Users = Depends(get_current_user)) -> Users:
    if not user_db.is_active(user):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Inactive user")
    return user


def get_current_active_superuser(user: Users = Depends(get_current_user)) -> Users:
    if not user_db.is_superuser(user):
        detail = "The user doesn't have enough privileges"
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail)
    return user
