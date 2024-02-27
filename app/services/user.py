from typing import Type
from sqlalchemy.orm import Session, joinedload
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.auth import encrypt_password
from app.services.role import get_role_by_name

def get_user_by_email(email: str, db: Session):
    return db.query(User).filter_by(email=email).options(
        joinedload(User.roles)
    ).first()

def create_user(user: UserCreate, db: Session):
    db_user = User(email=user.email, hashed_password=encrypt_password(user.password), full_name=user.full_name)
    role = get_role_by_name(name="Usuario", db=db)
    if role:
        db_user.roles.append(role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(user: UserUpdate, user_id: int, db: Session):
    user_bd = get_user(user_id, db=db)
    if user_bd is None:
        return user_bd
    user_bd.email = user.emailuser_bd.full_name = user.full_name
    db.commit()
    db.refresh(user_bd)
    return user_bd

def delete_user(user_id: int, db: Session):
    user_bd = get_user(user_id, db=db)
    if user_bd is None:
        return user_bd
    db.delete(user_bd)
    db.commit()
    return {"message": "Usuario eliminado"}
    
def get_user(user_id: int, db: Session) -> Type[User] | None:
    return db.query(User).filter_by(id= user_id).first()