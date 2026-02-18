from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    society_id = Column(Integer, ForeignKey("societies.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    facility_name = Column(String(100), nullable=False)  # gym, party_hall, swimming_pool, etc.
    booking_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    status = Column(String(20), default="confirmed")  # confirmed, cancelled
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    society = relationship("Society", back_populates="bookings")
    user = relationship("User", back_populates="bookings")
