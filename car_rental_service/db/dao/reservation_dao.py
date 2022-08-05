from time import sleep
from typing import List
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import ConnectionPool, Redis

from car_rental_service.db.dependencies import get_db_session
from car_rental_service.db.models.reservation import Reservation
from car_rental_service.services.redis.dependency import get_redis_pool
from car_rental_service.schema import ReservationStatus
from car_rental_service.web.api.reservation.schema import (
    ReservationInputDTO,
    ReservationOutputDTO,
)
from car_rental_service.web.exceptions import (
    CarIsLockedForReservation,
    ReservationAlreadyExist,
)


class ReservationDAO:
    """Class for doing operations on reservation model."""

    def __init__(
        self,
        session: AsyncSession = Depends(get_db_session),
        redis_pool: ConnectionPool = Depends(get_redis_pool),
    ) -> None:
        self.session = session
        self.redis_pool = redis_pool

    async def create_reservation(
        self,
        row: ReservationInputDTO,
    ) -> ReservationOutputDTO:
        """Create a car reservation for a given date slot

        Args:
            row (ReservationInputDTO): _description_
        """
        does_reservation_exists = await self.does_reservation_exists(
            row.user_id,
            row.car_id,
            row.start_date,
            row.end_date,
        )
        if does_reservation_exists:
            raise ReservationAlreadyExist()

        is_car_selection_locked = await self.is_car_selection_locked(
            row.user_id,
            row.car_id,
            row.start_date,
            row.end_date,
        )
        if is_car_selection_locked:
            raise CarIsLockedForReservation()
        else:
            await self.lock_car_selection(
                row.user_id,
                row.car_id,
                row.start_date,
                row.end_date,
            )

        await self.make_payment()

        reservation_row = Reservation(
            user_id=row.user_id,
            car_id=row.car_id,
            start_date=row.start_date,
            end_date=row.end_date,
            status=ReservationStatus.success,
        )

        self.session.add(reservation_row)
        await self.session.flush()
        await self.release_car_selection_lock(
            row.user_id,
            row.car_id,
            row.start_date,
            row.end_date,
        )

        return reservation_row

    async def make_payment(self) -> None:
        """
        **NOTE** mocking the payment flow and assuming it
        takes 300 ms for the round trip
        """
        sleep(0.3)

    async def does_reservation_exists(
        self,
        user_id: int,
        car_id: str,
        start_date: str,
        end_date: str,
    ) -> bool:
        """Does the reservation already exists for the given car and date slots.

        Args:
            car_id (UUID): Unique identifier for the car
            start_date (str): Start date
            end_date (str): End date

        Returns:
            bool: Signifies if the reservation is already made for
            the given car and date slots
        """
        query = select(Reservation).where(
            Reservation.user_id == user_id,
            Reservation.car_id == car_id,
            Reservation.start_date == start_date,
            Reservation.end_date == end_date,
        )
        rows = await self.session.execute(query)
        resp = rows.scalars().one_or_none()
        return True if resp else False

    async def lock_car_selection(
        self,
        user_id: int,
        car_id: int,
        start_date: str,
        end_date: str,
    ):
        lock_key = f"{user_id}_{car_id}_{start_date}_{end_date}"
        async with Redis(connection_pool=self.redis_pool) as redis:
            await redis.set(lock_key, 1, ex=300)

    async def release_car_selection_lock(
        self,
        user_id: int,
        car_id: int,
        start_date: str,
        end_date: str,
    ):
        lock_key = f"{user_id}_{car_id}_{start_date}_{end_date}"
        async with Redis(connection_pool=self.redis_pool) as redis:
            await redis.delete(lock_key)

    async def is_car_selection_locked(
        self,
        user_id: int,
        car_id: int,
        start_date: str,
        end_date: str,
    ) -> bool:
        """Check if a customer is already about to make payment for the same car
        and on the same date intervals.

        Args:
            car_id (UUID): Unique identifier of the car
            start_date (str): Start date of the reservation
            end_date (str): End date of the reservation

        Returns:
            bool: Signifies if the selected car and date slots are not
            already selected and pending for payment
        """
        lock_key = f"{user_id}_{car_id}_{start_date}_{end_date}"
        is_lock_exists = False
        async with Redis(connection_pool=self.redis_pool) as redis:
            is_lock_exists = True if await redis.get(lock_key) else False

        return is_lock_exists

    async def get_all_reservation(self, limit: int, offset: int) -> List[Reservation]:
        """Get all reservations.

        Args:
            limit (int): limit of records to fetch
            offset (int): fetching records after a particular number in the sorted order

        Returns:
            List[Reservation]: List of all reservation records
        """
        reservations = await self.session.execute(
            select(Reservation).limit(limit).offset(offset),
        )
        return reservations.scalars().fetchall()

    async def get_reservation_by_id(self, reservation_id: str) -> Reservation:
        """Get reservation by id.

        Args:
            reservation_id (UUID): unique identifier for a reservation

        Returns:
            Reservation: Reservation record
        """
        query = select(Reservation).where(Reservation.id == reservation_id)
        rows = await self.session.execute(query)
        return rows.scalars().fetch()
