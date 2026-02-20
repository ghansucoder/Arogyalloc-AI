import random

def predict_load():
    seasonal = random.uniform(1.1,1.5)
    outbreak = random.uniform(1.0,1.3)
    base = random.randint(150,300)

    return int(base * seasonal * outbreak)