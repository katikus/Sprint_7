import pytest
import logging
import allure  # Подключаем Allure



# Настроим логгер
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format=" \n %(asctime)s [%(levelname)s] %(message)s")

from support_functions.courier import create_random_courier_data, Courier


@pytest.fixture(scope="function")
@allure.title("Фикстура для создания случайного курьера")
@allure.description("Создаёт случайного курьера, выполняет регистрацию, а затем удаляет его после теста.")
def random_courier():
    """Фикстура для создания случайного курьера"""
    with allure.step("Генерируем случайные данные для курьера"):
        data = create_random_courier_data()
        allure.attach(str(data), name="Данные курьера", attachment_type=allure.attachment_type.JSON)

    courier = Courier()

    with allure.step("Отправляем запрос на регистрацию курьера"):
        response = courier.register_new_courier(data['login'], data['password'], data['first_name'])
        allure.attach(str(response), name="Ответ API (регистрация)", attachment_type=allure.attachment_type.JSON)

    logger.info(f"✅ Курьер создан: {data}")

    yield {
        'resp_json_data': response['resp_json_data'],
        'text' : response['text'],
        'resp_code' : response['resp_code'],
        'data': data
    }

    with allure.step("Выполняем удаление курьера после теста"):
        login_resp = courier.login_courier(data['login'], data['password'])
        allure.attach(str(login_resp), name="Ответ API (логин)", attachment_type=allure.attachment_type.JSON)

        if login_resp.get('resp_code') == 200:
            courier_id = login_resp.get('resp_json_data').get('id')

            delete_resp = courier.delete_courier(courier_id)
            allure.attach(str(delete_resp), name="Ответ API (удаление)", attachment_type=allure.attachment_type.JSON)

            logger.info(f"🗑️ Курьер {courier_id} удален")
        else:
            logger.warning(f"⚠️ Курьер {data['login']} не найден при попытке удаления")
            allure.attach(f"⚠️ Курьер {data['login']} не найден при попытке удаления",
                          name="Ошибка удаления", attachment_type=allure.attachment_type.TEXT)
