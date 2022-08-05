from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import String
from sqlalchemy.sql.schema import Column

from car_rental_service.db.base import Base


class User(Base):
    """Model for user."""

    __tablename__: str = "users"

    name = Column(String(length=100), nullable=False)
    email = Column(String(length=30), nullable=False)
    mobile = Column(String(length=10))

    reservations = relationship(
        "Reservation",
        lazy="joined",
    )
