from uuid import UUID
from datetime import datetime, date

from pydantic import BaseModel

from car_rental_service.schema import ReservationStatus


class ReservationOutputDTO(BaseModel):
    """DTO for reservation.

    It returned when accessing reservation(s)
    """

    id: int
    uuid: UUID
    created_at: datetime
    updated_at: datetime
    car_id: int
    user_id: int
    start_date: date
    end_date: date
    status: ReservationStatus

    class Config:
        orm_mode = True
        use_enum_values = True


class ReservationInputDTO(BaseModel):
    """DTO for creating new reservation."""

    car_id: int
    user_id: int
    start_date: date
    end_date: date

    class Config:
        orm_mode = True


CREATE_RESERVATION_RESPONSE_SCHEMAS = {
    409: {
        "description": "Reservation already exists.",
        "content": {
            "application/json": {
                "message": "Reservation already exists.",
            },
        },
    },
    406: {
        "description": "Car is locked for reservation.",
        "content": {
            "application/json": {
                "message": "Car is locked for reservation.",
            },
        },
    },
    500: {
        "description": "Something went wrong.",
        "content": {
            "application/json": {
                "message": "Something went wrong.",
            },
        },
    },
}


GET_RESERVATION_RESPONSE_SCHEMAS = {
    500: {
        "description": "Something went wrong.",
        "content": {
            "application/json": {
                "message": "Something went wrong.",
            },
        },
    },
}
