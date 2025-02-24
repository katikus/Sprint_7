import requests
import random
import string

from data.data import UserData
from support_functions.base import Base

def create_random_courier_data():
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    # генерируем логин, пароль и имя курьера
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    return {"login" : login, "password" : password, "first_name": first_name}


class Courier(Base):

    def register_new_courier(self, login, password, firstName):

        url = UserData.COURIER_URL

        payload = {
            "login": login,
            "password": password,
            "firstName": firstName
        }

        return self.base_request(url, method="POST", payload=payload)

    def login_courier(self, login=None, password=None, first_name=None):
        url = UserData.LOGIN_URL

        # собираем тело запроса
        payload = {
            "login": login,
            "password": password
        }

        return self.base_request(url, method="POST", payload=payload)


    def delete_courier(self, c_id):
        url = f"{UserData.COURIER_URL}/{c_id}"

        return self.base_request(url, method="DELETE")

