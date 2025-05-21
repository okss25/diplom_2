import allure
import pytest
import requests

from data import IngredientData
from urls import Urls


class TestCreateOrder:
    @allure.title('Проверка ответа создания заказа на запрос с указанными ингредиентами аутентифицированным пользователем')
    @allure.description
    @pytest.mark.parametrize('burger_ingredients', [IngredientData.burger_1, IngredientData.burger_2])
    def test_create_order_authenticated_user_success(self, create_new_user_and_delete, burger_ingredients):
        headers = {'Authorization': create_new_user_and_delete[1]['accessToken']}
        payload = {'ingredients': [burger_ingredients]}
        response = requests.post(Urls.order_create, data=payload, headers=headers)
        deserials = response.json()
        assert response.status_code == 200
        assert deserials['success'] is True
        assert 'name' in deserials.keys()
        assert 'number' in deserials['order'].keys()

    @allure.title('Проверка ответа о создании заказа на запрос с указанными ингредиентами неаутентифицированным пользователем')
    @allure.description
    @pytest.mark.parametrize('burger_ingredients', [IngredientData.burger_1, IngredientData.burger_2])
    def test_create_order_unauthenticated_user_success(self, burger_ingredients):
        payload = {'ingredients': [burger_ingredients]}
        response = requests.post(Urls.order_create, data=payload, headers=Urls.headers)
        assert response.status_code == 200 and response.json()["success"] is True

    @allure.title('Проверка ответа при создании заказа запросом с неуказанными ингредиентами аутентифицированным пользователем')
    @allure.description
    def test_create_order_empty_ingredients_authenticated_user_expected_error(self, create_new_user_and_delete):
        headers = {'Authorization': create_new_user_and_delete[1]['accessToken']}
        payload = {'ingredients': []}
        response = requests.post(Urls.order_create, data=payload, headers=headers)
        assert response.status_code == 400 and response.json() == {'success': False,
                                                                   'message': 'Ingredient ids must be provided'}

    @allure.title('Проверка ответа при создании заказа запросом с неуказанными ингредиентами неаутентифицированным пользователем')
    @allure.description
    def test_create_order_empty_ingredients_unauthenticated_user_expected_error(self):
        payload = {'ingredients': []}
        response = requests.post(Urls.order_create, data=payload, headers=Urls.headers)
        assert response.status_code == 400 and response.json() == {'success': False,
                                                                   'message': 'Ingredient ids must be provided'}

    @allure.title('Проверка ответа при создании заказа запросом с невалидными ингредиентами аутентифицированным пользователем')
    @allure.description
    def test_create_order_invalid_ingredients_authenticated_user_expected_error(self, create_new_user_and_delete):
        headers = {'Authorization': create_new_user_and_delete[1]['accessToken']}
        payload = {'ingredients': [IngredientData.invalid_hash_ingredient]}
        response = requests.post(Urls.order_create, data=payload, headers=headers)
        assert response.status_code == 500 and response.json() == {"success": False,
                                                                   "message": "One or more ids provided are incorrect"}