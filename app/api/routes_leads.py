from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Lead, LeadCreate, LeadResponse

router = APIRouter(prefix="/api/leads", tags=["Leads"])

@router.get("", response_model=List[LeadResponse])
def get_leads(db: Session = Depends(get_db)):
    return db.query(Lead).order_by(Lead.id.desc()).all()

@router.post("", response_model=LeadResponse)
def create_lead(lead_in: LeadCreate, db: Session = Depends(get_db)):
    lead = Lead(
        customer_name=lead_in.customer_name,
        phone_number=lead_in.phone_number,
        city=lead_in.city,
        gender=lead_in.gender,
        budget=lead_in.budget,
        status="NEW"
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead

@router.delete("/{lead_id}")
def delete_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    db.delete(lead)
    db.commit()
    return {"message": "Lead deleted successfully"}
