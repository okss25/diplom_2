import requests
import pytest
import allure

from data import UsersData
from helper import create_random_email, create_random_password, create_random_username
from urls import Urls


class TestRegistration:
    @allure.title('Проверка успешной регистрации аккаунта с валидными данными')
    @allure.description
    def test_registration_new_account_success_submit(self):
        payload = {
            'email': create_random_email(),
            'password': create_random_password(),
            'name': create_random_username()
        }
        response = requests.post(Urls.user_register, data=payload)
        deserials = response.json()
        assert response.status_code == 200
        assert deserials['success'] is True
        assert 'accessToken' in deserials.keys()
        assert 'refreshToken' in deserials.keys()
        assert deserials['user']['email'] == payload['email']
        assert deserials['user']['name'] == payload['name']

        access_token = deserials['accessToken']
        requests.delete(Urls.user_delete, headers={'Authorization': access_token})

    @allure.title('Проверка ответа на запрос регистрации с незаполненным обязательным полем')
    @allure.description
    @pytest.mark.parametrize('credentials', UsersData.credentials_with_empty_field)
    def test_registration_one_required_field_is_empty_failed_submit(self, credentials):
        response = requests.post(Urls.user_register, data=credentials)
        assert (response.status_code == 403 and response.json() ==
                {'success': False, 'message': 'Email, password and name are required fields'})

    @allure.title('Проверка ответа на запрос регистрации с существующим в базе email')
    @allure.description
    def test_registration_login_taken_failed_submit(self):
        payload = {
            'email': UsersData.email,
            'password': create_random_password(),
            'name': create_random_username()
        }
        response = requests.post(Urls.user_register, data=payload)
        assert response.status_code == 403 and response.json() == {'success': False, 'message': 'User already exists'}