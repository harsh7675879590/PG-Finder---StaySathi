import json
import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Lead, CallRecord
from app.agent.prompts import build_system_prompt
from app.agent.llm import llm_client
from app.agent.extractor import extract_post_call_data
from app.audio.tts import tts_service

router = APIRouter(prefix="/api/voice", tags=["Voice Engine"])
logger = logging.getLogger(__name__)

class InitiateCallRequest(BaseModel):
    lead_id: Optional[int] = None
    customer_name: Optional[str] = None
    phone_number: Optional[str] = None
    city: Optional[str] = None
    gender: Optional[str] = None
    budget: Optional[str] = None

class TurnRequest(BaseModel):
    messages: List[Dict[str, str]]
    metadata: Dict[str, Any]

class CompleteCallRequest(BaseModel):
    lead_id: Optional[int] = None
    transcript: List[Dict[str, str]]
    duration_seconds: int = 0
    metadata: Dict[str, Any]

@router.post("/initiate")
async def initiate_call(req: InitiateCallRequest, db: Session = Depends(get_db)):
    """
    Initializes a call with a lead, produces opening greeting and speech audio.
    """
    metadata = {}
    if req.lead_id:
        lead = db.query(Lead).filter(Lead.id == req.lead_id).first()
        if lead:
            metadata = {
                "customer_name": lead.customer_name or "",
                "phone_number": lead.phone_number or "",
                "city": lead.city or "",
                "gender": lead.gender or "",
                "budget": lead.budget or ""
            }
    else:
        metadata = {
            "customer_name": req.customer_name or "",
            "phone_number": req.phone_number or "",
            "city": req.city or "",
            "gender": req.gender or "",
            "budget": req.budget or ""
        }

    # Construct the initial greeting
    name = metadata.get("customer_name")
    if name:
        first_message = f"Hello, kya meri baat {name} ji se ho rahi hai? Main PG Finder se StaySathi bol rahi hoon."
    else:
        first_message = "Hello, main PG Finder se StaySathi bol rahi hoon. Aapne recently hamari website par PG search kiya tha, kya main aapka shubh naam jaan sakti hoon?"

    # Generate neural voice audio for opening
    audio_url = await tts_service.synthesize_speech(first_message)

    system_prompt = build_system_prompt(metadata)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "assistant", "content": first_message}
    ]

    return {
        "status": "connected",
        "metadata": metadata,
        "first_message": first_message,
        "audio_url": audio_url,
        "messages": messages
    }

@router.post("/turn")
async def conversation_turn(req: TurnRequest):
    """
    Processes a user speech turn, produces StaySathi's response, and synthesizes audio.
    """
    messages = req.messages
    # Get next response from LLM
    assistant_reply = llm_client.chat_turn(messages)
    
    # Generate neural speech audio
    audio_url = await tts_service.synthesize_speech(assistant_reply)

    return {
        "reply": assistant_reply,
        "audio_url": audio_url
    }

@router.post("/complete")
async def complete_call(req: CompleteCallRequest, db: Session = Depends(get_db)):
    """
    Concludes the call, triggers post-call extraction, and stores the CRM record.
    """
    extracted = extract_post_call_data(req.transcript, req.metadata)
    outcome = extracted.get("call_outcome", "completed")

    # Create CallRecord in DB
    record = CallRecord(
        lead_id=req.lead_id,
        duration_seconds=req.duration_seconds,
        transcript_json=json.dumps(req.transcript),
        audio_path=None,
        call_outcome=outcome,
        extracted_data_json=json.dumps(extracted)
    )
    db.add(record)

    # Update Lead status if linked
    if req.lead_id:
        lead = db.query(Lead).filter(Lead.id == req.lead_id).first()
        if lead:
            if outcome == "interested":
                lead.status = "QUALIFIED"
                if extracted.get("city") and extracted.get("city") != "Other":
                    lead.city = extracted.get("city")
                if extracted.get("monthly_budget"):
                    lead.budget = str(extracted.get("monthly_budget"))
            elif outcome == "busy_callback":
                lead.status = "CALLBACK"
            elif outcome == "not_interested":
                lead.status = "NOT_INTERESTED"
            elif outcome == "wrong_number":
                lead.status = "WRONG_NUMBER"

    db.commit()
    db.refresh(record)

    return {
        "status": "saved",
        "call_id": record.id,
        "outcome": outcome,
        "extracted_data": extracted
    }
