import uuid
from sqlalchemy import Column, ForeignKey, String, Integer, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from .database import Base

class Menu(Base):
    __tablename__ = 'menus'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, nullable=False,
                default=uuid.uuid4)
    title = Column(String, index=True)
    description = Column(String, index=True)
    
    submenus = relationship('Submenu', back_populates='menu', cascade='all, delete')

class Submenu(Base):
    __tablename__ = 'submenus'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, nullable=False,
                default=uuid.uuid4) 
    title = Column(String, index=True)
    description = Column(String, index=True)
    menu_id = Column(UUID(as_uuid=True), ForeignKey('menus.id'))
    
    menu = relationship('Menu', back_populates='submenus')
    dishes = relationship('Dish', back_populates='submenu', cascade='all, delete')

class Dish(Base):
    __tablename__ = 'dishes'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, nullable=False,
                default=uuid.uuid4)
    title = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float(precision=2), index=True)
    submenu_id = Column(UUID(as_uuid=True), ForeignKey('submenus.id'))
    
    submenu = relationship('Submenu', back_populates='dishes')
