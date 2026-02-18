from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Tower(Base):
    __tablename__ = "towers"

    id = Column(Integer, primary_key=True, index=True)
    society_id = Column(Integer, ForeignKey("societies.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    total_floors = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    society = relationship("Society", back_populates="towers")
    flats = relationship("Flat", back_populates="tower", cascade="all, delete-orphan")
