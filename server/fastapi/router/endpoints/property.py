from typing import List, Union

from controllers.crud.sql.synchronous import Controller
from database import ID, Base
from database.dal.model.property import PropertyDal
from database.dal.model.users import UserDal
from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse, Response
from models.property import Property
from models.users import Users
from pydantic import BaseModel
from sqlalchemy.orm import Session


class ItemController(Controller):
    def __init__(
        self,
        name: str,
        Model: Base,
        SchemaBase: BaseModel,
        SchemaCreate: BaseModel,
        SchemaUpdate: BaseModel,
        cache: int = 60,
    ) -> None:
        super().__init__(name, Model, SchemaBase, SchemaCreate, SchemaUpdate, cache)
        self.dal = PropertyDal(self.Model, cache)
        self.users = UserDal(Users)

    # Default endpoints
    def add_list(self):
        @self.router.get("/", response_model=List[self.SchemaBase])
        def list(
            *,
            db: Session = Depends(get_db),
            current_user: self.Model = Depends(get_current_active_user),
            page: int = 0,
            limit: int = 100,
        ) -> JSONResponse:
            """
            Retrieve property.
            """
            content = (
                self.dal.read_all(db, page, limit)
                if self.users.is_superuser(current_user)
                else self.dal.list_by_owner(db, current_user.id, page, limit)
            )
            return JSONResponse(content, status.HTTP_200_OK)

    def add_create(self):
        @self.router.post("/", response_model=self.SchemaBase)
        def create(
            *,
            db: Session = Depends(get_db),
            current_user: self.Model = Depends(get_current_active_user),
            data: self.SchemaCreate,
        ) -> JSONResponse:
            """
            Create new property.
            """
            new_data = self.dal.create_with_owner(db, data, current_user.id)
            return JSONResponse(status_code=status.HTTP_201_CREATED, content=new_data)

    def add_update(self):
        @self.router.put("/{id}", response_model=self.SchemaBase)
        def update(
            *,
            db: Session = Depends(get_db),
            current_user: self.Model = Depends(get_current_active_user),
            id: ID,
            data: self.SchemaUpdate,
        ) -> JSONResponse:
            """
            Update an property.
            """
            self.check_permissions(db, current_user, id)
            return super().dal.update(db, id, data)

    def add_read(self):
        @self.router.get("/{id}", response_model=self.SchemaBase)
        def read(
            *,
            id: Union[int, str],
            db: Session = Depends(get_db),
            current_user: self.Model = Depends(get_current_active_user),
        ) -> JSONResponse:
            """
            Get property by ID.
            """
            self.check_permissions(db, current_user, id)
            return super().dal.read_1(db, id)

    def add_delete(self):
        @self.router.delete("/{id}", response_model=self.SchemaBase)
        def delete(
            *,
            db: Session = Depends(get_db),
            current_user: self.Model = Depends(get_current_active_user),
            id: ID,
        ) -> Response:
            """
            Delete an property.
            """
            self.check_permissions(db, current_user, id)
            return super().dal.delete(db, id)

    # Utilities
    def check_permissions(self, db: Session, current_user: Users, id: ID) -> None:
        if not (property := self.dal.read_1(db, id)):
            raise HTTPException(status.HTTP_404_NOT_FOUND, self._404_detail(id))
        is_owner: bool = property.owner_id != current_user.id
        is_superuser: bool = self.users.is_superuser(current_user)
        if not (is_owner and is_superuser):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Not enough permissions")
