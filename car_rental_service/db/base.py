from uuid import uuid4

from sqlalchemy import Integer, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import as_declarative
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Boolean, DateTime

from car_rental_service.db.meta import meta


@as_declarative(metadata=meta)
class Base:
    """
    Base for all models.

    It has some type definitions to
    enhance autocompletion.
    """

    __tablename__: str

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    uuid = Column(UUID(as_uuid=True), nullable=False, unique=True, default=uuid4)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, server_default=text("True"), nullable=False)

    def to_dict(self):
        """Utility to convert a row to a dict."""
        row = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            row[column.name] = value
        return row

    def json_dict(self):
        """Returns a dict representation of the row.

        Returns:
            dict: dictionary representation of the object
        """
        return self.to_dict()
