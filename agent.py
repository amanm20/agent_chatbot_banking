from .intent import parse_intent
from .data_tools import get_balance, get_transactions
from .rag_tools import retrieve_policy
from .rec_tools import recommend_products
from .upgrade_tools import compare_upgrades

class Agent:
    def __init__(self):
        self.context = {"customer_id":"CUST-0001","account_id":None,"last_intent":None}

    def handle(self, message: str) -> str:
        intent = parse_intent(message, self.context)
        nm = intent["name"]
        self.context["last_intent"] = nm

        if nm=="off_topic":
            return "❓ I’m here to help with banking only. Try asking about your balance, transactions, policies, or product services."

        if nm=="balance":
            ac = intent.get("account_id") or self.context["account_id"] or "ACC-1001"
            self.context["account_id"] = ac
            return get_balance(ac)

        if nm=="transactions":
            ac = self.context["account_id"] or "ACC-1001"
            filt = intent.get("filter")
            return get_transactions(ac, n=5, tx_type=filt)

        if nm in ("policy_query","explain_policy"):
            return retrieve_policy(intent["query"])

        if nm=="recommend_product":
            return recommend_products(self.context["customer_id"])

        if nm=="service_upgrade":
            return compare_upgrades(self.context["customer_id"])

        # fallback
        return "🤔 Sorry, I didn’t catch that. You can ask about your balance, transactions, bank policies, or product recommendations."

agent = Agent()
