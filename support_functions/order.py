import logging

import allure

from data.data import UserData
from support_functions.base import Base

# Настроим логгер
logger = logging.getLogger(__name__)


class Order(Base):
    @allure.step("Создание заказа")
    def create_order(self, payload):
        url = UserData.ORDER_URL
        return self.base_request(url, method="POST", payload = payload)