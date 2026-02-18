from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import date, time
from app.database import get_db
from app.models.booking import Booking
from app.models.user import User
from app.schemas.schemas import BookingCreate, BookingOut
from app.auth.deps import get_current_user

router = APIRouter()


@router.get("/", response_model=list[BookingOut])
def list_bookings(
    facility: str | None = None,
    booking_date: str | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    query = db.query(Booking)
    if user.society_id:
        query = query.filter(Booking.society_id == user.society_id)
    if facility:
        query = query.filter(Booking.facility_name == facility)
    if booking_date:
        try:
            parsed_date = date.fromisoformat(booking_date)
            query = query.filter(Booking.booking_date == parsed_date)
        except ValueError:
            pass
    return query.order_by(Booking.booking_date.desc()).all()


@router.post("/", response_model=BookingOut)
def create_booking(
    data: BookingCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    society_id = data.society_id or user.society_id
    if not society_id:
        raise HTTPException(status_code=400, detail="Society ID required")

    # Parse string inputs to proper types
    try:
        booking_date = date.fromisoformat(data.booking_date)
    except (ValueError, TypeError):
        raise HTTPException(status_code=400, detail="Invalid booking_date. Use YYYY-MM-DD")

    try:
        start = time.fromisoformat(data.start_time)
    except (ValueError, TypeError):
        raise HTTPException(status_code=400, detail="Invalid start_time. Use HH:MM")

    try:
        end = time.fromisoformat(data.end_time)
    except (ValueError, TypeError):
        raise HTTPException(status_code=400, detail="Invalid end_time. Use HH:MM")

    if start >= end:
        raise HTTPException(status_code=400, detail="Start time must be before end time")

    # Check for double booking
    conflict = db.query(Booking).filter(
        and_(
            Booking.society_id == society_id,
            Booking.facility_name == data.facility_name,
            Booking.booking_date == booking_date,
            Booking.status == "confirmed",
            Booking.start_time < end,
            Booking.end_time > start,
        )
    ).first()

    if conflict:
        raise HTTPException(status_code=409, detail="Time slot already booked for this facility")

    booking = Booking(
        society_id=society_id,
        user_id=user.id,
        facility_name=data.facility_name,
        booking_date=booking_date,
        start_time=start,
        end_time=end,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


@router.delete("/{booking_id}")
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.user_id != user.id and user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    booking.status = "cancelled"
    db.commit()
    return {"message": "Booking cancelled"}
