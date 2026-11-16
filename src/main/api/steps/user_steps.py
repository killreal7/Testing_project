from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.create_user_requests import CreateUserRequest, CreateCreditUserRequest
from src.main.api.models.repay_credit_request import RepayCreditRequest
from src.main.api.models.request_credit_request import RequestCreditRequest
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.specs.request_specs import RequestsSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestsSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_create()
        ).post()
        return response

    def deposit_account(self, deposit_account_request: DepositAccountRequest, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestsSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.request_ok()
        ).post(deposit_account_request)
        return response

    def transfer_account(self, transfer_account_request: TransferAccountRequest, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestsSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.TRANSFER_ACCOUNT,
            ResponseSpecs.request_ok()
        ).post(transfer_account_request)
        return response

    def not_found_transfer_account(self, transfer_account_request: TransferAccountRequest, create_user_request: CreateUserRequest):
        response = CrudRequester(
            RequestsSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.TRANSFER_ACCOUNT,
            ResponseSpecs.request_not_found()
        ).post(transfer_account_request)
        return response

    def create_credit_account(self, create_credit_user_request: CreateCreditUserRequest):
        response = ValidateCrudRequester(
            RequestsSpecs.auth_headers(username=create_credit_user_request.username, password=create_credit_user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_create()
        ).post()
        return response

    def request_credit(self, request_credit_request: RequestCreditRequest, create_credit_user_request: CreateCreditUserRequest):
        response = ValidateCrudRequester(
            RequestsSpecs.auth_headers(username=create_credit_user_request.username, password=create_credit_user_request.password),
            Endpoint.REQUEST_CREDIT,
            ResponseSpecs.request_create()
        ).post(request_credit_request)
        return response

    def invalid_limit_request_credit(self, request_credit_request: RequestCreditRequest, create_credit_user_request: CreateCreditUserRequest):
        response = CrudRequester(
            RequestsSpecs.auth_headers(username=create_credit_user_request.username, password=create_credit_user_request.password),
            Endpoint.REQUEST_CREDIT,
            ResponseSpecs.request_bad()
        ).post(request_credit_request)
        return response

    def repay_credit(self, repay_credit_request: RepayCreditRequest, create_credit_user_request: CreateCreditUserRequest):
        response = ValidateCrudRequester(
            RequestsSpecs.auth_headers(username=create_credit_user_request.username, password=create_credit_user_request.password),
            Endpoint.REPAY_CREDIT,
            ResponseSpecs.request_ok()
        ).post(repay_credit_request)
        return response

    def invalid_repay_credit(self, repay_credit_request: RepayCreditRequest, create_credit_user_request: CreateCreditUserRequest):
        response = CrudRequester(
            RequestsSpecs.auth_headers(username=create_credit_user_request.username, password=create_credit_user_request.password),
            Endpoint.REPAY_CREDIT,
            ResponseSpecs.request_unprocessable_entity()
        ).post(repay_credit_request)
        return response