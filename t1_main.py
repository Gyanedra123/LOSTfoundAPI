from typing import List
from fastapi import FastAPI, HTTPException, status
from sqlmodel import SQLModel, Session
from t1_database import engine
import t1_crud
from t1_models import Item, ItemBase, ItemUpdate, ItemStatus

app = FastAPI(
    title="Campus Lost & Found API (Task 1)",
    description="Multi-file robust architecture using FastAPI and SQLModel.",
    version="1.0.0"
)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

def get_db_session():
    with Session(engine) as session:
        yield session

# 1. POST /items — 
@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemBase):
    session = next(get_db_session())
    return t1_crud.create_lost_found_item(session, item)

# 2. GET /items —
@app.get("/items", response_model=List[Item])
def read_items(offset: int = 0, limit: int = 100):
    session = next(get_db_session())
    return t1_crud.get_all_items(session, offset, limit)

# 3. GET /items/{item_id} —
@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    session = next(get_db_session())
    db_item = t1_crud.get_item_by_id(session, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail=f"Item with ID {item_id} not found")
    return db_item

# 4. PUT /items/{item_id} —
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item_update: ItemUpdate):
    session = next(get_db_session())
    db_item = t1_crud.get_item_by_id(session, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail=f"Item with ID {item_id} not found")
    return t1_crud.update_item_details(session, db_item, item_update)

# 5. DELETE /items/{item_id} — 
@app.delete("/items/{item_id}", status_code=status.HTTP_200_OK)
def delete_item(item_id: int):
    session = next(get_db_session())
    db_item = t1_crud.get_item_by_id(session, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail=f"Item with ID {item_id} not found")
    t1_crud.delete_item_by_id(session, db_item)
    return {"message": f"Successfully deleted item report {item_id}"}

# 6. GET /items/status/{status} — 
@app.get("/items/status/{status}", response_model=List[Item])
def read_items_by_status(status: ItemStatus):
    session = next(get_db_session())
    return t1_crud.get_items_by_status(session, status)

# 7. GET /items/category/{category} — 
@app.get("/items/category/{category}", response_model=List[Item])
def read_items_by_category(category: str):
    session = next(get_db_session())
    return t1_crud.get_items_by_category(session, category)
