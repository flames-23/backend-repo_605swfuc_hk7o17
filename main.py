import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from database import db, create_document, get_documents
from schemas import Event, Registration

app = FastAPI(title="FESdmiT API", description="College Event Registration Portal Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "FESdmiT Backend is running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    # Env vars
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

# --------- Events Endpoints ---------

@app.post("/api/events", response_model=dict)
async def create_event(event: Event):
    try:
        event_data = event.model_dump()
        event_id = create_document("event", event_data)
        return {"id": event_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/events", response_model=List[dict])
async def list_events(tag: Optional[str] = None):
    try:
        filter_dict = {"tags": {"$in": [tag]}} if tag else {}
        events = get_documents("event", filter_dict)
        # Convert ObjectId to str
        for ev in events:
            if "_id" in ev:
                ev["id"] = str(ev.pop("_id"))
            # datetime serialization
            if isinstance(ev.get("date"), datetime):
                ev["date"] = ev["date"].isoformat()
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --------- Registrations Endpoints ---------

@app.post("/api/registrations", response_model=dict)
async def register_for_event(reg: Registration):
    try:
        reg_data = reg.model_dump()
        reg_id = create_document("registration", reg_data)
        return {"id": reg_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/registrations", response_model=List[dict])
async def list_registrations(event_id: Optional[str] = None, email: Optional[str] = None):
    try:
        filter_dict = {}
        if event_id:
            filter_dict["event_id"] = event_id
        if email:
            filter_dict["email"] = email
        regs = get_documents("registration", filter_dict)
        for r in regs:
            if "_id" in r:
                r["id"] = str(r.pop("_id"))
            for dt_field in ["created_at", "updated_at"]:
                if isinstance(r.get(dt_field), datetime):
                    r[dt_field] = r[dt_field].isoformat()
        return regs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
