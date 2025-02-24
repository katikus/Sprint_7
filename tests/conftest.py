import pytest
import logging

logging.basicConfig(level=logging.INFO, format=" \n %(asctime)s [%(levelname)s] %(message)s")

# Настроим логгер
logger = logging.getLogger(__name__)



from support_functions.courier import create_random_courier_data, Courier


@pytest.fixture(scope="function")
def random_courier():
    """Фикстура для создания случайного курьера"""
    data = create_random_courier_data()
    courier = Courier()
    response = courier.register_new_courier(data['login'], data['password'], data['first_name'])

    logger.info(f"✅ Курьер создан: {data}")
    #print(f"\n ✅ Курьер создан: {data}")
    assert response['resp_code'] == 201, f"Ошибка при создании курьера: {response}"

    yield {
        'resp_data': response['resp_data'],
        'data': data
    }

    # Удаляем курьера после теста
    login_resp = courier.login_courier(data['login'], data['password'])
    if login_resp.get('resp_code') == 200:
        courier_id = login_resp.get('resp_data').get('id')
        delete_resp = courier.delete_courier(courier_id)
        assert delete_resp['resp_code'] == 200, f"Ошибка удаления курьера: {delete_resp}"
        logger.info(f"🗑️ Курьер {courier_id} удален")
    else:
        logger.warning(f"⚠️ Курьер {data['login']} не найден при попытке удаления")