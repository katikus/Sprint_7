
import pytest
import logging
import copy

import requests

from data.data import UserData
from support_functions.order import Order

# Настроим логгер
logger = logging.getLogger(__name__)



@pytest.mark.parametrize("test_color", [["BLACK"], ["GREY"],["GREY", "BLACK"], []])
def test_order_create_success(test_color):
    """Тест успешного создания заказа с разными цветами"""

    payload = copy.deepcopy(UserData.ORDER_DATA)
    payload["color"] = test_color

    logger.info(f"📦 В заказ переданы данные - {payload}")

    # Создаем заказ
    order = Order()
    order_resp = order.create_order(payload)

    # Проверяем, что ответ соответствует ожидаемому
    assert order_resp.get("resp_code") == 201, f"Ошибка: Заказ не был создан"
    # Проверяем, что в ответе есть 'track'
    assert "track" in order_resp["resp_data"]