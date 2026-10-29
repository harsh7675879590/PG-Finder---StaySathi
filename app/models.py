import datetime
import json
from typing import Optional, List, Dict, Any
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field
from app.database import Base

# ==========================================
# SQLAlchemy ORM Models
# ==========================================

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(100), nullable=True)
    phone_number = Column(String(20), nullable=True)
    city = Column(String(50), nullable=True)
    gender = Column(String(20), nullable=True)
    budget = Column(String(50), nullable=True)
    status = Column(String(30), default="NEW")  # NEW, QUALIFIED, CALLBACK, NOT_INTERESTED
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    calls = relationship("CallRecord", back_populates="lead", cascade="all, delete-orphan")


class CallRecord(Base):
    __tablename__ = "call_records"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=True)
    duration_seconds = Column(Integer, default=0)
    transcript_json = Column(Text, default="[]")  # List of {role: str, content: str, timestamp: str}
    audio_path = Column(String(255), nullable=True)
    call_outcome = Column(String(50), default="PENDING")  # interested, busy_callback, wrong_number, not_interested
    extracted_data_json = Column(Text, default="{}")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    lead = relationship("Lead", back_populates="calls")


# ==========================================
# Pydantic Schemas
# ==========================================

class LeadBase(BaseModel):
    customer_name: Optional[str] = None
    phone_number: Optional[str] = None
    city: Optional[str] = None
    gender: Optional[str] = None
    budget: Optional[str] = None

class LeadCreate(LeadBase):
    pass

class LeadResponse(LeadBase):
    id: int
    status: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True


class ExtractedCallData(BaseModel):
    caller_name: Optional[str] = Field(None, description="Confirmed or newly collected caller name")
    city: Optional[str] = Field(None, description="Gurgaon, Bangalore, Chennai, or Other")
    preferred_locality: Optional[str] = Field(None, description="Neighborhood e.g. Cyber City, Koramangala")
    gender_pg_type: Optional[str] = Field(None, description="Male, Female, Co-ed, Single Room, Sharing")
    monthly_budget: Optional[str] = Field(None, description="Monthly budget in INR, e.g. 15000")
    move_in_date: Optional[str] = Field(None, description="Estimated move-in date")
    stay_duration: Optional[str] = Field(None, description="Length of stay, e.g. 6 months")
    call_outcome: str = Field("interested", description="interested, busy_callback, wrong_number, not_interested")
    callback_time: Optional[str] = Field(None, description="Requested callback time or 'WhatsApp'")
    call_summary: str = Field(..., description="1-2 sentence executive summary of caller's needs")


class CallRecordResponse(BaseModel):
    id: int
    lead_id: Optional[int]
    duration_seconds: int
    transcript: List[Dict[str, Any]]
    audio_path: Optional[str]
    call_outcome: str
    extracted_data: Optional[Dict[str, Any]]
    created_at: datetime.datetime

    class Config:
        from_attributes = True

