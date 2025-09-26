from fastapi import FastAPI
from typing import List

app = FastAPI()

flights = [
    {"id": 1, "airline": "Latam", "origin": "Quito", "destination": "Chile", "seats": 10},
    {"id": 2, "airline": "Avianca", "origin": "Bogotá", "destination": "Guayaquil", "seats": 5}
]

@app.get("/")
def home():
    return {"message": "API de vuelos funcionando"}

@app.get("/flights")
def get_flights() -> List[dict]:
    return flights
