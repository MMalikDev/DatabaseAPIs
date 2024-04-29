from typing import Any

from configs.core import settings
from controllers.auth.utils import get_current_user, send_reset_password_email
from database import get_db
from database.dal.model.users import UserDal
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.responses import JSONResponse, Response
from fastapi.security import OAuth2PasswordRequestForm
from lib.token import create_access_token, generate_reset_token, verify_reset_token
from models.tokens import Token
from models.users import Users, UsersSchema
from sqlalchemy.orm import Session


class LoginController:
    def __init__(self) -> None:
        self.router = APIRouter()
        self.user = UserDal()

    def add_login_endpoints(self) -> None:
        self.add_login_access_token()
        self.add_test_token()
        self.add_reset_password()
        self.add_recover_password()

    def add_login_access_token(self):
        @self.router.post("/login/access-token", response_model=Token)
        def login_access_token(
            db: Session = Depends(get_db),
            form_data: OAuth2PasswordRequestForm = Depends(),
        ) -> Any:
            """
            OAuth2 compatible token login, get an access token for future requests
            """
            user = self.user.authenticate(db, form_data.username, form_data.password)
            if not user:
                raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credential")
            if not self.user.is_active(user):
                raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Inactive user")
            access_token_expires = settings.ACCESS_TOKEN_EXPIRE_MINUTES
            token = create_access_token(user.id, access_token_expires)
            return JSONResponse({"access_token": token, "token_type": "bearer"})

    def add_test_token(self):
        @self.router.post("/login/test-token", response_model=UsersSchema)
        def test_token(current_user: Users = Depends(get_current_user)) -> Users:
            """
            Test access token
            """
            return current_user

    def add_recover_password(self):
        @self.router.post("/password-recovery")
        def recover_password(name: str, db: Session = Depends(get_db)) -> JSONResponse:
            """
            Password Recovery
            """
            if not (user := self.user.get_by_name(db, name)):
                raise HTTPException(status.HTTP_404_NOT_FOUND, "User does not exist")
            password_reset_token = generate_reset_token(name)
            send_reset_password_email(user.username, password_reset_token)
            message = {"msg": "Password recovery email sent"}
            return JSONResponse(message, status.HTTP_205_RESET_CONTENT)

    def add_reset_password(self):
        @self.router.post("/reset-password")
        def reset_password(
            db: Session = Depends(get_db),
            token: str = Body(...),
            new_password: str = Body(...),
        ) -> Response:
            """
            Reset password
            """
            if not (name := verify_reset_token(token)):
                raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid token")
            if not (user := self.user.get_by_name(db, name)):
                raise HTTPException(status.HTTP_404_NOT_FOUND, "User does not exist")
            if not self.user.is_active(user):
                raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Inactive user")
            self.user.change_password(db, name, new_password)
            return Response(status_code=status.HTTP_200_OK)
