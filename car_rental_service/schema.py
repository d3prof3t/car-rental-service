from enum import Enum


class ReservationStatus(str, Enum):
    success = "SUCCESS"
    cancelled = "CANCELLED"
    processing = "PROCESSING"
