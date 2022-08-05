from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import String, Date, Integer
from sqlalchemy.sql.schema import Column, ForeignKey

from car_rental_service.db.base import Base


# class Car(Base):
#     """Model for master car repository."""

#     __tablename__: str = "cars"

#     name = Column(String(length=100), nullable=False)
#     brand = Column(String(length=50), nullable=False)
#     registered_number = Column(String(length=12), nullable=False)

#     # foregin relations
#     category_id = Column(Integer, ForeignKey("categories.id"))
#     reservations = relationship(
#         "Reservation",
#         lazy="joined",
#     )


# class User(Base):
#     """Model for user."""

#     __tablename__: str = "users"

#     name = Column(String(length=100), nullable=False)
#     email = Column(String(length=30), nullable=False)
#     mobile = Column(String(length=10))

#     reservations = relationship(
#         "Reservation",
#         lazy="joined",
#     )


class Reservation(Base):
    """Model for all car reservations made."""

    __tablename__: str = "reservations"

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String(length=10), nullable=False)

    # foreign relations
    car_id = Column(Integer, ForeignKey("cars.id"))
    user_id = Column(Integer, ForeignKey("users.id"))


car = relationship(
    "Car",
    back_populates="reservations",
    lazy="joined",
)
user = relationship(
    "User",
    back_populates="reservations",
    lazy="joined",
)
