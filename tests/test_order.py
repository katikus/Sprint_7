import pytest
import logging
import copy
import allure  # Подключаем Allure для отчётов

from data.data import UserData
from support_functions.order import Order

# Настраиваем логгер
logger = logging.getLogger(__name__)

@allure.suite("Order")
class TestOrder:
    @pytest.mark.parametrize("test_color", [["BLACK"], ["GREY"], ["GREY", "BLACK"], []])
    @allure.title("Тест успешного создания заказа")
    @allure.description("Создаём заказ с разными вариантами цвета и проверяем успешность создания.")
    def test_order_create_success(self, test_color):
        """Тест успешного создания заказа с разными вариантами цветов"""

        with allure.step("Создаём копию шаблонных данных заказа"):
            payload = copy.deepcopy(UserData.ORDER_DATA)
            payload["color"] = test_color
            allure.attach(str(payload), name="Данные заказа", attachment_type=allure.attachment_type.JSON)

        logger.info(f"📦 В заказ переданы данные - {payload}")

        with allure.step("Отправляем запрос на создание заказа"):
            order = Order()
            order_resp = order.create_order(payload)
            allure.attach(str(order_resp), name="Ответ API", attachment_type=allure.attachment_type.JSON)

        with allure.step("Проверяем, что сервер вернул код 201"):
            assert order_resp.get("resp_code") == 201, f"Ошибка: Заказ не был создан"

        with allure.step("Проверяем, что в ответе присутствует track"):
            assert "track" in order_resp["resp_json_data"], f"Ошибка: В ответе отсутствует track, ответ API: {order_resp}"