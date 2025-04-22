import json
from .bedrock_client import generate_text
from .data_tools import get_balance, get_transactions, ACCOUNTS
from .rag_tools import retrieve_policy
from .rec_tools import recommend_products
from .upgrade_tools import compare_upgrades

class Agent:
    def __init__(self):
        self.context = {
            "customer_id": None,
            "account_id":  None,
            "history":     []
        }

    def plan(self, user_msg: str) -> dict:
        tools_desc = [
            {"name":"GetBalance",       "args":"{account_id}"},
            {"name":"GetTransactions",  "args":"{account_id}, filter"},
            {"name":"RetrievePolicy",   "args":"{query}"},
            {"name":"RecommendProducts","args":"{customer_id}"},
            {"name":"CompareUpgrades",  "args":"{customer_id}"},
            {"name":"Answer",           "args":"{response}"}
        ]
        prompt = {
            "prompt_template": (
                "You are an AI banking assistant. You have these tools:\n"
                + "\n".join(f"{t['name']}: args {t['args']}" for t in tools_desc)
                + "\n\nMaintain context as JSON keys: customer_id, account_id.\n"
                "Given the conversation and context, choose exactly one tool and output "
                "ONLY valid JSON:\n"
                "{\n"
                "  \"tool\": <tool name>,\n"
                "  \"args\": { ... }\n"
                "}\n\n"
                f"Context: {json.dumps(self.context)}\n"
                f"History: {json.dumps(self.context['history'])}\n"
                f"User: {user_msg}\n"
                "Response→"
            )
        }
        return json.loads(generate_text(prompt["prompt_template"]))

    def handle(self, user_msg: str) -> str:
        self.context["history"].append({"user": user_msg})
        plan = self.plan(user_msg)
        tool = plan.get("tool")
        args = plan.get("args", {})

        # dispatch
        if tool == "GetBalance":
            acct = args.get("account_id") or self.context["account_id"]
            self.context["account_id"] = acct
            cust = ACCOUNTS.get(acct, {}).get("customer_id")
            self.context["customer_id"] = cust
            out = get_balance(acct)

        elif tool == "GetTransactions":
            acct   = self.context["account_id"]
            filt   = args.get("filter")
            out    = get_transactions(acct, filter=filt)

        elif tool == "RetrievePolicy":
            out = retrieve_policy(args.get("query",""))

        elif tool == "RecommendProducts":
            cid = self.context["customer_id"]
            out = recommend_products(cid)

        elif tool == "CompareUpgrades":
            cid = self.context["customer_id"]
            out = compare_upgrades(cid)

        elif tool == "Answer":
            out = args.get("response","")

        else:
            out = "❓ Sorry, I didn’t understand that."

        self.context["history"].append({"assistant": out})
        return out

agent = Agent()
