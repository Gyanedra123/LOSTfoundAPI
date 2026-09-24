from typing import List
from sqlmodel import Session, select
from t1_models import Item, ItemBase, ItemUpdate, ItemStatus

def create_lost_found_item(session: Session, item_data: ItemBase) -> Item:
    db_item = Item.from_orm(item_data)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


def get_all_items(session: Session, offset: int = 0, limit: int = 100) -> List[Item]:
    return session.exec(select(Item).offset(offset).limit(limit)).all()

# 
def get_item_by_id(session: Session, item_id: int) -> Item:
    return session.get(Item, item_id)


def update_item_details(session: Session, db_item: Item, item_update: ItemUpdate) -> Item:
    update_data = item_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


def delete_item_by_id(session: Session, db_item: Item):
    session.delete(db_item)
    session.commit()


def get_items_by_status(session: Session, status: ItemStatus) -> List[Item]:
    return session.exec(select(Item).where(Item.status == status)).all()


def get_items_by_category(session: Session, category: str) -> List[Item]:
    return session.exec(select(Item).where(Item.category == category)).all()
