from typing import List
from pydantic import UUID4, BaseModel
import uuid

class DishCreate(BaseModel):
    title: str
    description: str
    price: float

class DishGet(DishCreate):
    id: uuid.UUID
    submenu_id: uuid.UUID
    
    class Config:
        from_attributes = True


class SubmenuCreate(BaseModel):
    title: str
    description: str

class SubmenuGet(SubmenuCreate):
    id: uuid.UUID
    menu_id: uuid.UUID
    dishes: List[DishGet]

    class Congig:
        from_attributes = True


class MenuCreate(BaseModel):
    title: str
    description: str

class MenuGet(MenuCreate):
    id: uuid.UUID
    
    submenus_count: int

    class Congig:
        from_attributes = True

        