import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import ConnectionPool
from starlette import status

from car_rental_service.db.dao.reservation_dao import ReservationDAO
from car_rental_service.tests.payloads import CREATE_RESERVATION_PAYLOAD


@pytest.mark.anyio
async def test_health(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Checks the health endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    url = fastapi_app.url_path_for("health_check")
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.anyio
async def test_create_reservations(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
    fake_redis_pool: ConnectionPool,
) -> None:
    url = fastapi_app.url_path_for("create_reservation")
    response = await client.post(url, data=CREATE_RESERVATION_PAYLOAD.json())

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.anyio
async def test_get_reservations(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
    fake_redis_pool: ConnectionPool,
) -> None:
    dao = ReservationDAO(dbsession, fake_redis_pool)
    await dao.create_reservation(CREATE_RESERVATION_PAYLOAD)
    url = fastapi_app.url_path_for("get_reservations")
    response = await client.get(url)
    reservations = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(reservations) >= 1
