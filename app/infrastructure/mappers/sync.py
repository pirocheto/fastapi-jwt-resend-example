from app.infrastructure.mappers.types import DType, OType


def domain_from_orm(domain_obj: DType, orm_obj: OType) -> DType:
    """Synchronise les champs communs de l'objet ORM vers l'objet métier, en place."""
    domain_fields = set(domain_obj.__dataclass_fields__.keys())
    orm_fields = set(orm_obj.__table__.columns.keys())
    common_fields = domain_fields & orm_fields

    for field in common_fields:
        setattr(domain_obj, field, getattr(orm_obj, field))

    return domain_obj
