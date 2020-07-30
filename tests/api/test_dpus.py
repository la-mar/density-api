import logging

import pytest
import starlette.status as codes

from api.v1.endpoints.dpus import ERROR_404
from db.models import DPU as Model
from db.models import Doorway
from tests.utils import rand_int, rand_str

logger = logging.getLogger(__name__)

pytestmark = pytest.mark.asyncio

path: str = "/api/v1/dpus/"


@pytest.fixture(autouse=True)
async def seed_dpus(bind):
    for x in range(0, 30):
        await Model.create(**{"id": x})

    for x in range(0, 3):
        await Doorway.create(**{"name": rand_str(length=10)})


class TestEndpoint:
    async def test_create_dpu(self, client):
        response = await client.post(path, json={"id": 31})
        assert response.status_code == codes.HTTP_200_OK
        data = response.json()
        assert data["id"] == 31

    async def test_list_dpus(self, client):
        expected_record_count = 25
        response = await client.get(path)
        assert response.status_code == codes.HTTP_200_OK
        data = response.json()
        assert len(data) == expected_record_count
        assert response.links["next"] is not None

    async def test_get_dpu(self, client):
        id = 20
        response = await client.get(f"{path}{id}")
        assert response.status_code == codes.HTTP_200_OK
        data = response.json()
        assert data["id"] == 20

    async def test_update_exising_dpu(self, client):
        id = 10
        doorway_id = 1
        response = await client.put(f"{path}{id}", json={"doorway_id": doorway_id})
        assert response.status_code == codes.HTTP_200_OK
        data = response.json()
        assert data["id"] == id
        assert data["doorway_id"] == doorway_id

    async def test_partial_update_exising_dpu(self, client):
        id = 10
        doorway_id = 1
        response = await client.patch(f"{path}{id}", json={"doorway_id": doorway_id})
        assert response.status_code == codes.HTTP_200_OK
        data = response.json()
        assert data["id"] == id
        assert data["doorway_id"] == doorway_id

    async def test_update_dpu_not_found(self, client):
        id = 99999
        response = await client.put(
            f"{path}{id}", json={"doorway_id": rand_int(length=25)}
        )
        assert response.status_code == codes.HTTP_404_NOT_FOUND

    async def test_delete_existing_dpu(self, client):
        id = 20
        response = await client.delete(f"{path}{id}")
        assert response.status_code == codes.HTTP_200_OK
        data = response.json()
        assert data["id"] == id

    async def test_delete_dpu_not_found(self, client):
        id = 99999
        response = await client.delete(f"{path}{id}")
        assert response.status_code == codes.HTTP_404_NOT_FOUND
        data = response.json()
        assert data["detail"] == ERROR_404["detail"]
