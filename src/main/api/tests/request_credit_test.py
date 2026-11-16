import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.money_generator import MoneyGenerator
from src.main.api.models.create_user_requests import CreateCreditUserRequest
from src.main.api.models.request_credit_request import RequestCreditRequest
from src.main.api.db.crud.credit_crud import CreditCrudDB as Credit
from sqlalchemy.orm import Session


@pytest.mark.api
class TestRequestCredit:
    def test_request_credit_random(self, requested_credit_account, db_session: Session):
        credit_request, response = requested_credit_account

        assert response.balance == pytest.approx(credit_request.amount), 'Баланс не равен запрошенной сумме'

        credit_from_db = Credit.get_credit_by_id(db_session, response.creditId)
        assert credit_from_db.amount == response.amount, 'Ошибка в запрашиваемой сумме'
        assert credit_from_db.term_months == response.termMonths, 'Ошибка в сроке кредита'
        assert credit_from_db.account_id == credit_request.accountId, 'Неверный аккаунт запроса кредита'


    @pytest.mark.parametrize("amount", [5000, 5001, 14999, 15000])
    def test_request_credit(self, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest,
                            created_credit_account, db_session: Session, amount: int):
        request_credit_request = RequestCreditRequest(accountId=created_credit_account.id, amount=amount, termMonths=MoneyGenerator.credit_term_months())
        response = api_manager.user_steps.request_credit(request_credit_request, create_credit_user_request)

        assert response.amount == response.balance, 'Сумма пополнения не равна запрошенной сумме'
        assert response.balance == amount, 'Сумма пополнения не равна запрошенной сумме'

        credit_from_db = Credit.get_credit_by_id(db_session, response.creditId)
        assert credit_from_db.amount == response.amount, 'Ошибка в запрашиваемой сумме'
        assert credit_from_db.term_months == response.termMonths, 'Ошибка в сроке кредита'
        assert credit_from_db.account_id == created_credit_account.id, 'Неверный аккаунт запроса кредита'


    @pytest.mark.parametrize("amount", [4999, 15001])
    def test_invalid_request_credit(self, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest,
                            created_credit_account, db_session: Session, amount: int):
        request_credit_request = RequestCreditRequest(accountId=created_credit_account.id, amount=amount, termMonths=MoneyGenerator.credit_term_months())
        response = api_manager.user_steps.invalid_limit_request_credit(request_credit_request, create_credit_user_request)

        assert response.json()["error"] is not None, 'Ошибка. Кредит выдан'