from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    society_id = Column(Integer, ForeignKey("societies.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    flat_id = Column(Integer, ForeignKey("flats.id"), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    status = Column(String(20), default="open")  # open, in_progress, resolved
    priority = Column(String(20), default="medium")  # low, medium, high, urgent
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    society = relationship("Society", back_populates="complaints")
    user = relationship("User", back_populates="complaints", foreign_keys=[user_id])
    flat = relationship("Flat", back_populates="complaints")
