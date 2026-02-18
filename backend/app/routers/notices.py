from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.notice import Notice
from app.models.user import User
from app.schemas.schemas import NoticeCreate, NoticeOut
from app.auth.deps import get_current_user, require_role

router = APIRouter()


@router.get("/", response_model=list[NoticeOut])
def list_notices(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if user.society_id:
        return db.query(Notice).filter(
            Notice.society_id == user.society_id,
            Notice.is_active == True
        ).order_by(Notice.created_at.desc()).all()
    return []


@router.post("/", response_model=NoticeOut)
def create_notice(
    data: NoticeCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin")),
):
    society_id = data.society_id or user.society_id
    if not society_id:
        raise HTTPException(status_code=400, detail="Society ID required")
    notice = Notice(
        society_id=society_id,
        title=data.title,
        content=data.content,
        category=data.category,
        created_by=user.id,
    )
    db.add(notice)
    db.commit()
    db.refresh(notice)
    return notice


@router.delete("/{notice_id}")
def delete_notice(
    notice_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin")),
):
    notice = db.query(Notice).filter(Notice.id == notice_id).first()
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    notice.is_active = False
    db.commit()
    return {"message": "Notice deleted"}
