import allure
import requests

from urls import Urls


class TestGetOrders:
    @allure.title('Проверка успешного получения списка заказов для аутентифицированного пользователя')
    @allure.description('Тест проверяет, что авторизованный пользователь получает список своих заказов успешно')
    def test_get_orders_authenticated_user_success(self, create_user_and_order_and_delete):
        with allure.step("Получение токена авторизации из фикстуры"):
            token = create_user_and_order_and_delete[0]

        with allure.step("Подготовка заголовков запроса с токеном авторизации"):
            headers = {'Authorization': token}

        with allure.step("Отправка GET-запрос для получения заказов пользователя"):
            response = requests.get(Urls.get_user_orders, headers=headers)

        with allure.step("Десериализация ответа в JSON"):
            try:
                deserials = response.json()
            except ValueError as e:
                assert False, f"Ошибка десериализации ответа: {e}"

        with allure.step("Проверка статуса ответа и содержимого"):
            assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
            assert deserials.get('success') is True, f"Параметр success не равен True: {deserials}"
            assert 'orders' in deserials, "Ключ 'orders' отсутствует в ответе"
            assert 'total' in deserials, "Ключ 'total' отсутствует в ответе"

    @allure.title('Проверка ответа при запросе на получение списка заказов неаутентифицированного пользователя')
    @allure.description('Тест проверяет, что неавторизованный пользователь получает ошибку при попытке получить список заказов')
    def test_get_orders_unauthenticated_user_success(self):
        with allure.step("Отправка GET-запрос без авторизационных заголовков"):
            response = requests.get(Urls.get_user_orders, headers=Urls.headers)

        with allure.step("Десериализация ответа в JSON"):
            try:
                deserials = response.json()
            except ValueError as e:
                assert False, f"Ошибка десериализации ответа: {e}"

        with allure.step("Проверка, что возвращается статус 401 и сообщение об авторизации"):
            assert response.status_code == 401, f"Ожидался статус 401, получен {response.status_code}"
            expected_response = {'success': False, 'message': 'You should be authorised'}
            assert deserials == expected_response, f"Ответ не соответствует ожидаемому: {deserials}"