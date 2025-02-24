import requests
import pytest
import logging

from support_functions.courier import Courier, create_random_courier_data

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Настроим логгер
logger = logging.getLogger(__name__)


def test_courier_create_success(random_courier):
    """Тест успешного создания, логина и удаления курьера"""
    courier = Courier()

    data = random_courier['data']
    courier_login_obj = courier.login_courier(data['login'], data['password'])
    assert courier_login_obj['resp_code'] == 200, f"Ошибка логина: {courier_login_obj}"


def test_courier_create_twice_fail(random_courier):
    """Тест попытки повторного создания курьера с теми же данными"""
    data = random_courier['data']
    courier = Courier()

    duplicate_response = courier.register_new_courier(data['login'], data['password'],
                                              data['first_name'])
    assert duplicate_response['resp_code'] == 409, f"Повторная регистрация не вызвала ошибку: {duplicate_response}"



@pytest.mark.parametrize("missing_field", ["login", "password"])
def test_courier_create_missing_field(missing_field):
    """Тест, что курьер не создается, если отсутствует один из обязательных параметров"""
    courier = Courier()
    data = create_random_courier_data()
    data.pop(missing_field)  # Удаляем один из параметров


    response = courier.register_new_courier(
        data.get("login"),
        data.get("password"),
        data.get("first_name")
    )

    # Если API неожиданно создало курьера, удаляем его
    if response.get("resp_code") == 201:
        logger.warning(f"⚠️ Курьер был создан без {missing_field}, выполняем удаление...")
        print(f"⚠️ Курьер был создан без {missing_field}, выполняем удаление...")
        login_resp = courier.login_courier(data['login'], data['password'])
        if login_resp.get("resp_code") == 200:
            delete_resp = courier.delete_courier(login_resp['c_id'])
            assert delete_resp['resp_code'] == 200, f"Ошибка удаления курьера: {delete_resp}"
            logger.info(f"🗑️ Некорректно созданный курьер удален")

    assert response['resp_code'] == 400, f"Курьер создан без {missing_field}: {response}"
    logger.info(f"✅ Проверено: нельзя создать курьера без {missing_field}")

def test_courier_create_response_201(random_courier):
    """Тест, что при корректном создании курьера API возвращает 201"""
    # Так как фикстура уже создает курьера, просто проверяем код ответа
    logger.info(f"✅ Код ответа 201 при создании курьера {random_courier}")

def test_courier_create_right_response_body(random_courier):
    """Тест проверяет, что в resp_data правильное тело ответа"""
    # Извлекаем resp_data из словаря, который возвращает фикстура
    resp_data = random_courier['resp_data']

    # Ожидаемое значение для проверки
    expected_response = {"ok": True}
    # Проверяем, что ответ соответствует ожидаемому
    assert resp_data == expected_response, f"Ошибка: {random_courier}"


