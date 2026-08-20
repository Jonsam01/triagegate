import os
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from supabase import create_client
from router import validate_correction

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

supabase = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_SERVICE_KEY")
)


@app.get("/review", response_class=HTMLResponse)
def review_queue_page(request: Request):
    response = supabase.table("review_queue").select(
        "*").eq("status", "pending_review").order("created_at").execute()
    items = response.data
    return templates.TemplateResponse(request, "review.html", {"items": items})


@app.post("/review/{item_id}/approve")
def approve_item(item_id: str):
    item_response = supabase.table("review_queue").select(
        "*").eq("id", item_id).single().execute()
    item = item_response.data

    supabase.table("decisions").insert({
        "ticket_text": item["ticket_text"],
        "category": item["category"],
        "priority": item["priority"],
        "suggested_action": item["suggested_action"],
        "confidence": item["confidence"],
        "reasoning": item["reasoning"],
        "decision_type": "escalated",
        "decided_by": "human:reviewer",
        "final_outcome": "approved_as_is"
    }).execute()

    supabase.table("review_queue").update({
        "status": "resolved",
        "resolved_at": "now()"
    }).eq("id", item_id).execute()

    return RedirectResponse(url="/review", status_code=303)


@app.post("/review/{item_id}/override")
def override_item(
    item_id: str,
    category: str = Form(...),
    priority: str = Form(...),
    suggested_action: str = Form(...),
    correction_type: str = Form(...)
):
    is_valid, error = validate_correction(category, priority, correction_type)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error)

    item_response = supabase.table("review_queue").select(
        "*").eq("id", item_id).single().execute()
    item = item_response.data

    supabase.table("decisions").insert({
        "ticket_text": item["ticket_text"],
        "category": category,
        "priority": priority,
        "suggested_action": suggested_action,
        "confidence": item["confidence"],
        "reasoning": item["reasoning"],
        "decision_type": "escalated",
        "decided_by": "human:reviewer",
        "final_outcome": "overridden",
        "correction_type": correction_type
    }).execute()

    supabase.table("review_queue").update({
        "status": "resolved",
        "resolved_at": "now()"
    }).eq("id", item_id).execute()

    return RedirectResponse(url="/review", status_code=303)
