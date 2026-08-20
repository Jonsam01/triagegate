from classifier import classify_ticket

test_tickets = [
    "I was charged twice for my subscription this month, please refund the extra charge.",
    "app is weird sometimes idk",
    "How do I reset my password? I can't log into my account."
]

for ticket in test_tickets:
    result = classify_ticket(ticket)
    print(f"\nTicket: {ticket}")
    print(f"Result: {result}")
