import json, os
DATA = os.path.join(os.path.dirname(__file__), "..", "data")

with open(f"{DATA}/upgrades.json") as f:
    UPGRADES = json.load(f)

def compare_upgrades(customer_id: str) -> str:
    up = UPGRADES.get(customer_id)
    if not up:
        return "❌ No upgrade info available."
    opts = up["options"]
    out = ["🔼 Upgrade Options:"]
    for o in opts:
        out.append(
            f"• {o['name']}: +${o['fee']}/mo — {o['benefit']}"
        )
    out.append("\nReply “I’d like [option name]” to proceed.")
    return "\n".join(out)
