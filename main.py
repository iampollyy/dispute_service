from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import engine, get_db, create_schema, Base
from models import Dispute
from schemas import (
    DisputeResponse, DisputeCreate, DisputeStatusUpdate
)
from seed import seed_data
from message_reader import start_message_reader

app = FastAPI(title="DisputeService", version="1.0.0")


@app.on_event("startup")
def startup():
    create_schema()
    Base.metadata.create_all(bind=engine)
    seed_data()
    start_message_reader()


# ==================== DISPUTE ENDPOINTS ====================

@app.get("/disputes/{dispute_id}", response_model=DisputeResponse)
def get_dispute(dispute_id: int, db: Session = Depends(get_db)):
    dispute = db.query(Dispute).filter(Dispute.dispute_id == dispute_id).first()
    if not dispute:
        raise HTTPException(status_code=404, detail="Dispute not found")
    return dispute


@app.post("/disputes", response_model=DisputeResponse, status_code=201)
def create_dispute(data: DisputeCreate, db: Session = Depends(get_db)):
    dispute = Dispute(**data.model_dump())
    db.add(dispute)
    db.commit()
    db.refresh(dispute)
    return dispute


@app.patch("/disputes/{dispute_id}/status", response_model=DisputeResponse)
def update_dispute_status(
    dispute_id: int,
    data: DisputeStatusUpdate,
    db: Session = Depends(get_db)
):
    dispute = db.query(Dispute).filter(Dispute.dispute_id == dispute_id).first()
    if not dispute:
        raise HTTPException(status_code=404, detail="Dispute not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(dispute, key, value)
    db.commit()
    db.refresh(dispute)
    return dispute