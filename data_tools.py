import json, os
DATA = os.path.join(os.path.dirname(__file__), "..", "data")

with open(f"{DATA}/accounts.json") as f:
    ACCOUNTS = {a["account_id"]: a for a in json.load(f)}
with open(f"{DATA}/transactions.json") as f:
    TXNS = json.load(f)

def get_balance(account_id: str) -> str:
    acct = ACCOUNTS.get(account_id)
    if not acct:
        return f"❌ Account {account_id} not found."
    return (
        f"✅ {acct['type'].title()} Account {acct['number']} "
        f"Balance: ${acct['balance']:.2f}"
    )

def get_transactions(account_id: str, n: int=5, tx_type: str=None) -> str:
    history = [t for t in TXNS if t["account_id"] == account_id]
    if tx_type:
        if tx_type.lower() == "deposits":
            history = [t for t in history if t["amount"] > 0]
        elif tx_type.lower() in ("withdrawals","debits"):
            history = [t for t in history if t["amount"] < 0]
    last_n = sorted(history, key=lambda t: t["date"], reverse=True)[:n]
    if not last_n:
        return "ℹ️ No transactions found."
    lines = [f"{t['date']}: {t['merchant']} {t['amount']:+.2f}" for t in last_n]
    return "🧾 Recent transactions:\n" + "\n".join(lines)
