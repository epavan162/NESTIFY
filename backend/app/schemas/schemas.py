from pydantic import BaseModel, field_serializer
from datetime import datetime, date, time
from typing import Any


# --- Auth Schemas ---
class OTPRequest(BaseModel):
    phone: str

class OTPVerify(BaseModel):
    phone: str
    otp: str
    name: str | None = None

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: "UserOut"


# --- User Schemas ---
class UserBase(BaseModel):
    name: str
    email: str | None = None
    phone: str | None = None
    role: str = "resident"

class UserCreate(UserBase):
    password: str | None = None
    society_id: int | None = None
    flat_id: int | None = None
    is_owner: bool = False

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    role: str | None = None
    flat_id: int | None = None
    is_owner: bool | None = None
    is_active: bool | None = None

class UserOut(BaseModel):
    id: int
    name: str
    email: str | None = None
    phone: str | None = None
    role: str
    society_id: int | None = None
    flat_id: int | None = None
    is_owner: bool
    is_active: bool
    avatar_url: str | None = None
    created_at: datetime | None = None

    class Config:
        from_attributes = True


# --- Society Schemas ---
class SocietyBase(BaseModel):
    name: str
    address: str
    city: str
    state: str
    pincode: str

class SocietyCreate(SocietyBase):
    pass

class SocietyOut(SocietyBase):
    id: int
    is_active: bool
    created_at: datetime | None = None

    class Config:
        from_attributes = True


# --- Tower Schemas ---
class TowerBase(BaseModel):
    name: str
    total_floors: int = 1

class TowerCreate(TowerBase):
    society_id: int

class TowerOut(TowerBase):
    id: int
    society_id: int
    created_at: datetime | None = None

    class Config:
        from_attributes = True


# --- Flat Schemas ---
class FlatBase(BaseModel):
    flat_number: str
    floor: int = 0
    area_sqft: float | None = None
    flat_type: str | None = None

class FlatCreate(FlatBase):
    tower_id: int

class FlatOut(FlatBase):
    id: int
    tower_id: int
    created_at: datetime | None = None

    class Config:
        from_attributes = True


# --- Maintenance Invoice Schemas ---
class InvoiceBase(BaseModel):
    flat_id: int
    amount: float
    due_date: str  # Accept string from frontend
    month: int
    year: int

class InvoiceCreate(InvoiceBase):
    society_id: int | None = None

class InvoiceOut(BaseModel):
    id: int
    society_id: int
    flat_id: int
    amount: float
    late_fee: float
    total_amount: float
    due_date: date  # Return as date
    month: int
    year: int
    status: str
    created_at: datetime | None = None

    @field_serializer("due_date")
    def serialize_due_date(self, v: date) -> str:
        return v.isoformat() if v else ""

    class Config:
        from_attributes = True


# --- Payment Schemas ---
class PaymentCreate(BaseModel):
    invoice_id: int
    amount: float
    payment_method: str | None = None
    transaction_id: str | None = None

class PaymentOut(BaseModel):
    id: int
    invoice_id: int
    user_id: int
    amount: float
    payment_method: str | None = None
    transaction_id: str | None = None
    payment_date: datetime | None = None

    class Config:
        from_attributes = True


# --- Complaint Schemas ---
class ComplaintBase(BaseModel):
    title: str
    description: str | None = None
    priority: str = "medium"

class ComplaintCreate(ComplaintBase):
    image_url: str | None = None
    society_id: int | None = None

class ComplaintUpdate(BaseModel):
    status: str | None = None
    assigned_to: int | None = None
    priority: str | None = None

class ComplaintOut(BaseModel):
    id: int
    society_id: int
    user_id: int
    flat_id: int | None = None
    title: str
    description: str | None = None
    image_url: str | None = None
    status: str
    priority: str
    assigned_to: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


# --- Visitor Schemas ---
class VisitorBase(BaseModel):
    visitor_name: str
    visitor_phone: str | None = None
    purpose: str | None = None
    vehicle_number: str | None = None

class VisitorCreate(VisitorBase):
    flat_id: int
    society_id: int | None = None

class VisitorUpdate(BaseModel):
    status: str | None = None

class VisitorOut(BaseModel):
    id: int
    society_id: int
    flat_id: int
    visitor_name: str
    visitor_phone: str | None = None
    purpose: str | None = None
    vehicle_number: str | None = None
    entry_time: datetime | None = None
    exit_time: datetime | None = None
    status: str
    approved_by: int | None = None
    created_at: datetime | None = None

    class Config:
        from_attributes = True


# --- Notice Schemas ---
class NoticeBase(BaseModel):
    title: str
    content: str
    category: str = "general"

class NoticeCreate(NoticeBase):
    society_id: int | None = None

class NoticeOut(BaseModel):
    id: int
    society_id: int
    title: str
    content: str
    category: str
    created_by: int
    is_active: bool
    created_at: datetime | None = None

    class Config:
        from_attributes = True


# --- Booking Schemas ---
class BookingBase(BaseModel):
    facility_name: str
    booking_date: str  # Accept string from frontend
    start_time: str    # Accept string from frontend
    end_time: str      # Accept string from frontend

class BookingCreate(BookingBase):
    society_id: int | None = None

class BookingOut(BaseModel):
    id: int
    society_id: int
    user_id: int
    facility_name: str
    booking_date: date
    start_time: time
    end_time: time
    status: str
    created_at: datetime | None = None

    @field_serializer("booking_date")
    def serialize_booking_date(self, v: date) -> str:
        return v.isoformat() if v else ""

    @field_serializer("start_time")
    def serialize_start_time(self, v: time) -> str:
        return v.strftime("%H:%M") if v else ""

    @field_serializer("end_time")
    def serialize_end_time(self, v: time) -> str:
        return v.strftime("%H:%M") if v else ""

    class Config:
        from_attributes = True


# --- Poll Schemas ---
class PollBase(BaseModel):
    question: str
    options: list[str]

class PollCreate(PollBase):
    society_id: int | None = None
    expires_at: str | None = None

class PollOut(BaseModel):
    id: int
    society_id: int
    question: str
    options: list[str]
    created_by: int
    is_active: bool
    expires_at: datetime | None = None
    created_at: datetime | None = None
    vote_counts: list[int] | None = None
    total_votes: int | None = None
    user_voted: int | None = None

    class Config:
        from_attributes = True


class VoteCreate(BaseModel):
    option_index: int

class VoteOut(BaseModel):
    id: int
    poll_id: int
    user_id: int
    option_index: int
    created_at: datetime | None = None

    class Config:
        from_attributes = True


# Resolve forward reference
TokenResponse.model_rebuild()
