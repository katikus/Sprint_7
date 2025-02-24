
import pytest
import logging

from support_functions.courier import Courier

# Настроим логгер
logger = logging.getLogger(__name__)


def test_courier_authorize_success(random_courier):
    # Извлекаем data из словаря, который возвращает фикстура
    data = random_courier['data']

    courier = Courier()

    login_resp = courier.login_courier(data['login'], data['password'])
    logger.info(f"✅ Логин успешен {login_resp['resp_code']}")

    # Проверяем, что ответ соответствует ожидаемому
    assert login_resp.get("resp_code") == 200, f"Ошибка: Курьер не смог авторизоваться"


@pytest.mark.parametrize("missing_field", ["login", "password"])
def test_courier_authorize_without_required_field_success(random_courier, missing_field):
    data = random_courier['data']

    new_data = data.copy()
    new_data.pop(missing_field)

    courier = Courier()
    login_resp = courier.login_courier(**new_data)
    logger.info(f"✅ Логин не успешен {login_resp['resp_code']} данные использованные для логина {new_data} ")

    # Проверяем, что ответ соответствует ожидаемому
    assert login_resp.get("resp_code") == 400, f"Ошибка: Курьер не смог авторизоваться"


@pytest.mark.parametrize("missing_field", ["login", "password"])
def test_courier_authorize_with_empty_field_success(random_courier, missing_field):
    data = random_courier['data']

    new_data = data.copy()
    new_data[missing_field] = ''

    courier = Courier()
    login_resp = courier.login_courier(**new_data)
    logger.info(f"✅ Логин не успешен {login_resp['resp_code']} данные использованные для логина {new_data} ")

    # Проверяем, что ответ соответствует ожидаемому
    assert login_resp.get("resp_code") == 400, f"Ошибка: Курьер не смог авторизоваться"

@pytest.mark.parametrize("missing_field", ["login", "password"])
def test_courier_authorize_with_incorrect_data_success(random_courier, missing_field):

    data = random_courier['data']

    new_data = data.copy()
    new_data[missing_field] = new_data[missing_field]+"1"

    courier = Courier()
    login_resp = courier.login_courier(**new_data)
    logger.info(f"✅ Логин не успешен {login_resp['resp_code']} данные использованные для логина {new_data} ")

    # Проверяем, что ответ соответствует ожидаемому
    assert login_resp.get("resp_code") == 404, f"Ошибка: Курьер не смог авторизоваться"

def test_courier_authorization_return_id_success(random_courier):
    # Извлекаем data из словаря, который возвращает фикстура
    data = random_courier['data']

    # Логинимся под учетными данными
    courier = Courier()
    login_resp = courier.login_courier(data['login'], data['password'])
    logger.info(f"✅ Логин успешен {login_resp['resp_code']} id - {login_resp.get('resp_data').get("id")}")

    # Проверяем, что ответ соответствует ожидаемому
    assert login_resp.get('resp_data').get("id"), "Ошибка: значение пустое или None"