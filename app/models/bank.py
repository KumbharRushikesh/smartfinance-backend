from pydantic import BaseModel
from typing import Optional

class ConsentInitRequest(BaseModel):
    customer_id: str  # e.g., phone or account number

class TransactionFilter(BaseModel):
    account_id: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    txn_type: Optional[str] = None  # credit/debit
