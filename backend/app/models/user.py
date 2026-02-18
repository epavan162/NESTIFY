from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=True, index=True)
    phone = Column(String(20), unique=True, nullable=True, index=True)
    name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=True)
    role = Column(String(20), nullable=False, default="resident")  # admin, resident, security, treasurer
    society_id = Column(Integer, ForeignKey("societies.id"), nullable=True)
    flat_id = Column(Integer, ForeignKey("flats.id"), nullable=True)
    is_owner = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    google_id = Column(String(255), nullable=True, unique=True)
    avatar_url = Column(String(500), nullable=True)
    moved_in_at = Column(DateTime(timezone=True), nullable=True)
    moved_out_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    society = relationship("Society", back_populates="users")
    flat = relationship("Flat", back_populates="residents")
    payments = relationship("Payment", back_populates="user")
    complaints = relationship("Complaint", back_populates="user", foreign_keys="Complaint.user_id")
    bookings = relationship("Booking", back_populates="user")
    votes = relationship("Vote", back_populates="user")
