# main.py
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(
    title="API de Consulta de Vuelos - Latam (Demo)",
    description="API demo para consultar disponibilidad de vuelos por aerolínea (mock data).",
    version="1.0.0"
)

class Flight(BaseModel):
    flight_id: str
    airline: str
    origin: str
    destination: str
    departure: datetime
    arrival: datetime
    seats_available: int
    price_usd: float

MOCK_FLIGHTS = [
    {
        "flight_id": "LA100",
        "airline": "Latam",
        "origin": "SCL",
        "destination": "LIM",
        "departure": "2025-10-01T09:00:00",
        "arrival": "2025-10-01T10:30:00",
        "seats_available": 12,
        "price_usd": 120.0
    },
    {
        "flight_id": "LA200",
        "airline": "Latam",
        "origin": "GYE",
        "destination": "UIO",
        "departure": "2025-10-02T07:00:00",
        "arrival": "2025-10-02T08:15:00",
        "seats_available": 5,
        "price_usd": 90.0
    },
    {
        "flight_id": "AV300",
        "airline": "Avianca",
        "origin": "MDE",
        "destination": "BOG",
        "departure": "2025-10-03T12:00:00",
        "arrival": "2025-10-03T13:10:00",
        "seats_available": 20,
        "price_usd": 75.0
    }
]

# convertir strings a objetos Flight
from dateutil import parser
FLIGHTS: List[Flight] = []
for f in MOCK_FLIGHTS:
    f_copy = f.copy()
    f_copy['departure'] = parser.isoparse(f_copy['departure'])
    f_copy['arrival'] = parser.isoparse(f_copy['arrival'])
    FLIGHTS.append(Flight(**f_copy))

@app.get("/", tags=["root"])
def read_root():
    return {"message": "API de Consulta de Vuelos - Latam (Demo). /docs para Swagger UI"}

@app.get("/flights", response_model=List[Flight], tags=["flights"])
def get_flights(
    airline: Optional[str] = Query(None, description="Filtrar por aerolínea (ej: Latam)"),
    origin: Optional[str] = Query(None, description="Código IATA origen (ej: SCL)"),
    destination: Optional[str] = Query(None, description="Código IATA destino (ej: LIM)"),
    min_seats: Optional[int] = Query(None, description="Disponibilidad mínima de asientos")
):
    results = FLIGHTS
    if airline:
        results = [f for f in results if f.airline.lower() == airline.lower()]
    if origin:
        results = [f for f in results if f.origin.lower() == origin.lower()]
    if destination:
        results = [f for f in results if f.destination.lower() == destination.lower()]
    if min_seats is not None:
        results = [f for f in results if f.seats_available >= min_seats]
    return results

@app.get("/flights/{flight_id}", response_model=Flight, tags=["flights"])
def get_flight_by_id(flight_id: str):
    for f in FLIGHTS:
        if f.flight_id.lower() == flight_id.lower():
            return f
    raise HTTPException(status_code=404, detail="Vuelo no encontrado")
