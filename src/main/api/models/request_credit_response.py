from src.main.api.models.base_model import BaseModel


class RequestCreditResponse(BaseModel):
    id: int
    amount: int
    termMonths: int
    balance: int
    creditId: int