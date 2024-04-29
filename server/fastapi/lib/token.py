from datetime import datetime, timedelta
from typing import Optional

import jwt as WebToken
from configs.core import settings
from database import ID


def create_access_token(id: ID, exp_delta: Optional[timedelta] = None) -> str:
    duration = exp_delta if exp_delta else settings.ACCESS_TOKEN_EXPIRE_MINUTES
    expire = datetime.now() + duration
    payload = {"exp": expire, "id": str(id)}
    return WebToken.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)


def generate_reset_token(username: str) -> str:
    now = datetime.now()
    expires = now + settings.RESET_TOKEN_EXPIRE_HOURS
    exp = expires.timestamp()
    payload = {"exp": exp, "nbf": now, "id": username}
    return WebToken.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)


def verify_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = WebToken.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        return decoded_token.get("id")
    except WebToken.PyJWTError:
        return None
