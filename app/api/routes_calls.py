import json
from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import CallRecord

router = APIRouter(prefix="/api/calls", tags=["Calls"])

@router.get("")
def get_calls(db: Session = Depends(get_db)):
    records = db.query(CallRecord).order_by(CallRecord.id.desc()).all()
    results = []
    for r in records:
        results.append({
            "id": r.id,
            "lead_id": r.lead_id,
            "lead_name": r.lead.customer_name if r.lead else "Unknown",
            "duration_seconds": r.duration_seconds,
            "call_outcome": r.call_outcome,
            "audio_path": r.audio_path,
            "transcript": json.loads(r.transcript_json) if r.transcript_json else [],
            "extracted_data": json.loads(r.extracted_data_json) if r.extracted_data_json else {},
            "created_at": r.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    return results

@router.get("/{call_id}")
def get_call(call_id: int, db: Session = Depends(get_db)):
    r = db.query(CallRecord).filter(CallRecord.id == call_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Call record not found")
    return {
        "id": r.id,
        "lead_id": r.lead_id,
        "duration_seconds": r.duration_seconds,
        "call_outcome": r.call_outcome,
        "audio_path": r.audio_path,
        "transcript": json.loads(r.transcript_json) if r.transcript_json else [],
        "extracted_data": json.loads(r.extracted_data_json) if r.extracted_data_json else {},
        "created_at": r.created_at.strftime("%Y-%m-%d %H:%M:%S")
    }
