from car_rental_service.web.api.reservation.schema import (
    ReservationInputDTO,
)


CREATE_RESERVATION_PAYLOAD = ReservationInputDTO(
    car_id=1,
    user_id=1,
    start_date="2022-08-10",
    end_date="2022-08-15",
)
