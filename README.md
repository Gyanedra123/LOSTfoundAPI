# College Event Reservation API

## Project Description

This project is a FastAPI REST API for managing college events and student reservations. It allows users to create events, view and update events, reserve seats, check availability, and cancel reservations.

The API prevents overbooking and does not allow reservations for closed events.

## Technologies Used

* Python
* FastAPI
* SQLModel
* SQLite
* Uvicorn
* Pydantic

## Project Structure

```text
task2/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── crud.py
├── requirements.txt
├── README.md
└── events.db
```

## Installation

1. Open the project folder in the terminal.

2. Install the required packages:

```bash
python -m pip install -r requirements.txt
```

3. Run the FastAPI application:

```bash
python -m uvicorn main:app --reload
```

## Swagger UI

Open the following URL in your browser:

```text
http://127.0.0.1:8000/docs
```

Swagger UI can be used to test all API endpoints.

## Database

The application uses SQLite for storing events and reservations.

SQLModel is used for database models and operations. The database tables are automatically created when the application starts.

## API Endpoints

### Event APIs

| Method | Endpoint             | Description          |
| ------ | -------------------- | -------------------- |
| POST   | `/events`            | Create a new event   |
| GET    | `/events`            | Get all events       |
| GET    | `/events/{event_id}` | Get a specific event |
| PUT    | `/events/{event_id}` | Update an event      |
| DELETE | `/events/{event_id}` | Delete an event      |

### Reservation APIs

| Method | Endpoint                          | Description                   |
| ------ | --------------------------------- | ----------------------------- |
| POST   | `/events/{event_id}/reserve`      | Create a reservation          |
| GET    | `/events/{event_id}/reservations` | Get reservations for an event |
| DELETE | `/reservations/{reservation_id}`  | Cancel a reservation          |
| GET    | `/events/{event_id}/availability` | Check seat availability       |

## Business Logic

* Event capacity must be greater than 0.
* Student name cannot be empty.
* Email must be valid.
* A reservation can only be created for an existing event.
* Reservations are allowed only when the event status is `Open`.
* Reservations are rejected when the event is full.
* Available seats are calculated as:

```text
Remaining Seats = Capacity - Booked Seats
```

## Proof of Work

The `screenshots` folder contains screenshots showing:

* Creating an event
* Getting all events
* Successful reservation
* Getting event reservations
* Checking event availability
* Cancelling a reservation
* Failed reservation when the event is full or closed
