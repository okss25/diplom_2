import allure
import requests

from urls import Urls


class TestGetOrders:
    @allure.title('Проверка успешного получения списка заказов для аутентифицированного пользователя')
    @allure.description
    def test_get_orders_authenticated_user_success(self, create_user_and_order_and_delete):
        headers = {'Authorization': create_user_and_order_and_delete[0]}
        response = requests.get(Urls.get_user_orders, headers=headers)
        deserials = response.json()
        assert response.status_code == 200
        assert deserials['success'] is True
        assert 'orders' in deserials.keys()
        assert 'total' in deserials.keys()

    @allure.title('Проверка ответа при запросе на получение списка заказов неаутентифицированного пользователя')
    def test_get_orders_unauthenticated_user_success(self):
        response = requests.get(Urls.get_user_orders, headers=Urls.headers)
        assert response.status_code == 401 and response.json() == {'success': False,
                                                                   'message': 'You should be authorised'}