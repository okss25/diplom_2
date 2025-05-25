import allure
import requests

from data import UsersData
from helper import create_random_email, create_random_password
from urls import Urls

class TestAuthentication:
    @allure.title('Проверка успешной аутентификации пользователя при создании аккаунта')
    @allure.description('Аккаунт для проверки создается фикстурой и удаляется после.')
    def test_auth_existing_account_success(self, create_new_user_and_delete):
        payload = create_new_user_and_delete[0]
        with allure.step('Отправка POST-запрос для аутентификации пользователя'):
            response = requests.post(Urls.user_auth, data=payload)
        with allure.step('Проверка успешного статуса ответа'):
            assert response.status_code == 200
        with allure.step('Проверка наличия токена в ответе'):
            response_json = response.json()
            assert 'token' in response_json

    @allure.title('Проверка аутентификации с неверным паролем')
    def test_auth_with_wrong_password(self):
        payload = {
            'email': UsersData.existing_user_email,
            'password': 'wrong_password'
        }
        with allure.step('Отправка POST-запрос с неправильным паролем'):
            response = requests.post(Urls.user_auth, data=payload)
        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 401
        with allure.step('Проверка сообщения об ошибке'):
            response_json = response.json()
            assert response_json['error'] == 'Invalid credentials'

    @allure.title('Проверка аутентификации с несуществующим аккаунтом')
    def test_auth_nonexistent_account(self):
        payload = {
            'email': create_random_email(),
            'password': create_random_password()
        }
        with allure.step('Отправка POST-запрос для несуществующего аккаунта'):
            response = requests.post(Urls.user_auth, data=payload)
        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 404
        with allure.step('Проверка сообщения об ошибке'):
            response_json = response.json()
            assert response_json['error'] == 'User not found'