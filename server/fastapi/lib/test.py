from unittest import TestCase

from fastapi import APIRouter, FastAPI
from fastapi.responses import Response
from fastapi.testclient import TestClient
from lib.utilities import logger, test_logger


class TestPytest(TestCase):
    def __init__(
        self,
        methodName="runTest",
        *,
        name: str,
        example: dict,
        router: APIRouter,
        path="/test",
        id_field="id",
        nonexisting_id="nonexisting_id",
    ) -> None:
        super().__init__(methodName)
        self.name = name
        self.example = example

        self.path = path
        self.id_field = id_field
        self.endpoint = path + "/%s/"
        self.nonexisting_id = self.endpoint % nonexisting_id

        self.app = FastAPI()
        self.client = TestClient(self.app)
        self.app.include_router(router, prefix=path)

    # LIST
    def test_list(self) -> None:
        response = self.client.get(self.path)
        assert response.status_code == 200
        assert type(response.json()) == list

    # POST
    def test_create(self) -> None:
        response = self.client.post(self.path, json=self.example)
        body = response.json()
        assert response.status_code == 201
        for key, value in self.example.items():
            assert body.get(key) == value
        assert self.id_field in body

    def test_create_missing_field(self) -> None:
        for field in self.example.keys():
            incomplete_example = self.example.copy()
            incomplete_example.pop(field)
            response = self.client.post(self.path, json=incomplete_example)
            assert response.status_code == 422

    # GET
    def test_get(self) -> None:
        data = self.client.post(self.path, json=self.example).json()
        path = self.endpoint % data.get(self.id_field)
        response = self.client.get(path)
        assert response.status_code == 200
        assert response.json() == data

    def test_get_nonexisting(self) -> None:
        response = self.client.get(self.nonexisting_id)
        assert response.status_code == 404

    # PUT
    def test_update(self) -> None:
        data = self.client.post(self.path, json=self.example).json()
        path = self.endpoint % data.get(self.id_field)
        response = self.client.put(path, json=self.example)
        assert response.status_code == 200
        for key, value in self.example.items():
            assert response.json().get(key) == value

    def test_update_nonexisting(self) -> None:
        response = self.client.put(self.nonexisting_id, json=self.example)
        assert response.status_code == 404

    # DELETE
    def test_delete(self) -> None:
        data = self.client.post(self.path, json=self.example).json()
        path = self.endpoint % data.get(self.id_field)
        response = self.client.delete(path)
        assert response.status_code == 204

    def test_delete_nonexisting(self) -> None:
        response = self.client.delete(self.nonexisting_id)
        assert response.status_code == 404


class TestCustom:
    def __init__(
        self,
        name: str,
        example: dict,
        router: APIRouter,
        path: str = "/test",
        id_field: str = "id",
        nonexisting_id: str = "nonexisting_id",
    ) -> None:
        self.name = name
        self.example = example

        self.path = path
        self.id_field = id_field
        self.endpoint = path + "/%s/"
        self.nonexisting_id = self.endpoint % nonexisting_id

        self.app = FastAPI()
        self.client = TestClient(self.app)

        self.app.include_router(router, prefix=path)

    def default(self) -> None:
        # POST
        self.test_list()

        # POST
        self.test_create()
        self.test_create_missing_field()

        # GET
        self.test_get()
        self.test_get_nonexisting()

        # # PUT
        self.test_update()
        self.test_update_nonexisting()

        # DELETE
        self.test_delete()
        self.test_delete_nonexisting()

    def run(self) -> None:
        delimiter = f"{'#'*50}\n"
        message = f"Running tests for {self.name} API\n"

        logger.info(delimiter)
        logger.info(message)

        self.default()

        logger.info(delimiter)

    def initialise_example(self) -> dict:
        return self.client.post(self.path, json=self.example).json()

    # LIST
    @test_logger
    def test_list(self) -> None:
        response: Response = self.client.get(self.path)
        assert response.status_code == 200
        assert type(response.json()) == list

    # POST
    @test_logger
    def test_create(self) -> None:
        response: Response = self.client.post(self.path, json=self.example)
        body: dict = response.json()
        assert response.status_code == 201
        for key, value in self.example.items():
            assert body.get(key) == value
        assert self.id_field in body

    @test_logger
    def test_create_missing_field(self) -> None:
        for field in self.example.keys():
            incomplete_example: dict = self.example.copy()
            incomplete_example.pop(field)
            response: Response = self.client.post(self.path, json=incomplete_example)
            assert response.status_code == 422

    # GET
    @test_logger
    def test_get(self) -> None:
        data: dict = self.initialise_example()
        path: str = self.endpoint % data.get(self.id_field)
        response: Response = self.client.get(path)
        assert response.status_code == 200
        assert response.json() == data

    @test_logger
    def test_get_nonexisting(self) -> None:
        response: Response = self.client.get(self.nonexisting_id)
        assert response.status_code == 404

    # PUT
    @test_logger
    def test_update(self) -> None:
        data: dict = self.initialise_example()
        path: str = self.endpoint % data.get(self.id_field)
        response: Response = self.client.put(path, json=self.example)
        assert response.status_code == 200
        for key, value in self.example.items():
            assert response.json().get(key) == value

    @test_logger
    def test_update_nonexisting(self) -> None:
        response: Response = self.client.put(self.nonexisting_id, json=self.example)
        assert response.status_code == 404

    # DELETE
    @test_logger
    def test_delete(self) -> None:
        data: dict = self.initialise_example()
        path: str = self.endpoint % data.get(self.id_field)
        response: Response = self.client.delete(path)
        assert response.status_code == 204

    @test_logger
    def test_delete_nonexisting(self) -> None:
        response: Response = self.client.delete(self.nonexisting_id)
        assert response.status_code == 404
