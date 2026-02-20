import random

def predict_inflow():
    base = random.randint(150,300)
    risk = random.uniform(1.1,1.5)
    return int(base*risk)

def strategy_analysis(patients):
    return {
        "Standard": patients*0.9,
        "Priority": patients*0.75,
        "AI Optimized": patients*0.6
    }

def forecast_resources():
    return {
        "Beds": random.randint(60,100),
        "Oxygen": random.randint(10,24),
        "Ventilators": random.randint(20,60)
    }