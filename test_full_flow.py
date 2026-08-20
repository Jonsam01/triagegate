from classifier import classify_ticket
from router import route_decision
from audit_log import log_decision, add_to_review_queue

test_tickets = [
    # Clear billing issues
    "I was charged twice for my subscription this month, please refund the extra charge.",
    "My invoice shows $49 but I signed up for the $29 plan. Please fix this.",
    "Can I get a receipt for my last payment? I need it for expense reporting.",

    # Clear technical issues
    "The app crashes every time I try to upload a file larger than 10MB.",
    "Dashboard is showing a blank white screen since this morning's update.",
    "API requests are returning 500 errors intermittently since yesterday.",

    # Clear account access
    "How do I reset my password? I can't log into my account.",
    "I'm locked out after too many failed login attempts, please help.",
    "Need to update the email address on my account, the old one is deactivated.",

    # Clear feature requests
    "Would love to see dark mode added to the mobile app.",
    "Can you add CSV export to the reports page?",

    # Clear complaints
    "Your support team took 5 days to respond to my last ticket, that's unacceptable.",
    "I've been a customer for 2 years and the service quality has really dropped.",

    # Genuinely ambiguous / vague
    "app is weird sometimes idk",
    "the thing broke again ugh",
    "nothing works anymore??",
    "this is annoying can someone fix",
    "nvm figured it out actually wait no still broken",
    "nothing loads and also I think I was charged wrong but not sure",
    "nothing happens when I click the button, or maybe it's my wifi",
]

for ticket in test_tickets:
    classification = classify_ticket(ticket)
    decision_type = route_decision(classification)

    logged = log_decision(ticket, classification, decision_type)
    print(f"\nTicket: {ticket}")
    print(
        f"Decision: {decision_type} (confidence: {classification['confidence']})")
    print(f"Logged with id: {logged['id']}")

    if decision_type == "escalated":
        queued = add_to_review_queue(logged["id"], ticket, classification)
        print(f"Added to review queue with id: {queued['id']}")
test_tickets = [
    "app is weird sometimes idk",
    "nothing works and idk why",
]
