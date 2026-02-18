from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Visitor(Base):
    __tablename__ = "visitors"

    id = Column(Integer, primary_key=True, index=True)
    society_id = Column(Integer, ForeignKey("societies.id"), nullable=False)
    flat_id = Column(Integer, ForeignKey("flats.id"), nullable=False)
    visitor_name = Column(String(255), nullable=False)
    visitor_phone = Column(String(20), nullable=True)
    purpose = Column(String(255), nullable=True)
    vehicle_number = Column(String(20), nullable=True)
    entry_time = Column(DateTime(timezone=True), server_default=func.now())
    exit_time = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(20), default="pending")  # pending, approved, rejected, checked_out
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    society = relationship("Society", back_populates="visitors")
    flat = relationship("Flat", back_populates="visitors")
