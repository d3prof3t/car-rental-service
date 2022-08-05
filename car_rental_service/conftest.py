from typing import Any, AsyncGenerator

import pytest
from fakeredis import FakeServer
from fakeredis.aioredis import FakeConnection
from fastapi import FastAPI
from httpx import AsyncClient
from redis.asyncio import ConnectionPool
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from car_rental_service.db.dependencies import get_db_session
from car_rental_service.db.utils import create_database, drop_database
from car_rental_service.services.redis.dependency import get_redis_pool
from car_rental_service.settings import settings
from car_rental_service.web.application import get_app


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Backend for anyio pytest plugin.

    :return: backend name.
    """
    return "asyncio"


@pytest.fixture(scope="session")
async def _engine() -> AsyncGenerator[AsyncEngine, None]:
    """
    Create engine and databases.

    :yield: new engine.
    """
    from car_rental_service.db.meta import meta  # noqa: WPS433
    from car_rental_service.db.models import load_all_models  # noqa: WPS433

    load_all_models()

    await create_database()

    engine = create_async_engine(str(settings.db_url))
    async with engine.begin() as conn:
        await conn.run_sync(meta.create_all)

    try:
        yield engine
    finally:
        await engine.dispose()
        await drop_database()


@pytest.fixture
async def dbsession(
    _engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    """
    Get session to database.

    Fixture that returns a SQLAlchemy session with a SAVEPOINT, and the rollback to it
    after the test completes.

    :param _engine: current engine.
    :yields: async session.
    """
    connection = await _engine.connect()
    trans = await connection.begin()

    session_maker = sessionmaker(
        connection,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    session = session_maker()

    try:
        await setup_db(session)
        yield session
    finally:
        await session.close()
        await trans.rollback()
        await connection.close()


@pytest.fixture
async def fake_redis_pool() -> AsyncGenerator[ConnectionPool, None]:
    """
    Get instance of a fake redis.

    :yield: FakeRedis instance.
    """
    server = FakeServer()
    server.connected = True
    pool = ConnectionPool(connection_class=FakeConnection, server=server)

    yield pool

    await pool.disconnect()


async def setup_db(dbsession: AsyncSession):
    await dbsession.execute(
        """
        INSERT INTO "public"."car_availability_zones" ("id", "uuid", "created_at", "updated_at", "is_active", "name") VALUES
        (1, '10f10b20-6a74-49f4-b61a-e469f16c3b48', '2022-08-04 22:33:50.886581', '2022-08-04 22:33:50.886581', 't', 'Zone A'),
        (2, 'dc8437ee-f466-457c-9374-5f39cbe51701', '2022-08-04 22:33:50.886581', '2022-08-04 22:33:50.886581', 't', 'Zone B'),
        (3, '580e5b94-aaac-49ea-bf99-d889e08cb319', '2022-08-04 22:33:50.886581', '2022-08-04 22:33:50.886581', 't', 'Zone C'),
        (4, '504a3f31-6f2c-4755-ab61-db7ebe05b1c0', '2022-08-04 22:33:50.886581', '2022-08-04 22:33:50.886581', 't', 'Zone D');
        """,
    )
    await dbsession.execute(
        """
        INSERT INTO "public"."categories" ("id", "uuid", "created_at", "updated_at", "is_active", "name") VALUES
        (1, 'a341c07d-706b-44a2-bcbf-cee47749e7d2', '2022-08-04 22:34:59.317978', '2022-08-04 22:34:59.317978', 't', 'Sedan'),
        (2, 'cb877048-9fd1-457a-b7ce-cac8c94eb6f4', '2022-08-04 22:34:59.317978', '2022-08-04 22:34:59.317978', 't', 'SUV'),
        (3, 'eb7ff701-1677-4cfc-98a1-aec10ff9370e', '2022-08-04 22:34:59.317978', '2022-08-04 22:34:59.317978', 't', 'Hatchback');
        """,
    )
    await dbsession.execute(
        """
        INSERT INTO "public"."cars" ("id", "uuid", "created_at", "updated_at", "is_active", "name", "brand", "registered_number", "category_id") VALUES
        (1, '754bb404-90a9-423c-b512-513f25374eb0', '2022-08-04 22:36:55.150335', '2022-08-04 22:36:55.150335', 't', 'Car A', 'Brand A', 'HR26AZ1234', 1),
        (2, '5bf40d50-d32b-4019-806b-8ec4b83c6764', '2022-08-04 22:36:55.150335', '2022-08-04 22:36:55.150335', 't', 'Car B', 'Brand B', 'HR26AZ5678', 2),
        (3, '9d0aa319-8bbe-4ac7-955b-9271d15480b0', '2022-08-04 22:36:55.150335', '2022-08-04 22:36:55.150335', 't', 'Car C', 'Brand C', 'HR26AZ7891', 3);
        """,
    )

    await dbsession.execute(
        """
        INSERT INTO "public"."users" ("id", "uuid", "created_at", "updated_at", "is_active", "name", "email", "mobile") VALUES
        (1, 'a12be027-484c-42e0-a972-c3d0069d4a5d', '2022-08-05 03:04:17.427032', '2022-08-05 03:04:17.427032', 't', 'Saurabh Sharma', 'saurabhpysharma@gmail.com', '9654198036'),
        (2, '3d6ca315-5a0e-4a6d-b791-46eef1fca882', '2022-08-05 03:04:17.427032', '2022-08-05 03:04:17.427032', 't', 'Sammy', 'sammy@gmail.com', '9999999999'),
        (3, '372a7b8e-390c-4061-b8cc-4186c2da32ed', '2022-08-05 03:04:17.427032', '2022-08-05 03:04:17.427032', 't', 'John', 'john@gmail.com', '9999999991');
        """,
    )

    await dbsession.execute(
        """
        INSERT INTO "public"."reservations" ("id", "uuid", "created_at", "updated_at", "is_active", "car_id", "start_date", "end_date", "status", "user_id") VALUES
        (23, 'fcf85714-a228-4a0c-b128-cc0adcb1b43e', '2022-08-05 00:41:42.46016', '2022-08-05 00:41:42.46016', 't', 1, '2022-08-04', '2022-08-04', 'SUCCESS', 1),
        (24, 'fd5c5ee5-ddc5-422a-8bcf-7b131bca5f78', '2022-08-05 01:17:53.427526', '2022-08-05 01:17:53.427526', 't', 1, '2022-08-05', '2022-08-05', 'SUCCESS', 2);
        """,
    )


@pytest.fixture
def fastapi_app(
    dbsession: AsyncSession,
    fake_redis_pool: ConnectionPool,
) -> FastAPI:
    """
    Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.
    """
    application = get_app()
    application.dependency_overrides[get_db_session] = lambda: dbsession
    application.dependency_overrides[get_redis_pool] = lambda: fake_redis_pool
    return application  # noqa: WPS331


@pytest.fixture
async def client(
    fastapi_app: FastAPI,
    anyio_backend: Any,
) -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture that creates client for requesting server.

    :param fastapi_app: the application.
    :yield: client for the app.
    """
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac
