import logging

import pytest
from sqlalchemy import BigInteger, Column
from sqlalchemy.schema import PrimaryKeyConstraint
from sqlalchemy.sql.base import ImmutableColumnCollection

from db.models import Space as Model
from db.models.bases import Base, ColumnProxy, PrimaryKeyProxy
from tests.utils import rand_str

logger = logging.getLogger(__name__)


@pytest.fixture
def id_gen():
    i = 1
    yield i
    i += 1


class TestModel:
    @pytest.mark.asyncio
    async def test_create_instance(self, bind):
        result = await Model.create(id=999, name=rand_str(length=25))
        assert result.to_dict()["id"] == 999

    @pytest.mark.parametrize(
        "constraint",
        [
            "pk_spaces",
            "uq_spaces_name",
            Model.pk,
            Model.uq_name
            #
        ],
    )
    @pytest.mark.asyncio
    async def test_merge(self, constraint, bind):

        kwargs = {"constraint": constraint, "name": rand_str(length=25)}

        obj1 = await Model.merge(**kwargs)
        logger.debug(obj1.created_at)

        kwargs = {"constraint": constraint, "name": rand_str(length=25)}

        obj2 = await Model.merge(**kwargs)
        logger.debug(obj2.created_at)

        assert obj1.created_at < obj2.created_at

    def test_model_repr(self):
        repr(Model())

    def test_columns_property_alias(self):
        assert Model.c == Model.columns

    def test_base_repr(self):
        repr(Base)

    def test_model_name_property(self):
        assert Base.__model_name__ == "db.models.bases.Base"


class TestColumnProxy:
    def test_sa_obj_type(self):
        assert isinstance(Model.c.sa_obj, ImmutableColumnCollection)

    def test_iter(self):
        for c in Model.columns:
            assert isinstance(c, Column)

    def test_get_column_pytypes(self):
        assert Model.c.pytypes["id"] == int

    def test_get_column_dtype(self):
        assert isinstance(Model.c.dtypes["id"], BigInteger)

    def test_get_item_by_name(self):
        assert isinstance(Model.c["id"], Column)
        assert Model.c["id"].name == "id"

    def test_get_item_by_index(self):
        assert isinstance(Model.c[0], Column)
        assert Model.c[0].name == "id"


class TestPrimaryKeyProxy:
    def test_sa_obj_type(self):
        assert isinstance(Model.pk.sa_obj, PrimaryKeyConstraint)

    def test_iter(self):
        for p in Model.pk:
            assert isinstance(p, Column)

    def test_get_column_pytypes(self):
        assert Model.pk.pytypes["id"] == int

    def test_get_column_dtype(self):
        assert isinstance(Model.pk.dtypes["id"], BigInteger)

    def test_get_item_by_name(self):
        assert isinstance(Model.pk["id"], Column)
        assert Model.pk["id"].name == "id"

    def test_get_item_by_index(self):
        assert isinstance(Model.pk[0], Column)
        assert Model.pk[0].name == "id"

    def test_access_pk_names(self, bind):
        assert Model.pk.names == ["id"]

    def test_pk_repr(self, bind):
        assert repr(Model.pk) == '[\n    "id"\n]'

    @pytest.mark.asyncio
    async def test_pk_values(self, bind):
        ids = list(range(1, 5))
        for i in ids:
            await Model.create(name=rand_str(length=25))
        assert sorted(await Model.pk.values) == sorted(ids)


@pytest.mark.asyncio
class TestAggregateProxy:
    @pytest.fixture
    async def seed_users(bind):
        for x in range(1, 6):
            await Model.create(**{"name": rand_str(min=3, max=25)})

    async def test_agg_repr(self):
        repr(Model.agg)

    async def test_pk_accessor(self):
        assert isinstance(Model.agg._pk, PrimaryKeyProxy)

    async def test_column_accessor(self):
        assert isinstance(Model.agg._c, ColumnProxy)

    async def test_agg_count(self, bind, seed_users):

        result = await Model.agg.count()
        assert result == 5

    async def test_agg_max_on_pk(self, bind, seed_users):
        result = await Model.agg.max()
        assert result == 5

    async def test_agg_min_on_pk(self, bind, seed_users):
        result = await Model.agg.min()
        assert result == 1

    @pytest.mark.parametrize("column", Model.c.names + Model.c.columns)
    async def test_agg_max(self, bind, seed_users, column):
        result = await Model.agg.max(column)
        assert result is not None

    @pytest.mark.parametrize("column", Model.c.names + Model.c.columns)
    async def test_agg_min(self, bind, seed_users, column):
        result = await Model.agg.min(column)
        assert result is not None
