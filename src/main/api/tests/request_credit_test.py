import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_requests import CreateCreditUserRequest
from src.main.api.models.request_credit_request import RequestCreditRequest
from src.main.api.db.crud.credit_crud import CreditCrudDB as Credit
from sqlalchemy.orm import Session


@pytest.mark.api
class TestRequestCredit:
    @pytest.mark.parametrize("amount", [5000, 5001, 14999, 15000])
    def test_request_credit(self, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest, created_credit_account, db_session: Session,amount: int):
        request_credit_request = RequestCreditRequest(accountId=created_credit_account.id, amount=amount, termMonths=12)
        response = api_manager.user_steps.request_credit(request_credit_request, create_credit_user_request)

        assert response.amount == response.balance
        assert response.balance == amount

        credit_from_db = Credit.get_credit_by_id(db_session, response.creditId)
        assert credit_from_db.amount == response.amount
        assert credit_from_db.term_months == response.termMonths
        assert credit_from_db.account_id == created_credit_account.id


    @pytest.mark.parametrize("amount", [4999, 15001])
    def test_invalid_request_credit(self, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest,
                            created_credit_account, db_session: Session, amount: int):
        request_credit_request = RequestCreditRequest(accountId=created_credit_account.id, amount=amount, termMonths=12)
        response = api_manager.user_steps.invalid_limit_request_credit(request_credit_request, create_credit_user_request)

        assert response.json()["error"] is not None, 'Ошибка. Кредит выдан'