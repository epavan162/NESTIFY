from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Society, Tower, Flat
from app.schemas.schemas import (
    SocietyCreate, SocietyOut, TowerCreate, TowerOut, FlatCreate, FlatOut
)
from app.auth.deps import get_current_user, require_role
from app.models.user import User

router = APIRouter()


# --- Societies ---
@router.get("/", response_model=list[SocietyOut])
def list_societies(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.role == "admin":
        return db.query(Society).all()
    if user.society_id:
        return db.query(Society).filter(Society.id == user.society_id).all()
    return []


@router.post("/", response_model=SocietyOut)
def create_society(
    data: SocietyCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin")),
):
    society = Society(**data.model_dump())
    db.add(society)
    db.commit()
    db.refresh(society)
    # Assign admin to this society if not already assigned
    if not user.society_id:
        user.society_id = society.id
        db.commit()
    return society


@router.get("/{society_id}", response_model=SocietyOut)
def get_society(society_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    society = db.query(Society).filter(Society.id == society_id).first()
    if not society:
        raise HTTPException(status_code=404, detail="Society not found")
    return society


# --- Towers ---
@router.get("/{society_id}/towers", response_model=list[TowerOut])
def list_towers(society_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Tower).filter(Tower.society_id == society_id).all()


@router.post("/towers", response_model=TowerOut)
def create_tower(
    data: TowerCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin")),
):
    tower = Tower(**data.model_dump())
    db.add(tower)
    db.commit()
    db.refresh(tower)
    return tower


# --- Flats ---
@router.get("/towers/{tower_id}/flats", response_model=list[FlatOut])
def list_flats(tower_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Flat).filter(Flat.tower_id == tower_id).all()


@router.post("/flats", response_model=FlatOut)
def create_flat(
    data: FlatCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin")),
):
    flat = Flat(**data.model_dump())
    db.add(flat)
    db.commit()
    db.refresh(flat)
    return flat
