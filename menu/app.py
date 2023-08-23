import uuid
from fastapi import APIRouter, FastAPI, Depends, HTTPException
from typing import List
from pydantic import UUID4
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import joinedload

from . import schemas
from .database import SessionLocal
from . import models

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



'''ДЛЯ МЕНЮ'''

#Просматривает список меню
@app.get('/api/v1/menus')
async def menu_list(db: Session = Depends(get_db)):
    menu_list = db.query(models.Menu).all()
    #return [menu.target_menu_title for menu in menu_list]
    if menu_list:
        return menu_list
    else:
        return []
    '''else:
        raise HTTPException(status_code=404, detail=f'menu_list.title не найден')'''


#Просматривает определенное меню
@app.get('/api/v1/menus/{target_menu_id}') # , response_model=schemas.MenuGet
async def get_menu(target_menu_id: uuid.UUID, db: Session = Depends(get_db)):
    menu = db.query(models.Menu).options(joinedload(models.Menu.submenus)).filter(models.Menu.id == target_menu_id).first()
    submenus_count = db.query(models.Submenu).filter(models.Submenu.menu_id==target_menu_id).count()
    dish_count = db.query(func.count(models.Dish.id)).join(models.Dish.submenu).filter(models.Submenu.menu_id == target_menu_id).scalar()

    if menu:
        return {
            'title': menu.title,
            'description': menu.description,
            'id': menu.id,
            'submenus_count': submenus_count,
            'dish_count': dish_count,
        }
        

    else:
        raise HTTPException(status_code=404, detail=f'menu not found')
    

#Создает меню
@app.post('/api/v1/menus', status_code=201)
async def create_menu(menu: schemas.MenuCreate, db: Session = Depends(get_db)):
    new_menu = models.Menu(title=menu.title, description=menu.description)
    db.add(new_menu)
    db.commit()
    db.close()
    return new_menu

#Обновляет определенное меню
@app.patch('/api/v1/menus/{target_menu_id}')
async def update_menu(target_menu_id: uuid.UUID, schema: schemas.MenuCreate, db: Session = Depends(get_db)):
    menu = db.query(models.Menu).get(target_menu_id)

    if menu:
        menu.title = schema.title
        menu.description = schema.description
        db.commit()
        return menu

    elif not menu:
        raise HTTPException(status_code=404, detail=f'Объект с id {target_menu_id} не найден')
    db.close()
    

#Удаляет определенное меню
@app.delete('/api/v1/menus/{target_menu_id}')
async def delete_menu(target_menu_id: uuid.UUID, db: Session = Depends(get_db)):
    menu = db.query(models.Menu).get(target_menu_id)
    if menu:
        db.delete(menu)
        db.commit()
        db.close()
    elif not menu:
        raise HTTPException(status_code=404, detail=f'Объект с id {target_menu_id} не найден')


'''ДЛЯ МЕНЮ'''
############################################################################################################
'''ДЛЯ ПОДМЕНЮ'''

#Просматривает список подменю
@app.get('/api/v1/menus/{target_menu_id}/submenus')
async def submenu_list(target_menu_id: uuid.UUID, db: Session = Depends(get_db)):
    submenu_list = db.query(models.Submenu).filter(models.Submenu.menu_id == target_menu_id).all()
    if submenu_list:
        return submenu_list
    else:
        return []

#Просматривает определенное подменю
@app.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}')
async def get_submenu(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID, db: Session = Depends(get_db)):
    submenu = db.query(models.Submenu).filter(models.Submenu.id == target_submenu_id, models.Submenu.menu_id == target_menu_id).first()
    if submenu:
        return submenu
    elif not submenu:
        raise HTTPException(status_code=404, detail=f'submenu not found')
        #return []

#Создает подменю
@app.post('/api/v1/menus/{target_menu_id}/submenus', status_code=201)
async def create_submenu(target_menu_id: uuid.UUID, submenu: schemas.SubmenuCreate, db: Session = Depends(get_db)):
    new_submenu = models.Submenu(title=submenu.title, description=submenu.description, menu_id = target_menu_id)
    db.add(new_submenu)
    db.commit()
    db.close()
    return new_submenu

