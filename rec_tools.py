import json, os
DATA = os.path.join(os.path.dirname(__file__), "..", "data")
with open(f"{DATA}/customers.json") as f:
    CUST = {c["customer_id"]: c for c in json.load(f)}
with open(f"{DATA}/products.json") as f:
    PRODS = json.load(f)

def recommend_products(customer_id: str) -> str:
    c = CUST.get(customer_id)
    if not c:
        return "Profile not found."
    recs = []
    if c["avg_balance"] > 10000:
        recs.append("High‑interest savings account")
    if c["monthly_spend"] > 2000:
        recs.append("Cash‑back rewards credit card")
    if not recs:
        recs = ["No special recommendations at this time."]
    lines = [f"• {p}" for p in recs]
    return (
      "Based on your profile, I recommend:\n"
      + "\n".join(lines)
      + "\n\nI can opt you out anytime—just say “no more recommendations.”"
    )
