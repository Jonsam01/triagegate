import os
from collections import Counter
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

supabase = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_SERVICE_KEY")
)


def run_analytics():
    response = supabase.table("decisions").select("*").execute()
    all_decisions = response.data

    queue_response = supabase.table("review_queue").select("status").execute()
    all_queue_items = queue_response.data

    total = len(all_decisions)
    auto_resolved = [
        d for d in all_decisions if d["decision_type"] == "auto_resolved"]
    escalated_original = [d for d in all_decisions if d["decision_type"]
                          == "escalated" and d["decided_by"] == "system"]
    human_decisions = [
        d for d in all_decisions if d["decided_by"] == "human:reviewer"]

    approved_as_is = [d for d in human_decisions if d.get(
        "final_outcome") == "approved_as_is"]
    overridden = [d for d in human_decisions if d.get(
        "final_outcome") == "overridden"]

    still_pending = [
        q for q in all_queue_items if q["status"] == "pending_review"]

    print("=" * 50)
    print("TRIAGEGATE — DECISION ANALYTICS")
    print("=" * 50)
    print(f"\nTotal tickets processed: {total}")
    print(
        f"Auto-resolved: {len(auto_resolved)} ({len(auto_resolved)/total*100:.1f}%)")
    print(
        f"Escalated to review: {len(escalated_original)} ({len(escalated_original)/total*100:.1f}%)")

    print(f"\n--- Of escalated tickets ---")
    print(f"Approved as-is by human: {len(approved_as_is)}")
    print(f"Overridden by human: {len(overridden)}")
    print(f"Still pending in queue: {len(still_pending)}")

    reviewed = len(approved_as_is) + len(overridden)
    if reviewed > 0:
        override_rate = len(overridden) / reviewed * 100
        print(
            f"\nOverride rate: {override_rate:.1f}% of reviewed tickets were corrected")

    if overridden:
        print(f"\n--- Recurring correction patterns ---")
        correction_counts = Counter(d.get("correction_type")
                                    for d in overridden if d.get("correction_type"))
        for correction_type, count in correction_counts.most_common():
            print(f"{correction_type}: {count} time(s)")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    run_analytics()
