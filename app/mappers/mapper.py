from typing import TypeVar

from app.domain.models.base import DomainModel
from app.infrastructure.db.models import Base

DType = TypeVar("DType", bound=DomainModel)
OType = TypeVar("OType", bound=Base)  # ORM : SQLAlchemy


def domain_to_orm(model_obj: DType, orm_class: type[OType]) -> OType:
    model_fields = set(model_obj.__dataclass_fields__.keys())
    orm_fields = set(orm_class.__table__.columns.keys())
    common_fields = model_fields & orm_fields

    data = {field: getattr(model_obj, field) for field in common_fields}
    return orm_class(**data)


def orm_to_domain(orm_obj: OType, model_class: type[DType]) -> DType:
    orm_fields = set(orm_obj.__table__.columns.keys())
    model_fields = set(model_class.__dataclass_fields__.keys())
    common_fields = orm_fields & model_fields

    data = {field: getattr(orm_obj, field) for field in common_fields}
    return model_class(**data)
