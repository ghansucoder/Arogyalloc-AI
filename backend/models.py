from pydantic import BaseModel, EmailStr
from typing import Optional

# ================= USER =================
class User(BaseModel):
    username: EmailStr
    password: str
    role: str

    phone: Optional[str] = None
    full_name: Optional[str] = None

    # account features
    reset_token: Optional[str] = None
    session_token: Optional[str] = None

    # preferences
    email_notifications: Optional[bool] = True
    sms_notifications: Optional[bool] = True


# ================= LOGIN =================
class Login(BaseModel):
    username: EmailStr
    password: str


# ================= PASSWORD RESET =================
class ResetRequest(BaseModel):
    username: EmailStr

class ResetPassword(BaseModel):
    username: EmailStr
    token: str
    new_password: str


# ================= AMBULANCE =================
class AmbulanceRequest(BaseModel):
    name: str
    email: EmailStr
    phone: str
    location: str
    priority: str


# ================= RESOURCE =================
class ResourceUpdate(BaseModel):
    name: str
    value: int


# ================= SERVICE LOG =================
class ServiceLog(BaseModel):
    email: EmailStr
    service: str
    status: str