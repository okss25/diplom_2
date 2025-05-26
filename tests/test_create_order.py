import allure
import pytest
import requests

from data import IngredientData
from urls import Urls


class TestCreateOrder:
    @allure.title('Проверка ответа создания заказа на запрос с указанными ингредиентами аутентифицированным пользователем')
    @pytest.mark.parametrize('burger_ingredients', [IngredientData.burger_1, IngredientData.burger_2])
    def test_create_order_authenticated_user_success(self, create_new_user_and_delete, burger_ingredients):
        headers = {'Authorization': create_new_user_and_delete[1]['accessToken']}
        payload = {'ingredients': [burger_ingredients]}
        with allure.step('Отправка POST-запрос для создания заказа с аутентифицированным пользователем'):
            response = requests.post(Urls.order_create, data=payload, headers=headers)
        with allure.step('Проверка статус-кода ответа'):
            assert response.status_code == 200
        with allure.step('Проверка успешности ответа'):
            deserials = response.json()
            assert deserials['success'] is True
        with allure.step('Проверка наличия имени заказа'):
            assert 'name' in deserials.keys()
        with allure.step('Проверка наличия номера заказа'):
            assert 'number' in deserials['order'].keys()


    @allure.title('Проверка ответа о создании заказа на запрос с указанными ингредиентами неаутентифицированным пользователем')
    @pytest.mark.parametrize('burger_ingredients', [IngredientData.burger_1, IngredientData.burger_2])
    def test_create_order_unauthenticated_user_success(self, burger_ingredients):
        payload = {'ingredients': [burger_ingredients]}
        with allure.step('Отправка POST-запрос для создания заказа без авторизации'):
            response = requests.post(Urls.order_create, data=payload, headers=Urls.headers)
        with allure.step('Проверка, что статус-код 200 и success True'):
            deserials = response.json()
            assert response.status_code == 200
            assert deserials["success"] is True

    @allure.title('Проверка ответа при создании заказа запросом с неуказанными ингредиентами неаутентифицированным пользователем')
    def test_create_order_empty_ingredients_unauthenticated_user_expected_error(self):
        payload = {'ingredients': []}
        with allure.step('Отправка POST-запрос без авторизации и пустым списком ингредиентов'):
            response = requests.post(Urls.order_create, data=payload, headers=Urls.headers)
        with allure.step('Проверка статуса и сообщения об ошибке'):
            assert response.status_code == 400
            assert response.json() == {'success': False, 'message': 'Ingredient ids must be provided'}

@allure.title('Проверка ответа при создании заказа запросом с невалидными ингредиентами аутентифицированным пользователем')
def test_create_order_invalid_ingredients_authenticated_user_expected_error(self, create_new_user_and_delete):
    headers = {'Authorization': create_new_user_and_delete[1]['accessToken']}
    payload = {'ingredients': [IngredientData.invalid_hash_ingredient]}
    with allure.step('Отправка POST-запрос с невалидным идентификатором ингредиента'):
        response = requests.post(Urls.order_create, data=payload, headers=headers)
    with allure.step('Проверка статуса и сообщения об ошибке'):
        assert response.status_code == 500
        assert response.json() == {"success": False, "message": "One or more ids provided are incorrect"}