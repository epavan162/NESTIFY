from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.database import get_db
from app.models.user import User
from app.schemas.schemas import UserOut, UserUpdate
from app.auth.deps import get_current_user, require_role

router = APIRouter()


@router.get("/", response_model=list[UserOut])
def list_residents(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if user.role == "admin" and user.society_id:
        return db.query(User).filter(
            User.society_id == user.society_id,
            User.role == "resident"
        ).all()
    return []


@router.get("/{user_id}", response_model=UserOut)
def get_resident(user_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    resident = db.query(User).filter(User.id == user_id).first()
    if not resident:
        raise HTTPException(status_code=404, detail="Resident not found")
    return resident


@router.put("/{user_id}", response_model=UserOut)
def update_resident(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin")),
):
    resident = db.query(User).filter(User.id == user_id).first()
    if not resident:
        raise HTTPException(status_code=404, detail="Resident not found")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(resident, key, value)
    db.commit()
    db.refresh(resident)
    return resident


@router.post("/{user_id}/assign-flat", response_model=UserOut)
def assign_flat(
    user_id: int,
    flat_id: int,
    is_owner: bool = False,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin")),
):
    resident = db.query(User).filter(User.id == user_id).first()
    if not resident:
        raise HTTPException(status_code=404, detail="Resident not found")
    resident.flat_id = flat_id
    resident.is_owner = is_owner
    resident.moved_in_at = datetime.now(timezone.utc)
    resident.moved_out_at = None
    db.commit()
    db.refresh(resident)
    return resident


@router.post("/{user_id}/move-out", response_model=UserOut)
def move_out(
    user_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin")),
):
    resident = db.query(User).filter(User.id == user_id).first()
    if not resident:
        raise HTTPException(status_code=404, detail="Resident not found")
    resident.moved_out_at = datetime.now(timezone.utc)
    resident.flat_id = None
    db.commit()
    db.refresh(resident)
    return resident
