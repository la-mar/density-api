# flake8: noqa isort:skip_file
from starlette.config import environ

# inject environment variables prior to first import
environ["TESTING"] = "True"
environ["DATABASE_NAME"] = "testing"
environ["LOG_LEVEL"] = "30"

import os

import gino
import pytest
import sqlalchemy
from async_asgi_testclient import TestClient
from sqlalchemy_utils import create_database, database_exists, drop_database

import config
from db import db
from density.main import app
from util.jsontools import load_json
import tests.utils as testutils


ECHO = False

pytest.mark.cionly = pytest.mark.skipif(
    not testutils.to_bool(os.getenv("CI")), reason="run on CI only",
)

url = config.ALEMBIC_CONFIG.url

if not database_exists(url):
    create_database(url)


@pytest.fixture(scope="session")
def sa_engine():
    url = config.ALEMBIC_CONFIG.url

    if database_exists(url):
        drop_database(url)
    create_database(url)

    rv = sqlalchemy.create_engine(url, echo=ECHO)
    db.create_all(rv)  # create tables
    yield rv
    db.drop_all(rv)  # undo all that hard work you did
    rv.dispose()


@pytest.fixture
async def engine(sa_engine):
    db.create_all(sa_engine)
    e = await gino.create_engine(config.DATABASE_CONFIG.url, echo=ECHO)
    yield e
    await e.close()
    db.drop_all(sa_engine)


@pytest.fixture
async def bind(sa_engine):
    db.create_all(sa_engine)
    async with db.with_bind(config.DATABASE_CONFIG.url, echo=ECHO) as e:
        yield e
    db.drop_all(sa_engine)


@pytest.fixture
def conf():
    yield config


@pytest.fixture
async def client(bind) -> TestClient:
    yield TestClient(app)


# --- json fixtures ---------------------------------------------------------- #


@pytest.fixture(scope="session")
def json_fixture():
    yield lambda x: load_json(f"tests/fixtures/{x}")
