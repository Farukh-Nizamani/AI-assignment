from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
from model import AutismPredictor

app = FastAPI()

# Allow Streamlit (localhost) to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Autism Screening API is running. Use /predict for predictions."}

class Answers(BaseModel):
    answers: list[int]  # length must be 15, each value 0-3

predictor = AutismPredictor()

@app.post("/predict")
def predict(data: Answers):
    if len(data.answers) != 15 or any(a not in (0,1,2,3) for a in data.answers):
        raise HTTPException(status_code=400, detail="Invalid answers payload. Expected 15 answers.")
    prob = predictor.predict(data.answers)
    interpretation = "High likelihood" if prob > 0.7 else "Moderate" if prob > 0.4 else "Low likelihood"
    return {"probability": round(prob, 3), "interpretation": interpretation}
