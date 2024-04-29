from typing import List, Optional

from controllers.base import BaseController
from database import ObjectID
from database.dal.nosql.asynchronous import DataAccessLayer, DataAccessLayerCached
from fastapi import Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel


class Controller(BaseController):
    def __init__(
        self,
        name: str,
        ModelBase: BaseModel,
        SchemaUpdate: BaseModel,
        SchemaCreate: BaseModel,
        cache: bool = True,
        cache_exp: int = 60,
        max_limit: int = 1000,
    ) -> None:
        super().__init__(name)

        self.ModelBase: BaseModel = ModelBase
        self.SchemaUpdate: BaseModel = SchemaUpdate
        self.SchemaCreate: BaseModel = SchemaCreate

        if cache:
            self.dal = DataAccessLayerCached(name, cache_exp, max_limit)
        else:
            self.dal = DataAccessLayer(name, max_limit)

    def add_list_endpoint(self):
        @self.router.get(
            "/",
            response_model=List[self.ModelBase],
            response_description=self.descriptions.LIST,
        )
        async def list(
            page: Optional[int] = 1, limit: Optional[int] = 100
        ) -> JSONResponse:
            content = await self.dal.read_all()
            content = self.pagination(content, page, limit)
            return JSONResponse(content, status.HTTP_200_OK)

    def add_create_endpoint(self):
        @self.router.post(
            "/",
            response_model=self.ModelBase,
            response_description=self.descriptions.CREATE,
        )
        async def create(data: self.SchemaCreate = Body(...)) -> JSONResponse:
            data = jsonable_encoder(data)
            content = await self.dal.create(data)
            return JSONResponse(content, status.HTTP_201_CREATED)

    def add_read_endpoint(self):
        @self.router.get(
            "/{id}",
            response_model=self.ModelBase,
            response_description=self.descriptions.READ,
        )
        async def read(id: ObjectID) -> JSONResponse:
            if not (content := await self.dal.read_1(id)):
                raise HTTPException(status.HTTP_404_NOT_FOUND, self._404_detail(id))
            return JSONResponse(content, status.HTTP_200_OK)

    def add_update_endpoint(self):
        @self.router.put(
            "/{id}",
            response_description=self.descriptions.UPDATE,
            response_model=self.ModelBase,
        )
        async def update(id: ObjectID, data: self.SchemaUpdate = Body(...)):
            data = {k: v for k, v in data.model_dump().items() if v}

            if not len(data):
                raise HTTPException(status.HTTP_411_LENGTH_REQUIRED)

            if not (content := await self.dal.update(id, data)):
                raise HTTPException(status.HTTP_404_NOT_FOUND, self._404_detail(id))
            return JSONResponse(content, status.HTTP_200_OK)

    def add_delete_endpoint(self):
        @self.router.delete(
            "/{id}",
            response_description=self.descriptions.DELETE,
        )
        async def delete(id: ObjectID) -> Response:
            if not (await self.dal.delete(id)):
                raise HTTPException(status.HTTP_404_NOT_FOUND, self._404_detail(id))
            return Response(status_code=status.HTTP_204_NO_CONTENT)
