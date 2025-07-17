from fastapi import APIRouter, Depends, Body, HTTPException
from app.auth.auth_handler import get_current_user
from app.models.bank import ConsentInitRequest, TransactionFilter
from app.services import setu_service as ss

router = APIRouter()

@router.post("/bank/aa/initiate-linking")
async def initiate_link(request: ConsentInitRequest, user=Depends(get_current_user)):
    url = await ss.initiate_linking(request.customer_id, user["_id"])
    return {"consent_url": url}

@router.post("/bank/aa/callback")
async def callback_handler(payload: dict = Body(...)):
    await ss.process_callback(payload)
    return {"message": "Callback processed"}

@router.get("/bank/accounts")
async def get_accounts(user=Depends(get_current_user)):
    accounts = await ss.list_accounts(user["_id"])
    return {"accounts": accounts}

@router.get("/bank/transactions")
async def get_txns(filters: TransactionFilter = Depends(), user=Depends(get_current_user)):
    txns = await ss.get_transactions(user["_id"], filters)
    return {"transactions": txns}

@router.post("/bank/refresh")
async def refresh(user=Depends(get_current_user)):
    return await ss.refresh_data(user["_id"])

@router.delete("/bank/disconnect/{account_id}")
async def disconnect(account_id: str, user=Depends(get_current_user)):
    deleted = await ss.disconnect_account(user["_id"], account_id)
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"message": "Account disconnected"}
