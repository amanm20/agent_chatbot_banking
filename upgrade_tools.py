import json, os
DATA = os.path.join(os.path.dirname(__file__), "..", "data")
with open(f"{DATA}/upgrades.json") as f:
    UPGR = json.load(f)

def compare_upgrades(customer_id: str) -> str:
    # simplistic: look up UPG[r][customer_id]
    tier = UPGR.get(customer_id, {})
    if not tier:
        return "No upgrade options found."
    out = ["Upgrade options:"]
    for opt in tier["options"]:
        out.append(f"• {opt['name']}: +${opt['fee']}/mo → {opt['benefit']}")
    out.append("\nNext steps: reply “I’d like {tier}” or “more info.”")
    return "\n".join(out)
