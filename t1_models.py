from enum import Enum
from typing import Optional
from sqlmodel import Field, SQLModel


class ItemStatus(str, Enum):
    LOST = "Lost"
    FOUND = "Found"
    RETURNED = "Returned"
class ItemBase(SQLModel):
   
    title: str = Field(min_length=1, description="Title cannot be empty")

    description: str = Field(min_length=3, description="Must be a meaningful description")
    category: str = Field(index=True)
    location: str
    reported_by: str
    status: ItemStatus = Field(description="Must be Lost, Found, or Returned")


class Item(ItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ItemUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1)
    description: Optional[str] = Field(default=None, min_length=3)
    category: Optional[str] = None
    location: Optional[str] = None
    reported_by: Optional[str] = None
    status: Optional[ItemStatus] = None
