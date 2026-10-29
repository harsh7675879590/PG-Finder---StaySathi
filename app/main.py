import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.database import init_db, SessionLocal
from app.models import Lead
from app.api.routes_leads import router as leads_router
from app.api.routes_calls import router as calls_router
from app.api.routes_voice import router as voice_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Production-grade Voice AI Agent for PG Finder lead qualification."
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount recordings storage as static directory
app.mount("/storage/recordings", StaticFiles(directory=settings.RECORDINGS_DIR), name="recordings")

# Mount templates
TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Register API Routers
app.include_router(leads_router)
app.include_router(calls_router)
app.include_router(voice_router)

@app.on_event("startup")
def on_startup():
    init_db()
    # Seed default sample leads if table empty
    db = SessionLocal()
    try:
        if db.query(Lead).count() == 0:
            sample_leads = [
                Lead(customer_name="Harsh", phone_number="+91 98112 34567", city="Gurgaon", gender="Male", budget=None, status="NEW"),
                Lead(customer_name=None, phone_number="+91 97234 56789", city=None, gender=None, budget=None, status="NEW"),
                Lead(customer_name="Rohan Verma", phone_number="+91 99887 76655", city="Bangalore", gender="Male", budget="18000", status="NEW")
            ]
            db.add_all(sample_leads)
            db.commit()
    finally:
        db.close()

@app.get("/")
def serve_dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "project_name": settings.PROJECT_NAME})
