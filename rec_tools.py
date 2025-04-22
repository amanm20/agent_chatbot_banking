import json, os
DATA = os.path.join(os.path.dirname(__file__), "..", "data")

with open(f"{DATA}/customers.json") as f:
    CUSTOMERS = {c["customer_id"]: c for c in json.load(f)}

def recommend_products(customer_id: str) -> str:
    cust = CUSTOMERS.get(customer_id)
    if not cust:
        return "❌ Customer profile not found."
    recs = []
    if cust["avg_balance"] > 10000:
        recs.append("High‑Interest Savings Account")
    if cust["monthly_spend"] > 2000:
        recs.append("Cash‑Back Rewards Credit Card")
    if not recs:
        recs = ["No special recommendations at this time."]
    lines = "\n".join(f"• {r}" for r in recs)
    return (
        "💡 Based on your profile, I recommend:\n"
        + lines
        + "\n\n(Reply “stop recommendations” to opt out.)"
    )
