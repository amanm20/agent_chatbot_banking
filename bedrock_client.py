import os, json, boto3
from dotenv import load_dotenv

load_dotenv()
bedrock = boto3.client(
    "bedrock-runtime",
    region_name=os.environ["AWS_REGION"],
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"]
)
MODEL = os.environ["BEDROCK_MODEL"]

def generate_text(prompt: str) -> str:
    resp = bedrock.invoke_model(
        modelId=MODEL,
        contentType="application/json",
        accept="application/json",
        body=json.dumps({"prompt": prompt})
    )
    return json.loads(resp["body"])["completion"]

def embed_text(text: str) -> list:
    # assume MODEL supports embed if you choose an embed model, else swap in SageMaker, etc.
    resp = bedrock.invoke_model(
        modelId=os.environ["EMBED_MODEL"],
        contentType="application/json",
        accept="application/json",
        body=json.dumps({"text": text})
    )
    return json.loads(resp["body"])["embedding"]
