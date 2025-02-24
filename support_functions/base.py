import requests
from data.data import UserData


class Base:
    def base_request(self, url, method="POST", payload=None):
        # создаём список, чтобы метод мог его вернуть
        response_data = {}

        try:
            # В зависимости от метода, выполняем нужный запрос
            if method.upper() == "POST":
                response = requests.post(url, json=payload)
            elif method.upper() == "GET":
                response = requests.get(url, params=payload)
            elif method.upper() == "PUT":
                response = requests.put(url, json=payload)
            elif method.upper() == "DELETE":
                response = requests.delete(url, json=payload)
            else:
                raise ValueError(f"Метод {method} не поддерживается")

            # добавляем код ответа от сервера
            response_data["resp_code"] = response.status_code

            # Если успешный код ответа (200-299), получаем тело ответа
            if 200 <= response.status_code < 300:
                try:
                    response_data["resp_data"] = response.json()  # Парсим JSON, если он есть
                except ValueError:
                    response_data["resp_data"] = "No JSON response"
            else:
                # В случае ошибки, добавляем информацию об ошибке
                response_data["url"] = response.url
                try:
                    response_data["message"] = response.json().get('message', 'No message')
                except ValueError:
                    response_data["message"] = "Non-JSON error response"

        except requests.exceptions.RequestException as e:
            # Обработка ошибок запроса, например, отсутствие сети
            response_data["resp_code"] = 500  # Общий код для ошибки
            response_data["message"] = f"Request failed: {str(e)}"

        # возвращаем список
        return response_data

