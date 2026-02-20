from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import User,Login,ResourceUpdate,AmbulanceRequest,ResetRequest,ResetPassword
from auth import register_user,login_user,request_reset,reset_password,google_login
from ai_engine import predict_inflow,strategy_analysis
from database import resources,logs

import smtplib, os
from pydantic import BaseModel
from google.oauth2 import id_token
from google.auth.transport import requests


app = FastAPI(title="Arogyalloc AI")

# ================= USER ACTIVITY STORAGE =================
user_logs={}

# ================= CORS =================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ================= EMAIL SENDER =================
def send_email(to,subject,message):
    try:
        server=smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login(os.getenv("EMAIL_USER"),os.getenv("EMAIL_PASS"))
        text=f"Subject:{subject}\n\n{message}"
        server.sendmail(os.getenv("EMAIL_USER"),to,text)
        server.quit()
    except:
        pass


# ================= AUTH =================

@app.post("/register")
def register(user:User):

    res=register_user(user)

    if res["status"]=="success":
        user_logs[user.username]=[]

        send_email(
            user.username,
            "Welcome to Arogyalloc AI",
            "Your healthcare platform account has been created successfully."
        )

    return res


@app.post("/login")
def login(data:Login):

    res=login_user(data)

    if res["status"]=="success":
        user_logs.setdefault(data.username,[]).append("User logged in")

    return res


# ================= GOOGLE LOGIN =================

class GoogleToken(BaseModel):
    token:str

@app.post("/google-login")
def google_login_route(data:GoogleToken):

    try:
        info=id_token.verify_oauth2_token(
            data.token,
            requests.Request(),
            audience=None
        )

        email=info["email"]

        res=google_login(email)

        user_logs.setdefault(email,[]).append("Logged in via Google")

        return res

    except:
        return {"status":"error","msg":"Invalid Google token"}


# ================= PASSWORD RESET =================

@app.post("/request-reset")
def forgot(data:ResetRequest):
    return request_reset(data.username)


@app.post("/reset-password")
def reset(data:ResetPassword):
    return reset_password(data.username,data.token,data.new_password)


# ================= DASHBOARD =================

@app.get("/dashboard")
def dashboard():

    inflow=predict_inflow()

    return {
        "occupancy":f"{inflow//3}%",
        "inflow":inflow,
        "gap":max(0,inflow-resources["Beds"])
    }


# ================= PREDICT =================

@app.get("/predict")
def predict():
    patients=predict_inflow()
    return {
        "patients":patients,
        "strategies":strategy_analysis(patients)
    }


# ================= INVENTORY =================

@app.get("/inventory")
def inventory():

    extra={
        "Ventilators":12,
        "ICU Beds":18,
        "Oxygen Tanks":40,
        "Blood Units":65,
        "Nurses":26,
        "PPE Kits":120,
        "Stretchers":20,
        "Ambulances":8,
        "Emergency Kits":35
    }

    return {**resources,**extra}


@app.post("/update-resource")
def update(res:ResourceUpdate):
    resources[res.name]=res.value
    logs.append(f"{res.name} updated to {res.value}")
    return {"status":"updated"}


# ================= AMBULANCE SERVICE =================

@app.post("/book-ambulance")
def ambulance(req:AmbulanceRequest):

    log=f"Ambulance booked for {req.name} at {req.location}"

    logs.append(log)
    user_logs.setdefault(req.email,[]).append(log)

    send_email(
        req.email,
        "Ambulance Confirmed",
        f"""
Hello {req.name}

Your ambulance request has been received.

Priority: {req.priority}
Location: {req.location}

Our emergency team is on the way.

Thank you for using Arogyalloc AI Healthcare Services.
"""
    )

    return {"status":"Ambulance dispatched"}


# ================= USER ACTIVITY =================

@app.get("/user-activity")
def activity(email:str):
    return user_logs.get(email,[])


# ================= LOGS =================

@app.get("/logs")
def logs_view():
    return logs