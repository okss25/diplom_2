import requests
import pytest
import allure

from data import UsersData
from helper import create_random_email, create_random_password, create_random_username
from urls import Urls


class TestRegistration:
    @allure.title('Проверка успешной регистрации аккаунта с валидными данными')
    def test_registration_new_account_success_submit(self):
        with allure.step("Генерация случайных данных для регистрации"):
            email = create_random_email()
            password = create_random_password()
            username = create_random_username()

        with allure.step("Формирование тела запроса"):
            payload = {
                'email': email,
                'password': password,
                'name': username
            }

        with allure.step("Отправка запроса на регистрацию"):
            response = requests.post(Urls.user_register, json=payload)

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 200, f"Неверный код ответа: {response.status_code}, текст: {response.text}"

        with allure.step("Проверка успешности регистрации в ответе"):
            try:
                response_json = response.json()
            except ValueError as e:
                assert False, f"Ошибка десериализации ответа в JSON: {e}"


            assert response_json.get('success') is True, f"Регистрация не удалась: {response_json}"

            assert 'accessToken' in response_json, "Нет accessToken в ответе"
            assert 'refreshToken' in response_json, "Нет refreshToken в ответе"
            assert 'user' in response_json, "Нет данных о пользователе в ответе"

            user_data = response_json['user']
            assert user_data.get('email') == email, f"Email в ответе {user_data.get('email')} не совпадает с отправленным {email}"
            assert user_data.get('name') == username, f"Имя в ответе {user_data.get('name')} не совпадает с отправленным {username}"

        access_token = response_json['accessToken']
        with allure.step("Удаление созданного пользователя"):
            delete_response = requests.delete(Urls.user_delete, headers={'Authorization': access_token})
            assert delete_response.status_code == 202 or delete_response.status_code == 200, \
                f"Удаление пользователя завершилось с кодом {delete_response.status_code}"

    @allure.title('Проверка ответа на запрос регистрации с незаполненным обязательным полем')
    @pytest.mark.parametrize('credentials', UsersData.credentials_with_empty_field)
    def test_registration_one_required_field_is_empty_failed_submit(self, credentials):
        with allure.step(f"Отправка регистрации с данными: {credentials}"):
            response = requests.post(Urls.user_register, data=credentials)

        with allure.step("Проверка статуса и сообщения об ошибке"):
            assert response.status_code == 403, f"Ожидался код 403, получен {response.status_code}"
            response_json = response.json()
            assert response_json == {'success': False, 'message': 'Email, password and name are required fields'}, \
                f"Неверный ответ: {response_json}"

    @allure.title('Проверка ответа на запрос регистрации с существующим в базе email')
    def test_registration_login_taken_failed_submit(self):
        with allure.step("Подготовка данных с уже существующим email"):
            payload = {
                'email': UsersData.email,
                'password': create_random_password(),
                'name': create_random_username()
            }

        with allure.step("Отправка запроса на регистрацию с существующим email"):
            response = requests.post(Urls.user_register, data=payload)

        with allure.step("Проверка ответа на регистрацию с уже существующим email"):
            assert response.status_code == 403, f"Ожидался код 403, получен {response.status_code}"
            response_json = response.json()
            assert response_json == {'success': False, 'message': 'User already exists'}, \
                f"Неверный ответ: {response_json}"