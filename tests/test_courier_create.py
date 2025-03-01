import pytest
import logging
import allure  # Подключаем Allure для отчётов

from support_functions.courier import Courier, create_random_courier_data

# Настроим логирование
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

@allure.suite("Courier Create")
class TestCourierСreate:
    @allure.title("Тест кода ответа 201 при успешном создании курьера")
    @allure.description("Фикстура `random_courier` создаёт курьера, проверяем, что API вернёт 201.")
    def test_courier_create_response_201(self, random_courier):
        assert random_courier['resp_code'] == 201, f"Ошибка: {random_courier}"
        allure.attach(str(random_courier), name="Ответ API", attachment_type=allure.attachment_type.JSON)
        logger.info(f"✅ Код ответа 201 при создании курьера {random_courier}")

    @allure.title("Тест структуры ответа при успешном создании курьера")
    @allure.description("Проверяем, что тело ответа API соответствует ожидаемому формату.")
    def test_courier_create_right_response_body(self, random_courier):
        expected_response = {"ok": True}

        with allure.step("Извлекаем `resp_json_data` из фикстуры и проверяем его"):
            resp_data = random_courier['resp_json_data']
            allure.attach(str(resp_data), name="Ответ API", attachment_type=allure.attachment_type.JSON)

            assert resp_data == expected_response, f"Ошибка: {random_courier}"

    @allure.title("Тест попытки повторного создания курьера с теми же данными")
    @allure.description("Регистрируем курьера, затем повторно пробуем создать его с теми же данными.")
    def test_courier_create_twice_fail(self, random_courier):
        data = random_courier['data']
        courier = Courier()

        with allure.step("Повторная попытка регистрации с теми же данными"):
            duplicate_response = courier.register_new_courier(data['login'], data['password'], data['first_name'])
        print(duplicate_response)
        with allure.step("Проверяем, что API вернуло 409 (конфликт)"):
            assert duplicate_response[
                       'resp_code'] == 409, f"Повторная регистрация не вызвала ошибку: {duplicate_response}"

            assert duplicate_response['resp_json_data']['message'] == "Этот логин уже используется", f"Ошибка логина: {duplicate_response}"
            allure.attach(str(duplicate_response), name="Ответ API", attachment_type=allure.attachment_type.JSON)

    @pytest.mark.parametrize("missing_field", ["login", "password"])
    @allure.title("Тест создания курьера без обязательного поля")
    @allure.description("Пробуем создать курьера без одного из обязательных параметров и проверяем код ошибки.")
    def test_courier_create_missing_field(self, missing_field):
        courier = Courier()

        with allure.step(f"Создаём случайные данные для курьера и удаляем поле {missing_field}"):
            data = create_random_courier_data()
            data.pop(missing_field)
            allure.attach(str(data), name="Данные без обязательного поля", attachment_type=allure.attachment_type.JSON)

        with allure.step("Отправляем запрос на создание курьера"):
            response = courier.register_new_courier(
                data.get("login"),
                data.get("password"),
                data.get("first_name")
            )

        with allure.step("Проверяем, что API вернуло 400 (ошибка)"):
            assert response['resp_code'] == 400, f"Курьер создан без {missing_field}: {response}"
            assert response['resp_json_data']['message'] == "Недостаточно данных для создания учетной записи", f"Ошибка логина: {response}"
            allure.attach(str(response), name="Ответ API", attachment_type=allure.attachment_type.JSON)

