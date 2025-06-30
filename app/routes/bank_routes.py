from fastapi import APIRouter, Depends, HTTPException
from app.auth.auth_handler import get_current_user
from app.services import plaid_service
from app.models.bank import ExchangeTokenRequest, BankAccountOut
from app.db import db
from bson import ObjectId

router = APIRouter()

@router.get("/bank/link-token")
async def get_link_token(user=Depends(get_current_user)):
    token = await plaid_service.create_link_token(user["id"])
    return {"link_token": token}

@router.post("/bank/exchange-token")
async def exchange_token(payload: ExchangeTokenRequest, user=Depends(get_current_user)):
    access_token, item_id = await plaid_service.exchange_public_token(payload.public_token)
    await db.bank_accounts.insert_one({
        "user_id": user["id"],
        "access_token": access_token,
        "item_id": item_id,
        "institution_name": payload.institution_name
    })
    return {"message": "Bank account linked"}

@router.get("/bank/accounts")
async def list_user_banks(user=Depends(get_current_user)):
    banks = await db.bank_accounts.find({"user_id": user["id"]}).to_list(None)
    return [{"id": str(bank["_id"]), "institution_name": bank["institution_name"]} for bank in banks]

@router.get("/bank/transactions/{bank_id}")
async def get_transactions_by_bank(bank_id: str, user=Depends(get_current_user)):
    bank = await db.bank_accounts.find_one({"_id": ObjectId(bank_id), "user_id": user["id"]})
    if not bank:
        raise HTTPException(status_code=404, detail="Bank account not found")
    txns = await plaid_service.fetch_transactions(bank["access_token"])
    return {"transactions": txns}
