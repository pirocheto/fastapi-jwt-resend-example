from dataclasses import dataclass
from typing import Any, TypeVar

from app.infrastructure.db.models import Base

OrmT = TypeVar("OrmT", bound=Base)


@dataclass
class DomainModel:
    """
    Base class for domain models.
    This class can be extended by other domain models to inherit common properties or methods.
    """

    @property
    def __dataclass_fields__(self) -> dict[str, Any]:
        raise NotImplementedError()

    def to_orm(self) -> Base:
        """Convert the domain model to an ORM model."""
        raise NotImplementedError()