#Обновляет определенное подменю
@app.patch('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}')
async def update_submenu(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID, schema: schemas.SubmenuCreate, db: Session = Depends(get_db)):
    submenu = db.query(models.Submenu).filter(models.Submenu.id == target_submenu_id, models.Submenu.menu_id == target_menu_id).first()

    if submenu:
        submenu.title = schema.title # type: ignore
        submenu.description = schema.description # type: ignore
        db.commit()
    elif not submenu:
        raise HTTPException(status_code=404, detail=f'Объект с id {target_menu_id} не найден')
    db.close()
    return f'Название и описание изменены изменено'

#Удаляет определенное подменю
@app.delete('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}')
async def delete_submenu(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID, db: Session = Depends(get_db)):
    submenu = db.query(models.Submenu).filter(models.Submenu.id == target_submenu_id, models.Submenu.menu_id == target_menu_id).first()
    if submenu:
        db.delete(submenu)
        db.commit()
        db.close()
    elif not submenu:
        raise HTTPException(status_code=404, detail=f'Объект с id {target_menu_id} не найден')

    return f'Меню {submenu.title} удалено'

'''ДЛЯ ПОДМЕНЮ'''
############################################################################################################
'''ДЛЯ БЛЮД'''

#Просматривает список блюд
@app.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes')
async def dishes_list(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID, db: Session = Depends(get_db)):
    submenu = db.query(models.Submenu).filter(models.Submenu.id == target_submenu_id, models.Submenu.menu_id == target_menu_id).first()
    dishes_list = db.query(models.Dish).filter(models.Dish.submenu_id == target_submenu_id).all()
    
    return dishes_list
   

#Просматривает определенное блюдо
@app.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}', response_model=schemas.DishGet)
async def get_dish(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID, target_dish_id: uuid.UUID, db: Session = Depends(get_db)):
    submenu = db.query(models.Submenu).filter(models.Submenu.id == target_submenu_id, models.Submenu.menu_id == target_menu_id).first()
    dish = db.query(models.Dish).filter(models.Dish.id == target_dish_id, models.Dish.submenu_id == target_submenu_id).first()
    if submenu and dish:
        return dish
    elif not dish:
        raise HTTPException(status_code=404, detail=f'Объект не найден')

#Создает блюдо
@app.post('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes', status_code=201)
async def create_dish(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID, dish: schemas.DishCreate, db: Session = Depends(get_db)):
    submenu = db.query(models.Submenu).filter(models.Submenu.id == target_submenu_id, models.Submenu.menu_id == target_menu_id).first()
    if submenu:
        new_dish = models.Dish(title=dish.title, description=dish.description, submenu_id = target_submenu_id, price=dish.price)
        db.add(new_dish)
        db.commit()
        db.close()
        return "Объект создан"
    else: 
        raise HTTPException(status_code=404, detail=f'Объект не найден')
#Обновляет определенное блюдо
@app.patch('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}')
async def update_dish(target_menu_id: uuid.UUID, target_dish_id: uuid.UUID, target_submenu_id: uuid.UUID, title: str, description: str, db: Session = Depends(get_db)):
    submenu = db.query(models.Submenu).filter(models.Submenu.id == target_submenu_id, models.Submenu.menu_id == target_menu_id).first()
    dish = db.query(models.Dish).filter(models.Dish.id == target_dish_id, models.Dish.submenu_id == target_submenu_id).first()

    if dish and submenu:
        dish.target_dish_title = title
        dish.target_dish_description = description
        db.commit()
    elif not dish and submenu:
        raise HTTPException(status_code=404, detail=f'Объект не найден')
    db.close()
    return dish

#Удаляет определенное блюдо
@app.delete('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}')
async def delete_dish(target_menu_id: uuid.UUID, target_dish_id: uuid.UUID, target_submenu_id: uuid.UUID, db: Session = Depends(get_db)):
    submenu = db.query(models.Submenu).filter(models.Submenu.id == target_submenu_id, models.Submenu.menu_id == target_menu_id).first()
    dish = db.query(models.Dish).filter(models.Dish.id == target_dish_id, models.Dish.submenu_id == target_submenu_id).first()
    if dish and submenu:    
        db.delete(dish)
        db.commit()
        db.close()
    elif not dish:
        raise HTTPException(status_code=404, detail=f'Объект не найден')

    return f'Меню {dish.title} удалено'

'''ДЛЯ БЛЮД'''

