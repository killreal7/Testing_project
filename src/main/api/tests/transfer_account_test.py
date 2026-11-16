import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.money_generator import MoneyGenerator
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_requests import CreateUserRequest
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.db.crud.account_crud import AccountCrudDB as Account
from sqlalchemy.orm import Session


@pytest.mark.api
class TestTransferAccount:
    @pytest.mark.parametrize("amount", [500.0, 500.1, 9999.9, 10000.0])
    def test_transfer_account(self, api_manager: ApiManager, created_account: CreateUserRequest, funded_account: CreateUserRequest,
                              create_user_request: CreateUserRequest, db_session: Session, amount: float):
        transfer_account_request = TransferAccountRequest(fromAccountId=funded_account.id, toAccountId=created_account.id, amount=amount)
        response = api_manager.user_steps.transfer_account(transfer_account_request, create_user_request)

        assert response.fromAccountIdBalance == pytest.approx(funded_account.balance - amount), 'Ошибка. Неверная сумма списания'

        account_from_db = Account.get_account_by_id(db_session, response.fromAccountId)
        assert account_from_db.balance == round(response.fromAccountIdBalance, 2), 'Неверный баланс в БД'

        account_from_db = Account.get_account_by_id(db_session, response.toAccountId)
        assert account_from_db.balance == created_account.balance + amount, 'Ошибка. Неверная сумма поступления'


    def test_not_found_transfer_account(self, api_manager: ApiManager, created_account: CreateAccountResponse,
                              funded_account: CreateAccountResponse, create_user_request: CreateUserRequest,
                              db_session: Session):
        transfer_account_request = TransferAccountRequest(fromAccountId=funded_account.id,
                                                          toAccountId=777, amount=MoneyGenerator.valid_transfer_amount())
        api_manager.user_steps.not_found_transfer_account(transfer_account_request, create_user_request)

        account_from_db = Account.get_account_by_id(db_session, funded_account.id)
        assert account_from_db.balance == pytest.approx(funded_account.balance), 'Ошибка. У пользователя списались деньги'