import logging
import random

import pytest
import starlette.status as codes

from db.models import DPU
from db.models import Reading as Model
from util import utcnow

logger = logging.getLogger(__name__)

pytestmark = pytest.mark.asyncio

path: str = "/api/v1/readings/"


@pytest.fixture(autouse=True)
async def seed_readings(bind):
    for x in range(1, 4):
        await DPU.create(**{"id": x})

    for x in range(0, 30):
        await Model.create(
            **{
                "id": x,
                "dpu_id": random.choice([1, 2, 3]),
                "timestamp": utcnow(),
                "direction": random.choice([-1, 1]),
            }
        )


class TestEndpoint:
    async def test_create_reading(self, client):
        response = await client.post(
            path,
            json={"dpu_id": 1, "timestamp": "1944-06-06T00:00:00", "direction": -1},
        )
        assert response.status_code == codes.HTTP_200_OK
        data = response.json()
        assert data["dpu_id"] == 1

    async def test_list_readings(self, client):

        expected_record_count = 25
        response = await client.get(path)
        assert response.status_code == codes.HTTP_200_OK
        data = response.json()
        assert len(data) == expected_record_count
        assert response.links["next"] is not None

    async def test_get_reading(self, client):

        id = 20
        response = await client.get(f"{path}{id}")
        response
        assert response.status_code == codes.HTTP_200_OK
        data = response.json()
        assert data["id"] == 20
