TriageGate

A confidence-gated support ticket triage system. Instead of blindly trusting every LLM classification, TriageGate scores its own confidence on every decision,  auto-resolving what it's sure about and routing anything uncertain to a human review queue with a full, immutable audit trail.

Live demo: [triagegate-production.up.railway.app/review](https://triagegate-production.up.railway.app/review)

 ## Why this exists

Most AI automation demos show a model making a call and moving on. This project asks a different question: **what happens when the model isn't sure?** TriageGate is built around the idea that production AI systems need a safety net — a way to catch uncertain decisions before they reach a customer, and a permanent record of every decision (human or system) that was ever made.

 ## How it works:
Ticket intake
→ Groq classification (category, priority, suggested action, confidence, reasoning)
→ Confidence-threshold router
≥ 0.80 confidence → auto-resolved, logged
< 0.80 confidence → escalated to review queue, logged
→ Human review interface
Approve → confirms the model's original call
Override → corrects category/priority/action, tags what was wrong
→ Immutable audit log (every decision, human or system, permanently recorded)
→ Analytics: auto-resolve rate, override rate, recurring correction patterns

 ## Results from test batch

- 32 tickets processed
- 50% auto-resolved on high confidence
- 25% escalated for human review
- 25% override rate on reviewed tickets — proof the confidence-gating catches genuine uncertainty, not just decorative thresholds
- Recurring pattern surfaced: the model occasionally buries a secondary issue (e.g. a billing complaint embedded in a technical-sounding ticket) under the primary category — a concrete, specific insight for prompt refinement, not just a vague "it's not perfect."

## Tech stack

- Python 3.11+
- FastAPI — intake endpoint, review interface
- Groq (openai/gpt-oss-20b) — classification with structured confidence scoring
- Supabase (PostgreSQL) — immutable audit log (`decisions`) and pending review queue (`review_queue`)
- Jinja2 — server-rendered review interface
- pytest — unit tests on routing and correction-validation logic
- GitHub Actions — CI, running the full test suite on every push

 ## Key design decisions

- Confidence is a float, not a label. This makes the routing threshold tunable without changing the data schema.
- The model must always explain its reasoning, not just output a category. This is what a human reviewer actually reads before approving or overriding.
- The audit log is append-only. A human override never edits the original system decision — it writes a new row. This means the full decision history is always reconstructable, not just the final state.
- Correction data is structured, not free-text.** Every override captures *what* was wrong (category, priority, action, or confidence calibration itself), which is what makes pattern analysis across corrections possible.

## Running locally

```bash
git clone https://github.com/Jonsam01/triagegate.git
cd triagegate
python -m venv venv
venv\Scripts\Activate.ps1   # Windows
pip install -r requirements.txt
```

Create a `.env` file with:

Run the test suite:
```bash
pytest tests/ -v
```

Start the review interface:
```bash
uvicorn main:app --reload
```

Visit `http://127.0.0.1:8000/review`

## Status

## Status

Core system, feedback loop, tests, and CI are complete. Deployed and live on Railway.

## Author

Built by [John Samuel](https://github.com/Jonsam01) — automation engineer
