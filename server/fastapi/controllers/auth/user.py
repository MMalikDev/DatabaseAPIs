from controllers.crud.sql.synchronous import Controller
from database import ID, Base, get_db
from database.dal.model.users import UserDal
from fastapi import Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models.users import Users, UsersSchema, UsersSchemaCreate, UsersSchemaUpdate
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .utils import get_current_active_user


class UsersControllers(Controller):
    def __init__(
        self,
        name: str,
        Model: Base = Users,
        SchemaBase: BaseModel = UsersSchema,
        SchemaCreate: BaseModel = UsersSchemaCreate,
        SchemaUpdate: BaseModel = UsersSchemaUpdate,
        max_limit: ID = 1000,
    ) -> None:
        super().__init__(name, Model, SchemaBase, SchemaCreate, SchemaUpdate)
        self.dal = UserDal(self.Model, max_limit)

    # Base Configuration
    def add_user_endpoints(self) -> None:
        self.add_signup_endpoint()
        self.add_read_profile_endpoint()
        self.add_update_profile_endpoint()
        self.add_profiles_endpoint()

    def add_signup_endpoint(self):
        @self.router.post("/signup", response_model=self.SchemaBase)
        def signup(
            *,
            db: Session = Depends(get_db),
            username: str = Body(None),
            password: str = Body(...),
        ) -> JSONResponse:
            """
            Create new user.
            """
            if self.dal.get_by_name(db, username):
                raise HTTPException(status.HTTP_400_BAD_REQUEST, "User already exists")

            data = self.SchemaCreate(username=username, password=password)
            content = self.dal.create(db, data.model_dump())
            return JSONResponse(jsonable_encoder(content), status.HTTP_201_CREATED)

    def add_read_profile_endpoint(self):
        @self.router.get("/profile", response_model=self.SchemaBase)
        def profile(
            current_user: self.Model = Depends(get_current_active_user),
        ) -> JSONResponse:
            """
            Get current user profile.
            """
            return JSONResponse(jsonable_encoder(current_user), status.HTTP_200_OK)

    def add_update_profile_endpoint(self):
        @self.router.put("/profile", response_model=self.SchemaBase)
        def update_profile(
            *,
            db: Session = Depends(get_db),
            current_user: self.Model = Depends(get_current_active_user),
            name: str = Body(None),
            password: str = Body(None),
        ) -> JSONResponse:
            """
            Update current user profile
            """
            user = jsonable_encoder(current_user)
            data = self.SchemaUpdate(**user)
            data = data.model_dump()
            if password:
                data["password"] = password
            if name:
                data["username"] = name
            content = self.dal.update(db, current_user.id, data)
            return JSONResponse(jsonable_encoder(content), status.HTTP_200_OK)

    def add_profiles_endpoint(self):
        @self.router.get("/profile/{id}", response_model=self.SchemaBase)
        def profiles(
            *,
            db: Session = Depends(get_db),
            current_user: self.Model = Depends(get_current_active_user),
            id: int,
        ) -> JSONResponse:
            """
            Get a specific user profile by id.
            """
            if not (user := self.dal.read_1(db, id)):
                raise HTTPException(status.HTTP_404_NOT_FOUND, self._404_detail(id))
            if user != current_user and not self.dal.is_superuser(current_user):
                raise HTTPException(
                    status.HTTP_403_FORBIDDEN, "Insufficient privileges"
                )
            return JSONResponse(jsonable_encoder(user), status.HTTP_200_OK)
