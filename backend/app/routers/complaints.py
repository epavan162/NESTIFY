from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.complaint import Complaint
from app.models.user import User
from app.schemas.schemas import ComplaintCreate, ComplaintUpdate, ComplaintOut
from app.auth.deps import get_current_user, require_role

router = APIRouter()


@router.get("/", response_model=list[ComplaintOut])
def list_complaints(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if user.role == "admin" and user.society_id:
        return db.query(Complaint).filter(
            Complaint.society_id == user.society_id
        ).order_by(Complaint.created_at.desc()).all()
    return db.query(Complaint).filter(
        Complaint.user_id == user.id
    ).order_by(Complaint.created_at.desc()).all()


@router.post("/", response_model=ComplaintOut)
def create_complaint(
    data: ComplaintCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    society_id = data.society_id or user.society_id
    if not society_id:
        raise HTTPException(status_code=400, detail="Society ID required")
    complaint = Complaint(
        society_id=society_id,
        user_id=user.id,
        flat_id=user.flat_id,
        title=data.title,
        description=data.description,
        image_url=data.image_url,
        priority=data.priority,
    )
    db.add(complaint)
    db.commit()
    db.refresh(complaint)
    return complaint


@router.put("/{complaint_id}", response_model=ComplaintOut)
def update_complaint(
    complaint_id: int,
    data: ComplaintUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(complaint, key, value)
    db.commit()
    db.refresh(complaint)
    return complaint
