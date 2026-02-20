import hashlib
import secrets
from database import users


# =========================
# PASSWORD HASHING
# =========================
def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()


# =========================
# REGISTER USER
# =========================
def register_user(user):

    # allow only gmail accounts
    if not user.username.endswith("@gmail.com"):
        return {"status": "error", "msg": "Only Gmail accounts allowed"}

    if user.username in users:
        return {"status": "error", "msg": "User already exists"}

    users[user.username] = {
        "password": hash_password(user.password),
        "role": user.role,
        "phone": user.phone,
        "full_name": user.full_name,
        "reset_token": None,
        "session": None,
        "email_notifications": True,
        "sms_notifications": True
    }

    return {"status": "success"}


# =========================
# LOGIN USER
# =========================
def login_user(data):

    if data.username not in users:
        return {"status": "error", "msg": "User not found"}

    hashed = hash_password(data.password)

    if users[data.username]["password"] != hashed:
        return {"status": "error", "msg": "Wrong password"}

    token = secrets.token_hex(16)
    users[data.username]["session"] = token

    return {
        "status": "success",
        "role": users[data.username]["role"],
        "token": token
    }


# =========================
# PASSWORD RESET REQUEST
# =========================
def request_reset(username):

    if username not in users:
        return {"status": "error", "msg": "User not found"}

    token = secrets.token_hex(12)
    users[username]["reset_token"] = token

    return {
        "status": "success",
        "reset_token": token
    }


# =========================
# RESET PASSWORD
# =========================
def reset_password(username, token, new_password):

    if username not in users:
        return {"status": "error", "msg": "User not found"}

    if users[username]["reset_token"] != token:
        return {"status": "error", "msg": "Invalid token"}

    users[username]["password"] = hash_password(new_password)
    users[username]["reset_token"] = None

    return {"status": "success"}


# =========================
# GOOGLE LOGIN READY
# =========================
def google_login(email):

    if not email.endswith("@gmail.com"):
        return {"status": "error", "msg": "Use Gmail account"}

    if email not in users:
        users[email] = {
            "password": None,
            "role": "user",
            "phone": None,
            "full_name": None,
            "reset_token": None,
            "session": None,
            "email_notifications": True,
            "sms_notifications": True
        }

    token = secrets.token_hex(16)
    users[email]["session"] = token

    return {"status": "success", "token": token}