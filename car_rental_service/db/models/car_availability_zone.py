from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String

from car_rental_service.db.base import Base


class CarAvailabilityZone(Base):
    """Model for car availability zone."""

    __tablename__: str = "car_availability_zones"

    name = Column(String(length=24), nullable=False)
