from sqlalchemy.sql.sqltypes import String
from sqlalchemy.sql.schema import Column

from car_rental_service.db.base import Base


class Category(Base):
    """Model for all car categories."""

    __tablename__: str = "categories"

    name = Column(String(length=20), nullable=False)
