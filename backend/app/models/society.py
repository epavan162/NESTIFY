from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Society(Base):
    __tablename__ = "societies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    address = Column(String(500), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    pincode = Column(String(10), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    towers = relationship("Tower", back_populates="society", cascade="all, delete-orphan")
    users = relationship("User", back_populates="society")
    notices = relationship("Notice", back_populates="society", cascade="all, delete-orphan")
    complaints = relationship("Complaint", back_populates="society")
    visitors = relationship("Visitor", back_populates="society")
    invoices = relationship("MaintenanceInvoice", back_populates="society")
    bookings = relationship("Booking", back_populates="society")
    polls = relationship("Poll", back_populates="society")
