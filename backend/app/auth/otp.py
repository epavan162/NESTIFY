import random
from datetime import datetime, timedelta, timezone

# In-memory OTP store for development
# In production, use Redis or a proper SMS service
_otp_store: dict[str, dict] = {}


def generate_otp(phone: str) -> str:
    """Generate and store a 6-digit OTP for a phone number."""
    otp = str(random.randint(100000, 999999))
    _otp_store[phone] = {
        "otp": otp,
        "expires_at": datetime.now(timezone.utc) + timedelta(minutes=5),
    }
    # Mock SMS: print to console instead of sending
    print(f"[MOCK SMS] OTP for {phone}: {otp}")
    return otp


def verify_otp(phone: str, otp: str) -> bool:
    """Verify OTP for a phone number."""
    stored = _otp_store.get(phone)
    if not stored:
        return False
    if datetime.now(timezone.utc) > stored["expires_at"]:
        del _otp_store[phone]
        return False
    if stored["otp"] != otp:
        return False
    # OTP verified, remove it
    del _otp_store[phone]
    return True
