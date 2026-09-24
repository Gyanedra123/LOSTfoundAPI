from fastapi import HTTPException
from sqlmodel import Session, select, func

from models import Event, Reservation
from schemas import EventCreate, EventUpdate, ReservationCreate


def create_event(session: Session, event_data: EventCreate):
    if event_data.capacity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Capacity must be greater than 0"
        )

    if event_data.status not in ["Open", "Closed"]:
        raise HTTPException(
            status_code=400,
            detail="Status must be Open or Closed"
        )

    event = Event.model_validate(event_data)

    session.add(event)
    session.commit()
    session.refresh(event)

    return event


def get_events(session: Session):
    return session.exec(select(Event)).all()


def get_event(session: Session, event_id: int):
    event = session.get(Event, event_id)

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    return event


def update_event(
    session: Session,
    event_id: int,
    event_data: EventUpdate
):
    event = session.get(Event, event_id)

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    if event_data.capacity is not None:
        if event_data.capacity <= 0:
            raise HTTPException(
                status_code=400,
                detail="Capacity must be greater than 0"
            )

        booked = session.exec(
            select(func.count(Reservation.id))
            .where(Reservation.event_id == event_id)
        ).one()

        if event_data.capacity < booked:
            raise HTTPException(
                status_code=400,
                detail="Capacity cannot be less than already booked seats"
            )

    if event_data.status is not None:
        if event_data.status not in ["Open", "Closed"]:
            raise HTTPException(
                status_code=400,
                detail="Status must be Open or Closed"
            )

    update_data = event_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(event, key, value)

    session.add(event)
    session.commit()
    session.refresh(event)

    return event


def delete_event(session: Session, event_id: int):
    event = session.get(Event, event_id)

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    reservations = session.exec(
        select(Reservation)
        .where(Reservation.event_id == event_id)
    ).all()

    for reservation in reservations:
        session.delete(reservation)

    session.delete(event)
    session.commit()

    return {"message": "Event deleted successfully"}


def create_reservation(
    session: Session,
    event_id: int,
    reservation_data: ReservationCreate
):
    event = session.get(Event, event_id)

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    if event.status != "Open":
        raise HTTPException(
            status_code=400,
            detail="Event is closed"
        )

    booked = session.exec(
        select(func.count(Reservation.id))
        .where(Reservation.event_id == event_id)
    ).one()

    if booked >= event.capacity:
        raise HTTPException(
            status_code=400,
            detail="Event is full. No seats available"
        )

    if not reservation_data.student_name.strip():
        raise HTTPException(
            status_code=400,
            detail="Student name cannot be empty"
        )

    reservation = Reservation(
        event_id=event_id,
        student_name=reservation_data.student_name.strip(),
        roll_number=reservation_data.roll_number,
        email=reservation_data.email
    )

    session.add(reservation)
    session.commit()
    session.refresh(reservation)

    return reservation


def get_reservations(session: Session, event_id: int):
    event = session.get(Event, event_id)

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    return session.exec(
        select(Reservation)
        .where(Reservation.event_id == event_id)
    ).all()


def delete_reservation(session: Session, reservation_id: int):
    reservation = session.get(Reservation, reservation_id)

    if not reservation:
        raise HTTPException(
            status_code=404,
            detail="Reservation not found"
        )

    session.delete(reservation)
    session.commit()

    return {"message": "Reservation cancelled successfully"}


def get_availability(session: Session, event_id: int):
    event = session.get(Event, event_id)

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    booked = session.exec(
        select(func.count(Reservation.id))
        .where(Reservation.event_id == event_id)
    ).one()

    remaining = event.capacity - booked

    return {
        "capacity": event.capacity,
        "booked": booked,
        "remaining": remaining
    }