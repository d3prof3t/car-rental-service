from typing import List

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.param_functions import Depends

from car_rental_service.db.dao.reservation_dao import ReservationDAO
from car_rental_service.db.models.reservation import Reservation
from car_rental_service.web.api.reservation.schema import (
    CREATE_RESERVATION_RESPONSE_SCHEMAS,
    GET_RESERVATION_RESPONSE_SCHEMAS,
    ReservationInputDTO,
    ReservationOutputDTO,
)
from car_rental_service.web.exceptions import (
    CarIsLockedForReservation,
    ReservationAlreadyExist,
)

router = APIRouter()


@router.get(
    "/",
    response_model=List[ReservationOutputDTO],
    responses=GET_RESERVATION_RESPONSE_SCHEMAS,
)
async def get_reservations(
    limit: int = 10,
    offset: int = 0,
    reservation_dao: ReservationDAO = Depends(),
) -> List[Reservation]:
    """
    Retrieve all dummy objects from the database.

    :param limit: limit of dummy objects, defaults to 10.
    :param offset: offset of dummy objects, defaults to 0.
    :param dummy_dao: DAO for dummy models.
    :return: list of dummy obbjects from database.
    """
    return await reservation_dao.get_all_reservation(limit=limit, offset=offset)


@router.post(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=CREATE_RESERVATION_RESPONSE_SCHEMAS,
)
async def create_reservation(
    new_reservation_object: ReservationInputDTO,
    reservation_dao: ReservationDAO = Depends(),
) -> None:
    """Create new reservation.

    Args:
        new_reservation_object (ReservationInputDTO): _description_
        reservation_dao (ReservationDAO): _description_

    Returns:
        : _description_
    """
    try:
        resp = await reservation_dao.create_reservation(new_reservation_object)
        headers = {"X-Location-Id": str(resp.id)}
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, headers=headers)
    except ReservationAlreadyExist as reservation_already_exists:
        return JSONResponse(
            status_code=reservation_already_exists.status_code,
            content={"message": reservation_already_exists.message},
        )
    except CarIsLockedForReservation as car_is_locked_for_reservation:
        return JSONResponse(
            status_code=car_is_locked_for_reservation.status_code,
            content={"message": car_is_locked_for_reservation.message},
        )
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Something went wrong."},
        )
