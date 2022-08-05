from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import String, Integer
from sqlalchemy.sql.schema import Column, ForeignKey

from car_rental_service.db.base import Base


# **NOTE**: Moved the below `Car` model in the same module as `Reservation`
# as both need to load in a specific order


class Car(Base):
    """Model for master car repository."""

    __tablename__: str = "cars"

    name = Column(String(length=100), nullable=False)
    brand = Column(String(length=50), nullable=False)
    registered_number = Column(String(length=12), nullable=False)

    # foregin relations
    category_id = Column(Integer, ForeignKey("categories.id"))
    reservations = relationship(
        "Reservation",
    )
