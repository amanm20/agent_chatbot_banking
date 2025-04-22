import json, os
DATA = os.path.join(os.path.dirname(__file__), "..", "data")

with open(f"{DATA}/accounts.json") as f:
    ACC = {a["account_id"]: a for a in json.load(f)}

with open(f"{DATA}/transactions.json") as f:
    TXNS = json.load(f)

def get_balance(acct_id: str) -> str:
    a = ACC.get(acct_id)
    if not a: return f"❌ Account {acct_id} not found."
    return (
      f"✅ Your {a['type']} account ({a['number']}) balance is "
      f"${a['balance']:.2f}."
    )

def get_transactions(acct_id: str, n: int=5, tx_type: str=None) -> str:
    hist = [t for t in TXNS if t["account_id"] == acct_id]
    if tx_type:
        if tx_type.lower()=="deposits":
            hist = [t for t in hist if t["amount"]>0]
        elif tx_type.lower()=="withdrawals":
            hist = [t for t in hist if t["amount"]<0]
    last = sorted(hist, key=lambda t: t["date"], reverse=True)[:n]
    if not last:
        return "ℹ️ No transactions found."
    lines = [f"{t['date']}: {t['merchant']} {t['amount']:+.2f}" for t in last]
    return "🧾 Recent transactions:\n" + "\n".join(lines)
