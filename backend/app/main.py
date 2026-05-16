from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.services.signal_generator import generate_fake_signals

app = FastAPI(title="SentinelRF API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "SentinelRF Backend Running"}

@app.get("/signals")
def get_signals(count: int = 100):
    return generate_fake_signals(count)