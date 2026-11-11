import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_requests import CreateCreditUserRequest
from src.main.api.models.repay_credit_request import RepayCreditRequest
from src.main.api.db.crud.credit_crud import CreditCrudDB as Credit
from sqlalchemy.orm import Session


@pytest.mark.api
class TestRepayCredit:
    def test_repay_credit(self, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest, requested_credit_account, db_session: Session):
        repay_credit_request = RepayCreditRequest(creditId=requested_credit_account.creditId,accountId=requested_credit_account.id, amount=8000)
        response = api_manager.user_steps.repay_credit(repay_credit_request, create_credit_user_request)

        assert response.amountDeposited == 8000

        credit_from_db = Credit.get_credit_by_id(db_session, response.creditId)
        assert credit_from_db.amount == response.amountDeposited
        assert credit_from_db.balance == 0


    def test_invalid_repay_credit(self, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest, requested_credit_account, db_session: Session):
        repay_credit_request = RepayCreditRequest(creditId=requested_credit_account.creditId,accountId=requested_credit_account.id, amount=7000)
        api_manager.user_steps.invalid_repay_credit(repay_credit_request, create_credit_user_request)

        credit_from_db = Credit.get_credit_by_id(db_session, requested_credit_account.creditId)
        assert credit_from_db.balance != 0, 'Ошибка. Кредит погашен'