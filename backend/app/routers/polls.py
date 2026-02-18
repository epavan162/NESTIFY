from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.poll import Poll, Vote
from app.models.user import User
from app.schemas.schemas import PollCreate, PollOut, VoteCreate, VoteOut
from app.auth.deps import get_current_user, require_role

router = APIRouter()


@router.get("/", response_model=list[PollOut])
def list_polls(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if not user.society_id:
        return []
    polls = db.query(Poll).filter(
        Poll.society_id == user.society_id,
        Poll.is_active == True
    ).order_by(Poll.created_at.desc()).all()

    result = []
    for poll in polls:
        votes = db.query(Vote).filter(Vote.poll_id == poll.id).all()
        vote_counts = [0] * len(poll.options)
        user_voted = None
        for v in votes:
            if v.option_index < len(vote_counts):
                vote_counts[v.option_index] += 1
            if v.user_id == user.id:
                user_voted = v.option_index
        result.append(PollOut(
            id=poll.id,
            society_id=poll.society_id,
            question=poll.question,
            options=poll.options,
            created_by=poll.created_by,
            is_active=poll.is_active,
            expires_at=poll.expires_at,
            created_at=poll.created_at,
            vote_counts=vote_counts,
            total_votes=len(votes),
            user_voted=user_voted,
        ))
    return result


@router.post("/", response_model=PollOut)
def create_poll(
    data: PollCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin")),
):
    society_id = data.society_id or user.society_id
    if not society_id:
        raise HTTPException(status_code=400, detail="Society ID required")
    poll = Poll(
        society_id=society_id,
        question=data.question,
        options=data.options,
        created_by=user.id,
    )
    db.add(poll)
    db.commit()
    db.refresh(poll)
    return PollOut(
        id=poll.id,
        society_id=poll.society_id,
        question=poll.question,
        options=poll.options,
        created_by=poll.created_by,
        is_active=poll.is_active,
        created_at=poll.created_at,
        vote_counts=[0] * len(poll.options),
        total_votes=0,
    )


@router.post("/{poll_id}/vote", response_model=VoteOut)
def cast_vote(
    poll_id: int,
    data: VoteCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    poll = db.query(Poll).filter(Poll.id == poll_id, Poll.is_active == True).first()
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found or inactive")
    if data.option_index >= len(poll.options):
        raise HTTPException(status_code=400, detail="Invalid option")
    existing = db.query(Vote).filter(Vote.poll_id == poll_id, Vote.user_id == user.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already voted")
    vote = Vote(poll_id=poll_id, user_id=user.id, option_index=data.option_index)
    db.add(vote)
    db.commit()
    db.refresh(vote)
    return vote
