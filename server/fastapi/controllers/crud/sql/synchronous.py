from typing import List

from controllers.base import BaseController
from database import ID, Base, get_db
from database.dal.sql.synchronous import DataAccessLayer, DataAccessLayerCached
from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session


class Controller(BaseController):
    def __init__(
        self,
        name: str,
        Model: Base,
        SchemaBase: BaseModel,
        SchemaCreate: BaseModel,
        SchemaUpdate: BaseModel,
        cache: bool = True,
        cache_exp: int = 60,
        max_limit: int = 1000,
    ) -> None:
        super().__init__(name)

        self.Model = Model

        self.SchemaBase = SchemaBase
        self.SchemaCreate = SchemaCreate
        self.SchemaUpdate = SchemaUpdate

        if cache:
            self.dal = DataAccessLayerCached(self.Model, cache_exp, max_limit)
        else:
            self.dal = DataAccessLayer(self.Model, max_limit)

    def add_list_endpoint(self) -> None:
        @self.router.get(
            "/",
            response_model=List[self.SchemaBase],
            response_description=self.descriptions.LIST,
        )
        def list(
            *, db: Session = Depends(get_db), page: int = 1, limit: int = 100
        ) -> JSONResponse:
            content = self.dal.read_all(db, page, limit)
            return JSONResponse(jsonable_encoder(content), status.HTTP_200_OK)

    def add_create_endpoint(self) -> None:
        @self.router.post(
            "/",
            response_model=self.SchemaBase,
            response_description=self.descriptions.CREATE,
        )
        def create(
            *, db: Session = Depends(get_db), data: self.SchemaCreate
        ) -> JSONResponse:
            data = data.model_dump()
            if not (content := self.dal.create(db, data)):
                return JSONResponse(content, status.HTTP_302_FOUND)
            return JSONResponse(jsonable_encoder(content), status.HTTP_201_CREATED)

    def add_read_endpoint(self) -> None:
        @self.router.get(
            "/{id}",
            response_model=self.SchemaBase,
            response_description=self.descriptions.READ,
        )
        def read(*, db: Session = Depends(get_db), id: ID) -> JSONResponse:
            if not (content := self.dal.read_1(db, id)):
                raise HTTPException(status.HTTP_404_NOT_FOUND, self._404_detail(id))
            return JSONResponse(jsonable_encoder(content), status.HTTP_200_OK)

    def add_update_endpoint(self) -> None:
        @self.router.put(
            "/{id}",
            response_model=self.SchemaBase,
            response_description=self.descriptions.UPDATE,
        )
        def update(
            *, db: Session = Depends(get_db), id: ID, data: self.SchemaUpdate
        ) -> JSONResponse:
            data = data.model_dump()
            if not (content := self.dal.update(db, id, data)):
                raise HTTPException(status.HTTP_404_NOT_FOUND, self._404_detail(id))
            return JSONResponse(jsonable_encoder(content), status.HTTP_200_OK)

    def add_delete_endpoint(self) -> None:
        @self.router.delete(
            "/{id}",
            response_description=self.descriptions.DELETE,
        )
        def delete(*, db: Session = Depends(get_db), id: ID) -> Response:
            if not self.dal.delete(db, id):
                raise HTTPException(status.HTTP_404_NOT_FOUND, self._404_detail(id))
            return Response(status_code=status.HTTP_204_NO_CONTENT)
