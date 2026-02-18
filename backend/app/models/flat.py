from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Flat(Base):
    __tablename__ = "flats"

    id = Column(Integer, primary_key=True, index=True)
    tower_id = Column(Integer, ForeignKey("towers.id", ondelete="CASCADE"), nullable=False)
    flat_number = Column(String(20), nullable=False)
    floor = Column(Integer, nullable=False, default=0)
    area_sqft = Column(Float, nullable=True)
    flat_type = Column(String(20), nullable=True)  # 1BHK, 2BHK, 3BHK, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    tower = relationship("Tower", back_populates="flats")
    residents = relationship("User", back_populates="flat")
    invoices = relationship("MaintenanceInvoice", back_populates="flat")
    visitors = relationship("Visitor", back_populates="flat")
    complaints = relationship("Complaint", back_populates="flat")
