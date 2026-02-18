from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.database import get_db
from app.models.visitor import Visitor
from app.models.user import User
from app.schemas.schemas import VisitorCreate, VisitorUpdate, VisitorOut
from app.auth.deps import get_current_user, require_role

router = APIRouter()


@router.get("/", response_model=list[VisitorOut])
def list_visitors(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if user.role in ("admin", "security") and user.society_id:
        return db.query(Visitor).filter(
            Visitor.society_id == user.society_id
        ).order_by(Visitor.created_at.desc()).limit(100).all()
    if user.flat_id:
        return db.query(Visitor).filter(
            Visitor.flat_id == user.flat_id
        ).order_by(Visitor.created_at.desc()).all()
    return []


@router.post("/", response_model=VisitorOut)
def add_visitor(
    data: VisitorCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    society_id = data.society_id or user.society_id
    if not society_id:
        raise HTTPException(status_code=400, detail="Society ID required")
    visitor = Visitor(
        society_id=society_id,
        flat_id=data.flat_id,
        visitor_name=data.visitor_name,
        visitor_phone=data.visitor_phone,
        purpose=data.purpose,
        vehicle_number=data.vehicle_number,
    )
    db.add(visitor)
    db.commit()
    db.refresh(visitor)
    return visitor


@router.put("/{visitor_id}/approve", response_model=VisitorOut)
def approve_visitor(
    visitor_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    visitor = db.query(Visitor).filter(Visitor.id == visitor_id).first()
    if not visitor:
        raise HTTPException(status_code=404, detail="Visitor not found")
    visitor.status = "approved"
    visitor.approved_by = user.id
    db.commit()
    db.refresh(visitor)
    return visitor


@router.put("/{visitor_id}/checkout", response_model=VisitorOut)
def checkout_visitor(
    visitor_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    visitor = db.query(Visitor).filter(Visitor.id == visitor_id).first()
    if not visitor:
        raise HTTPException(status_code=404, detail="Visitor not found")
    visitor.status = "checked_out"
    visitor.exit_time = datetime.now(timezone.utc)
    db.commit()
    db.refresh(visitor)
    return visitor
