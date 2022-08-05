from datetime import date, datetime
from typing import List
from fastapi import Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from car_rental_service.db.dependencies import get_db_session
from car_rental_service.schema import ReservationStatus
from car_rental_service.db.models.reservation import Reservation
from car_rental_service.db.models.car import Car


class CarDAO:
    """Class for doing operations on car model."""

    def __init__(
        self,
        session: AsyncSession = Depends(get_db_session),
    ) -> None:
        self.session = session

    async def get_available_cars(
        self,
        start_date: str,
        end_date: str,
        car_id: int = None,
    ) -> List[Car]:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        reserved_cars: List[int] = await self.get_reserved_cars(
            start_date,
            end_date,
            car_id,
        )

        query = select(Car).where(Car.id.not_in(reserved_cars))
        rows = await self.session.execute(query)
        return rows.scalars().unique().fetchall()

    async def get_reserved_cars(
        self,
        start_date: date,
        end_date: date,
        car_id: int = None,
    ) -> List[int]:
        reservations_query = select(Reservation).where(
            Reservation.start_date == start_date,
            Reservation.end_date == end_date,
            Reservation.status == ReservationStatus.success.value,
        )
        if car_id:
            reservations_query = reservations_query.where(Reservation.car_id == car_id)

        reservation_rows = await self.session.execute(reservations_query)
        return [
            reservation.car_id
            for reservation in reservation_rows.columns("car_id").fetchall()
        ]
