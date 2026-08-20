import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

supabase = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_SERVICE_KEY")
)


def log_decision(ticket_text: str, classification: dict, decision_type: str, decided_by: str = "system") -> dict:
    row = {
        "ticket_text": ticket_text,
        "category": classification["category"],
        "priority": classification["priority"],
        "suggested_action": classification["suggested_action"],
        "confidence": classification["confidence"],
        "reasoning": classification["reasoning"],
        "decision_type": decision_type,
        "decided_by": decided_by
    }

    response = supabase.table("decisions").insert(row).execute()
    return response.data[0]


def add_to_review_queue(decision_id: str, ticket_text: str, classification: dict) -> dict:
    row = {
        "decision_id": decision_id,
        "ticket_text": ticket_text,
        "category": classification["category"],
        "priority": classification["priority"],
        "suggested_action": classification["suggested_action"],
        "confidence": classification["confidence"],
        "reasoning": classification["reasoning"]
    }

    response = supabase.table("review_queue").insert(row).execute()
    return response.data[0]
