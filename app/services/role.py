from typing import Type
from sqlalchemy import Session
from app.models.role import Role

def  get_role_by_name(name: str, db: Session) -> Type[Role] | None:
    return db.query(Role).filter_by(nombre=name).first()