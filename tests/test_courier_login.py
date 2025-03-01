import pytest
import logging
import allure
from support_functions.courier import Courier

# Настроим логгер
logger = logging.getLogger(__name__)

@allure.suite("Courier Login")
class TestCourierLogin:

    @allure.title("Успешная авторизация курьера")
    @allure.description("Проверяем, что курьер может авторизоваться с корректными данными")
    def test_courier_authorize_success(self, random_courier):
        data = random_courier['data']
        courier = Courier()

        with allure.step("Отправляем запрос на авторизацию"):
            login_resp = courier.login_courier(data['login'], data['password'])
            allure.attach(str(login_resp), name="Response", attachment_type=allure.attachment_type.JSON)

        logger.info(f"✅ Логин успешен {login_resp['resp_code']}")
        assert login_resp.get("resp_code") == 200, "Ошибка: Курьер не смог авторизоваться"
        assert '"id":' in login_resp['text'], f"Ошибка логина: {login_resp}"


    @pytest.mark.parametrize("missing_field", ["login", "password"])
    @allure.title("Авторизация без обязательного поля")
    @allure.description("Проверяем, что нельзя авторизоваться без логина или пароля")
    def test_courier_authorize_without_required_field_success(self, random_courier, missing_field):
        data = random_courier['data']
        new_data = data.copy()
        new_data.pop(missing_field)

        courier = Courier()

        with allure.step(f"Отправляем запрос без поля {missing_field}"):
            login_resp = courier.login_courier(**new_data)
            allure.attach(str(login_resp), name="Response", attachment_type=allure.attachment_type.JSON)

        logger.info(f"✅ Логин не успешен {login_resp['resp_code']}, данные: {new_data}")
        assert login_resp.get("resp_code") == 400, "Ошибка: Ожидался код 400"
        assert login_resp['resp_json_data']['message'] == "Недостаточно данных для входа", f"Ошибка логина: {login_resp}"

    @pytest.mark.parametrize("missing_field", ["login", "password"])
    @allure.title("Авторизация с пустым значением поля")
    @allure.description("Проверяем, что нельзя авторизоваться с пустым логином или паролем")
    def test_courier_authorize_with_empty_field_success(self, random_courier, missing_field):
        data = random_courier['data']
        new_data = data.copy()
        new_data[missing_field] = ''

        courier = Courier()

        with allure.step(f"Отправляем запрос с пустым значением поля {missing_field}"):
            login_resp = courier.login_courier(**new_data)
            allure.attach(str(login_resp), name="Response", attachment_type=allure.attachment_type.JSON)

        logger.info(f"✅ Логин не успешен {login_resp['resp_code']}, данные: {new_data}")
        assert login_resp.get("resp_code") == 400, "Ошибка: Ожидался код 400"
        assert login_resp['resp_json_data']['message'] == "Недостаточно данных для входа", f"Ошибка логина: {login_resp}"

    @pytest.mark.parametrize("missing_field", ["login", "password"])
    @allure.title("Авторизация с некорректными данными")
    @allure.description("Проверяем, что нельзя авторизоваться с неправильным логином или паролем")
    def test_courier_authorize_with_incorrect_data_success(self, random_courier, missing_field):
        data = random_courier['data']
        new_data = data.copy()
        new_data[missing_field] += "1"  # Меняем логин или пароль

        courier = Courier()

        with allure.step(f"Отправляем запрос с некорректными данными в поле {missing_field}"):
            login_resp = courier.login_courier(**new_data)
            allure.attach(str(login_resp), name="Response", attachment_type=allure.attachment_type.JSON)

        logger.info(f"✅ Логин не успешен {login_resp['resp_code']}, данные: {new_data}")
        assert login_resp.get("resp_code") == 404, "Ошибка: Ожидался код 404"
        assert login_resp['resp_json_data'][
                   'message'] == "Учетная запись не найдена", f"Ошибка логина: {login_resp}"

    @allure.title("Авторизация возвращает ID курьера")
    @allure.description("Проверяем, что успешная авторизация возвращает ID")
    def test_courier_authorization_return_id_success(self, random_courier):
        data = random_courier['data']
        courier = Courier()

        with allure.step("Отправляем запрос на авторизацию"):
            login_resp = courier.login_courier(data['login'], data['password'])
            allure.attach(str(login_resp), name="Response", attachment_type=allure.attachment_type.JSON)

        courier_id = login_resp.get('resp_json_data', {}).get("id")
        logger.info(f"✅ Логин успешен {login_resp['resp_code']}, ID: {courier_id}")
        assert courier_id, "Ошибка: ID не возвращен"
