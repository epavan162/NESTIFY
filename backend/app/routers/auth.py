from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.database import get_db
from app.models.user import User
from app.schemas.schemas import (
    OTPRequest, OTPVerify, LoginRequest, TokenResponse, UserOut, UserCreate
)
from app.auth.jwt import create_access_token
from app.auth.oauth import get_google_auth_url, exchange_google_code
from app.auth.otp import generate_otp, verify_otp
from app.auth.deps import get_current_user

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", response_model=UserOut)
def register(data: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    if data.email:
        existing = db.query(User).filter(User.email == data.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
    if data.phone:
        existing = db.query(User).filter(User.phone == data.phone).first()
        if existing:
            raise HTTPException(status_code=400, detail="Phone already registered")

    hashed_pw = pwd_context.hash(data.password) if data.password else None
    user = User(
        name=data.name,
        email=data.email,
        phone=data.phone,
        password_hash=hashed_pw,
        role=data.role,
        society_id=data.society_id,
        flat_id=data.flat_id,
        is_owner=data.is_owner,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not user.password_hash:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not pwd_context.verify(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id), "role": user.role})
    return TokenResponse(access_token=token, user=UserOut.model_validate(user))


@router.post("/otp/send")
def send_otp(data: OTPRequest):
    otp = generate_otp(data.phone)
    return {"message": f"OTP sent to {data.phone}", "otp_dev": otp}


@router.post("/otp/verify", response_model=TokenResponse)
def verify_phone_otp(data: OTPVerify, db: Session = Depends(get_db)):
    if not verify_otp(data.phone, data.otp):
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    user = db.query(User).filter(User.phone == data.phone).first()
    if not user:
        # Auto-register on first OTP login
        user = User(
            name=data.name or f"User-{data.phone[-4:]}",
            phone=data.phone,
            role="resident",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    token = create_access_token({"sub": str(user.id), "role": user.role})
    return TokenResponse(access_token=token, user=UserOut.model_validate(user))


@router.get("/google/url")
def google_login_url():
    return {"url": get_google_auth_url()}


@router.get("/google/callback")
async def google_callback(code: str, db: Session = Depends(get_db)):
    userinfo = await exchange_google_code(code)
    if not userinfo or "email" not in userinfo:
        raise HTTPException(status_code=400, detail="Google authentication failed")

    google_id = userinfo.get("id")
    email = userinfo.get("email")
    name = userinfo.get("name", email)
    avatar = userinfo.get("picture")

    user = db.query(User).filter(User.google_id == google_id).first()
    if not user:
        user = db.query(User).filter(User.email == email).first()
        if user:
            user.google_id = google_id
            user.avatar_url = avatar
        else:
            user = User(
                name=name,
                email=email,
                google_id=google_id,
                avatar_url=avatar,
                role="resident",
            )
            db.add(user)
        db.commit()
        db.refresh(user)

    token = create_access_token({"sub": str(user.id), "role": user.role})
    # Redirect to frontend with token
    from app.config import get_settings
    settings = get_settings()
    return {"access_token": token, "user": UserOut.model_validate(user)}


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
