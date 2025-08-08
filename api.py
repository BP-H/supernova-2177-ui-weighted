# File: /api.py
# A simplified, Vercel-friendly API.

import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

# --- Pydantic Schemas (Data Models) ---
class VibeNodeOut(BaseModel):
    id: int
    name: str
    description: str
    author_username: str

# --- FastAPI App ---
# This is the main entry point for Vercel.
app = FastAPI(
    title="superNova_2177 API",
    description="A serverless API for the social metaverse.",
    version="1.0-Vercel"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Endpoints ---
@app.get("/api")
def get_root():
    """A simple endpoint to confirm the API is running."""
    return {"status": "superNova_2177 API is online and resonating."}

@app.get("/api/status", tags=["System"])
def get_system_status():
    """A sample endpoint that works without a database."""
    return {
        "status": "online",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "metrics": {
            "total_harmonizers": 1, # Placeholder data
            "total_vibenodes": 5,   # Placeholder data
        },
        "mission": "To create order and meaning from chaos through collective resonance.",
    }

@app.get("/api/feed", response_model=List[VibeNodeOut], tags=["Content"])
def get_feed():
    """A sample feed endpoint with placeholder data."""
    mock_feed = [
        VibeNodeOut(id=1, name="Reality #2177: The Neon Dimension", description="Consciousness flows through digital streams...", author_username="genesis"),
        VibeNodeOut(id=2, name="Quantum Entanglement Alert", description="Multiple timelines are converging...", author_username="taha"),
        VibeNodeOut(id=3, name="Portal Discovery: Dimension X-99", description="A new gateway has been discovered...", author_username="system"),
    ]
    return mock_feed
