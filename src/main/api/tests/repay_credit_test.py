import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_requests import CreateCreditUserRequest
from src.main.api.models.repay_credit_request import RepayCreditRequest
from src.main.api.db.crud.credit_crud import CreditCrudDB as Credit
from sqlalchemy.orm import Session


@pytest.mark.api
class TestRepayCredit:
    def test_repay_credit(self, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest,
                          requested_credit_account, db_session: Session):
        credit_request, credit_response = requested_credit_account
        repay_credit_request = RepayCreditRequest(creditId=credit_response.creditId,accountId=credit_response.id,
                                                  amount=credit_request.amount)
        response = api_manager.user_steps.repay_credit(repay_credit_request, create_credit_user_request)

        assert response.amountDeposited == pytest.approx(credit_request.amount), 'Ошибка в сумме погашения кредита'

        credit_from_db = Credit.get_credit_by_id(db_session, response.creditId)
        assert credit_from_db.amount == response.amountDeposited, 'Ошибка во внесенной сумме'
        assert credit_from_db.balance == 0, 'Ошибка. Деньги не поступили на счет'


    def test_invalid_repay_credit(self, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest,
                                  requested_credit_account, db_session: Session):
        credit_request, credit_response = requested_credit_account
        repay_credit_request = RepayCreditRequest(creditId=credit_response.creditId,accountId=credit_response.id,
                                                  amount=credit_request.amount - 1)
        api_manager.user_steps.invalid_repay_credit(repay_credit_request, create_credit_user_request)

        credit_from_db = Credit.get_credit_by_id(db_session, credit_response.creditId)
        assert credit_from_db.balance != 0, 'Ошибка. Кредит погашен'