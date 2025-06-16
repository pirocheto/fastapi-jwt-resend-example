from typing import Any, Protocol, TypeVar, runtime_checkable

from app.domain.models.base import DomainModel
from app.infrastructure.db.models import Base


@runtime_checkable
class DataclassProtocol(Protocol):
    __dataclass_fields__: dict[str, Any]


DType = TypeVar("DType", bound=DomainModel)
OType = TypeVar("OType", bound=Base)
