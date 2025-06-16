"""Mapper module for converting between domain models and ORM models."""

from app.infrastructure.mappers.types import DType, OType


def domain_to_orm(model_obj: DType, orm_class: type[OType]) -> OType:
    """Convert a domain model to an ORM model."""

    model_fields = set(model_obj.__dataclass_fields__.keys())
    orm_fields = set(orm_class.__table__.columns.keys())
    common_fields = model_fields & orm_fields

    data = {field: getattr(model_obj, field) for field in common_fields}
    return orm_class(**data)


def orm_to_domain(orm_obj: OType, model_class: type[DType]) -> DType:
    """Convert an ORM model to a domain model."""

    orm_fields = set(orm_obj.__table__.columns.keys())
    model_fields = set(model_class.__dataclass_fields__.keys())
    common_fields = orm_fields & model_fields

    data = {field: getattr(orm_obj, field) for field in common_fields}
    return model_class(**data)
