from sqlalchemy import Boolean, Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship

class Role(Base):
    __tablename__= "role"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, index=True)
    descripcion = Column(String(200), index=True)