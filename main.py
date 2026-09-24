from fastapi import FastAPI, Depends
from sqlmodel import Session

from database import create_db_and_tables, get_session
from schemas import EventCreate, EventUpdate, ReservationCreate
from crud import (
    create_event,
    get_events,
    get_event,
    update_event,
    delete_event,
    create_reservation,
    get_reservations,
    delete_reservation,
    get_availability
)


app = FastAPI(
    title="College Event Reservation API",
    description="API for managing college events and student reservations",
    version="1.0.0"
)


@app.on_event("startup")
def startup():
    create_db_and_tables()


@app.post("/events")
def post_event(
    event_data: EventCreate,
    session: Session = Depends(get_session)
):
    return create_event(session, event_data)


@app.get("/events")
def read_events(
    session: Session = Depends(get_session)
):
    return get_events(session)


@app.get("/events/{event_id}")
def read_event(
    event_id: int,
    session: Session = Depends(get_session)
):
    return get_event(session, event_id)


@app.put("/events/{event_id}")
def put_event(
    event_id: int,
    event_data: EventUpdate,
    session: Session = Depends(get_session)
):
    return update_event(session, event_id, event_data)


@app.delete("/events/{event_id}")
def remove_event(
    event_id: int,
    session: Session = Depends(get_session)
):
    return delete_event(session, event_id)


@app.post("/events/{event_id}/reserve")
def reserve_event(
    event_id: int,
    reservation_data: ReservationCreate,
    session: Session = Depends(get_session)
):
    return create_reservation(
        session,
        event_id,
        reservation_data
    )


@app.get("/events/{event_id}/reservations")
def read_reservations(
    event_id: int,
    session: Session = Depends(get_session)
):
    return get_reservations(session, event_id)


@app.delete("/reservations/{reservation_id}")
def cancel_reservation(
    reservation_id: int,
    session: Session = Depends(get_session)
):
    return delete_reservation(session, reservation_id)


@app.get("/events/{event_id}/availability")
def event_availability(
    event_id: int,
    session: Session = Depends(get_session)
):
    return get_availability(session, event_id)