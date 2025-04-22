import re

OFF_TOPIC = ["weather","movie","football","weed","sport","bitcoin"]

def parse_intent(msg: str, ctx: dict) -> dict:
    m = msg.lower()
    # Off‑topic
    if any(word in m for word in OFF_TOPIC):
        return {"name":"off_topic"}

    # Balance
    if re.search(r"\b(balance|what.*balance|how much.*have)\b", m):
        acct = re.search(r"(checking|savings)", m)
        return {"name":"balance", "account_id": f"ACC-1{ '001' if not acct else '002' }"}

    # Transactions
    if re.search(r"\b(transactions|history|spent|deposits|withdrawals)\b", m):
        filt = "deposits" if "deposit" in m else "withdrawals" if "withdrawal" in m else None
        return {"name":"transactions", "filter":filt}

    # Policy query
    if re.search(r"\b(fee|agreement|policy|procedure|terms)\b", m):
        # differentiate “explain” vs factual
        if "explain" in m or "mean" in m:
            return {"name":"explain_policy", "query":msg}
        else:
            return {"name":"policy_query", "query":msg}

    # Recommendations
    if re.search(r"\b(recommend|suggest)\b.*(product|account|card)\b", m):
        return {"name":"recommend_product"}

    # Service upgrades
    if re.search(r"\b(upgrade|premium|tier)\b", m):
        return {"name":"service_upgrade"}

    # Follow‑up context: “last month”, “that account”
    if "last month" in m or "that account" in m:
        return {"name":ctx.get("last_intent","balance")}

    # Default fallback
    return {"name":"fallback"}
