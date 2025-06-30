from pydantic import BaseModel, Field
from typing import List

class ExchangeTokenRequest(BaseModel):
    public_token: str
    institution_name: str  # e.g., "BOB", "SBI"

class BankAccountOut(BaseModel):
    id: str
    institution_name: str
