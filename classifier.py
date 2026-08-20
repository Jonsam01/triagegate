import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a support ticket triage assistant. Given a customer support ticket, classify it and respond ONLY with valid JSON in this exact format, with no other text:

{
  "category": "billing" | "technical" | "account_access" | "feature_request" | "complaint" | "other",
  "priority": "low" | "medium" | "high" | "urgent",
  "suggested_action": "a short string describing the recommended next step",
  "confidence": a float between 0.0 and 1.0 representing how confident you are in this classification,
  "reasoning": "a 1-2 sentence explanation of why you chose this classification"
}

Be honest about your confidence. If the ticket is ambiguous, vague, or could reasonably fall into multiple categories, give it a LOWER confidence score rather than guessing."""


def classify_ticket(ticket_text: str) -> dict:
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": ticket_text}
        ],
        response_format={"type": "json_object"},
        temperature=0.2
    )

    result = json.loads(response.choices[0].message.content)
    return result
