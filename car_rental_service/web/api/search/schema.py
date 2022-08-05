from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class SearchOutputDTO(BaseModel):
    """DTO for reservation.

    It returned when accessing reservation(s)
    """

    id: int
    uuid: UUID
    created_at: datetime
    updated_at: datetime
    name: str
    brand: str
    registered_number: str
    category_id: int

    class Config:
        orm_mode = True
        use_enum_values = True
