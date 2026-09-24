from pydantic import EmailStr
from sqlmodel import SQLModel


class EventCreate(SQLModel):
    title: str
    venue: str
    capacity: int
    organizer: str
    status: str = "Open"


class EventUpdate(SQLModel):
    title: str | None = None
    venue: str | None = None
    capacity: int | None = None
    organizer: str | None = None
    status: str | None = None


class ReservationCreate(SQLModel):
    student_name: str
    roll_number: str
    email: EmailStr