import logging

import pytest
import starlette.status as codes

from api.v1.endpoints.doorways import ERROR_404
from db.models import Doorway as Model
from tests.utils import rand_str

logger = logging.getLogger(__name__)

pytestmark = pytest.mark.asyncio

path: str = "/api/v1/doorways/"


@pytest.fixture(autouse=True)
async def seed_doorways(bind):
    for x in range(0, 30):
        await Model.create(**{"name": rand_str(min=10, max=25)})


class TestEndpoint:
    async def test_create_doorway(self, client):
        response = await client.post(path, json={"name": "test"})
        assert response.status_code == codes.HTTP_200_OK
        data = response.json()
        assert data["id"] == 31

    async def test_list_doorways(self, client):
        expected_record_count = 25
        response = await client.get(path)
        assert response.status_code == codes.HTTP_200_OK
        data = response.json()
        assert len(data) == expected_record_count
        assert response.links["next"] is not None

    async def test_get_doorway(self, client):
        id = 20
        response = await client.get(f"{path}{id}")
        assert response.status_code == codes.HTTP_200_OK
        data = response.json()
        assert data["id"] == 20

    async def test_update_exising_doorway(self, client):
        id = 10
        name = rand_str(length=25)
        response = await client.put(f"{path}{id}", json={"name": name})
        assert response.status_code == codes.HTTP_200_OK
        data = response.json()
        assert data["id"] == id
        assert data["name"] == name

    async def test_partial_update_exising_doorway(self, client):
        id = 10
        name = rand_str(length=25)
        response = await client.patch(f"{path}{id}", json={"name": name})
        assert response.status_code == codes.HTTP_200_OK
        data = response.json()
        assert data["id"] == id
        assert data["name"] == name

    async def test_update_doorway_not_found(self, client):
        id = 99999
        response = await client.put(f"{path}{id}", json={"name": rand_str(length=25)})
        assert response.status_code == codes.HTTP_404_NOT_FOUND

    async def test_delete_existing_doorway(self, client):
        id = 20
        response = await client.delete(f"{path}{id}")
        assert response.status_code == codes.HTTP_200_OK
        data = response.json()
        assert data["id"] == id

    async def test_delete_doorway_not_found(self, client):
        id = 99999
        response = await client.delete(f"{path}{id}")
        assert response.status_code == codes.HTTP_404_NOT_FOUND
        data = response.json()
        assert data["detail"] == ERROR_404["detail"]
