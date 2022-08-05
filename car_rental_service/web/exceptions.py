import logging
from fastapi import status


class CustomException(Exception):
    """wrapper for all custom exceptions"""

    def __init__(self, message=None, status_code=None, payload=None, handled=True):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload
        self.handled = handled
        if not self.handled:
            self.log()

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv

    def log(self):
        logging.getLogger(__name__).error(self.message, exc_info=True)


class ReservationAlreadyExist(CustomException):
    def __init__(self):
        self.message = "Reservation already exists."
        self.status_code = status.HTTP_409_CONFLICT
        super().__init__(self.message, self.status_code)


class CarIsLockedForReservation(CustomException):
    def __init__(self):
        self.message = "Car is locked for reservation."
        self.status_code = status.HTTP_406_NOT_ACCEPTABLE
        super().__init__(self.message, self.status_code)
