import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_requests import CreateUserRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.db.crud.account_crud import AccountCrudDB as Account
from sqlalchemy.orm import Session


@pytest.mark.api
class TestDepositAccount:
    @pytest.mark.parametrize("amount", [1000.0, 1000.1, 8999.9, 9000.0])
    def test_deposit_account(self, api_manager: ApiManager, create_user_request: CreateUserRequest, created_account: DepositAccountRequest, db_session: Session, amount: float):
        initial_balance = created_account.balance
        deposit_account_request = DepositAccountRequest(accountId=created_account.id, amount=amount)
        response = api_manager.user_steps.deposit_account(deposit_account_request, create_user_request)

        assert response.balance == initial_balance + amount

        account_from_db = Account.get_account_by_id(db_session, response.id)
        assert account_from_db.balance == response.balance


    def test_deposit_account_by_admin(self, api_manager: ApiManager, created_account: DepositAccountRequest, db_session: Session):
        deposit_account_request = DepositAccountRequest(accountId=created_account.id, amount=5000.0)
        api_manager.admin_steps.deposit_account_as_admin(deposit_account_request)

        account_from_db = Account.get_account_by_id(db_session, created_account.id)
        assert account_from_db.balance == created_account.balance, 'Ошибка. Счет пополнен'
