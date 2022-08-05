import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import ConnectionPool
from starlette import status


@pytest.mark.anyio
async def test_search(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
    fake_redis_pool: ConnectionPool,
) -> None:
    url = fastapi_app.url_path_for("search")
    response = await client.get(
        url,
        params={"start_date": "2022-08-10", "end_date": "2022-08-15"},
    )
    cars = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(cars) >= 1
