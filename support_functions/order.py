import requests
import random
import string

import logging

from data.data import UserData
from data.data import UserData
from support_functions.base import Base

# Настроим логгер
logger = logging.getLogger(__name__)


class Order(Base):

    def create_order(self, payload):
        url = UserData.ORDER_URL
        return self.base_request(url, method="POST", payload = payload)