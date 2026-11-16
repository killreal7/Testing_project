import pytest
from src.main.api.models.create_user_requests import CreateUserRequest, CreateCreditUserRequest
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.request_credit_request import RequestCreditRequest
from src.main.api.generators.money_generator import MoneyGenerator


@pytest.fixture
def create_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def created_account(api_manager, create_user_request):
    account = api_manager.user_steps.create_account(create_user_request)
    return account

@pytest.fixture
def funded_account(api_manager, create_user_request):
    account = api_manager.user_steps.create_account(create_user_request)
    deposit_request = DepositAccountRequest(accountId=account.id, amount=MoneyGenerator.max_deposit_amount())
    api_manager.user_steps.deposit_account(deposit_request, create_user_request)
    deposit_request = DepositAccountRequest(accountId=account.id, amount=MoneyGenerator.valid_deposit_amount())
    deposit_response = api_manager.user_steps.deposit_account(deposit_request, create_user_request)
    account.balance = deposit_response.balance
    return account

@pytest.fixture
def create_credit_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateCreditUserRequest)
    api_manager.admin_steps.create_credit_user(user_request)
    return user_request

@pytest.fixture
def created_credit_account(api_manager, create_credit_user_request):
    account = api_manager.user_steps.create_credit_account(create_credit_user_request)
    return account

@pytest.fixture
def requested_credit_account(api_manager, create_credit_user_request, created_credit_account):
    request_credit = RequestCreditRequest(accountId=created_credit_account.id, amount=MoneyGenerator.valid_credit_amount(),
                                          termMonths=MoneyGenerator.credit_term_months())
    credit = api_manager.user_steps.request_credit(request_credit, create_credit_user_request)
    return request_credit, credit