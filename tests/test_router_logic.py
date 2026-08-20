from router import route_decision, CONFIDENCE_THRESHOLD, validate_correction
import sys
import os

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


def test_high_confidence_auto_resolves():
    classification = {"confidence": 0.95}
    assert route_decision(classification) == "auto_resolved"


def test_low_confidence_escalates():
    classification = {"confidence": 0.3}
    assert route_decision(classification) == "escalated"


def test_confidence_at_exact_threshold_auto_resolves():
    classification = {"confidence": CONFIDENCE_THRESHOLD}
    assert route_decision(classification) == "auto_resolved"


def test_confidence_just_below_threshold_escalates():
    classification = {"confidence": CONFIDENCE_THRESHOLD - 0.01}
    assert route_decision(classification) == "escalated"


def test_zero_confidence_escalates():
    classification = {"confidence": 0.0}
    assert route_decision(classification) == "escalated"


def test_perfect_confidence_auto_resolves():
    classification = {"confidence": 1.0}
    assert route_decision(classification) == "auto_resolved"


def test_missing_confidence_defaults_to_escalated():
    classification = {}
    assert route_decision(classification) == "escalated"


def test_valid_correction_passes():
    is_valid, error = validate_correction(
        "billing", "high", "category_corrected")
    assert is_valid is True
    assert error == ""


def test_invalid_category_fails():
    is_valid, error = validate_correction(
        "not_a_real_category", "high", "category_corrected")
    assert is_valid is False
    assert "Invalid category" in error


def test_invalid_priority_fails():
    is_valid, error = validate_correction(
        "billing", "super_urgent", "category_corrected")
    assert is_valid is False
    assert "Invalid priority" in error


def test_invalid_correction_type_fails():
    is_valid, error = validate_correction(
        "billing", "high", "not_a_real_reason")
    assert is_valid is False
    assert "Invalid correction_type" in error
