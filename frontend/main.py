from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth_system import *
from ai_engine import predict_load
import random

app = FastAPI(title="Arogyalloc AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/register")
def register(data: dict):
    ok = register_user(
        data["username"],
        data["password"],
        data["question"],
        data["answer"]
    )
    return {"status": ok}

@app.post("/login")
def login(data: dict):
    return {"status": login_user(data["username"], data["password"])}

@app.get("/question/{username}")
def question(username: str):
    return {"question": get_security_question(username)}

@app.post("/reset")
def reset(data: dict):
    ok = reset_password(
        data["username"],
        data["answer"],
        data["newpass"]
    )
    return {"status": ok}

@app.get("/predict")
def predict():
    patients = predict_load()
    beds = random.randint(100,200)

    return {
        "patients": patients,
        "beds": beds,
        "strategies":{
            "Standard": beds,
            "Priority": int(beds*0.85),
            "AI Optimized": int(beds*1.25)
        }
    }