import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_KEY")

supabase = create_client(url, key)

# Try inserting a dummy row into decisions
response = supabase.table("decisions").insert({
    "ticket_text": "Test ticket - connection check",
    "category": "other",
    "priority": "low",
    "suggested_action": "none",
    "confidence": 0.99,
    "reasoning": "This is a test row to confirm the connection works.",
    "decision_type": "auto_resolved",
    "decided_by": "system"
}).execute()

print("Insert successful!")
print(response.data)
