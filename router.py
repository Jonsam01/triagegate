CONFIDENCE_THRESHOLD = 0.80


def route_decision(classification: dict) -> str:
    """
    Takes a classification dict (from classify_ticket) and decides
    whether it should be auto-resolved or escalated to human review.

    Returns either "auto_resolved" or "escalated".
    """
    confidence = classification.get("confidence", 0.0)

    if confidence >= CONFIDENCE_THRESHOLD:
        return "auto_resolved"
    else:
        return "escalated"


VALID_CATEGORIES = {"billing", "technical",
                    "account_access", "feature_request", "complaint", "other"}
VALID_PRIORITIES = {"low", "medium", "high", "urgent"}
VALID_CORRECTION_TYPES = {"category_corrected", "priority_corrected",
                          "action_corrected", "confidence_miscalibrated", "multiple"}


def validate_correction(category: str, priority: str, correction_type: str) -> tuple[bool, str]:
    """
    Validates a human override submission before it's written to the audit log.
    Returns (is_valid, error_message).
    """
    if category not in VALID_CATEGORIES:
        return False, f"Invalid category: {category}"

    if priority not in VALID_PRIORITIES:
        return False, f"Invalid priority: {priority}"

    if correction_type not in VALID_CORRECTION_TYPES:
        return False, f"Invalid correction_type: {correction_type}"

    return True, ""
