from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.create_user_requests import CreateUserRequest, CreateCreditUserRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.specs.request_specs import RequestsSpecs
from src.main.api.steps.base_steps import BaseSteps
from src.main.api.foundation.endpoint import Endpoint


class AdminSteps(BaseSteps):
    def create_user(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestsSpecs.auth_headers(username="admin", password="123456"),
            Endpoint.ADMIN_CREATE_USER,
            ResponseSpecs.request_ok()
        ).post(create_user_request)

        self.created_obj.append(response)
        return response

    def delete_user(self, user_id: int):
        CrudRequester(
            RequestsSpecs.auth_headers(username="admin", password="123456"),
            Endpoint.ADMIN_DELETE_USER,
            ResponseSpecs.request_ok()
        ).delete(user_id)

    def create_invalid_user(self, create_user_request: CreateUserRequest):
        CrudRequester(
            RequestsSpecs.auth_headers(username="admin", password="123456"),
            Endpoint.ADMIN_CREATE_USER,
            ResponseSpecs.request_bad()
        ).post(create_user_request)

    def login_user(self, login_user_request: LoginUserRequest):
        response = ValidateCrudRequester(
            RequestsSpecs.unauth_headers(),
            Endpoint.LOGIN_USER,
            ResponseSpecs.request_ok()
        ).post(login_user_request)
        return response

    def create_credit_user(self, create_credit_user_request: CreateCreditUserRequest):
        response = ValidateCrudRequester(
            RequestsSpecs.auth_headers(username="admin", password="123456"),
            Endpoint.ADMIN_CREATE_USER,
            ResponseSpecs.request_ok()
        ).post(create_credit_user_request)

        self.created_obj.append(response)
        return response

    def deposit_account_as_admin(self, deposit_account_request: DepositAccountRequest):
        response = CrudRequester(
            RequestsSpecs.auth_headers(username="admin", password="123456"),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.request_forbidden()
        ).post(deposit_account_request)
        return response
