import httpx
from app.config import SETU_API_KEY, SETU_BASE_URL
from app.db import db
import os

SETU_BASE_URL = os.getenv("SETU_BASE_URL", "https://your-setu-api.com")
SETU_API_KEY = os.getenv("SETU_API_KEY")

if not SETU_API_KEY:
    raise RuntimeError("SETU_API_KEY environment variable is not set")


headers = {
    "x-api-key": SETU_API_KEY,
    "Content-Type": "application/json"
}

async def initiate_linking(customer_id: str, user_id: str):
    payload = {
        "customer_id": customer_id,
        "purpose": "Personal finance",
        "redirect_url": "https://your-frontend.com/aa/success",
    }
    async with httpx.AsyncClient() as client:
        res = await client.post(f"{SETU_BASE_URL}/consents", headers=headers, json=payload)
    consent = res.json()
    await db.aa_consents.insert_one({**consent, "user_id": user_id})
    return consent["url"]

async def process_callback(data: dict):
    consent_id = data["consentId"]
    user_id = data["userId"]
    await db.bank_accounts.insert_one({
        "user_id": user_id,
        "consent_id": consent_id,
        "linked_accounts": data.get("accounts", []),
        "transactions": data.get("transactions", [])
    })

async def list_accounts(user_id: str):
    return await db.bank_accounts.find({"user_id": user_id}).to_list(None)

async def get_transactions(user_id: str, filters):
    query = {"user_id": user_id}
    if filters.account_id:
        query["linked_accounts.account_id"] = filters.account_id
    accounts = await db.bank_accounts.find(query).to_list(None)
    txns = []
    for acc in accounts:
        txns.extend(acc.get("transactions", []))
    return txns

async def refresh_data(user_id: str):
    print(f"Triggering manual refresh for user {user_id}")
    return {"message": "Data refresh initiated"}

async def disconnect_account(user_id: str, account_id: str):
    result = await db.bank_accounts.delete_one({
        "user_id": user_id,
        "linked_accounts.account_id": account_id
    })
    return result.deleted_count
