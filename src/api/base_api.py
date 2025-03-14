import logging
from requests import Response
import requests

logger = logging.getLogger("API")

class BaseAPI:
    """
    Базовый класс для взаимодействия с API
    """

    def __init__(self, base_url: str, timeout: int = 10):
        """Инициализация базового класса"""
        self.base_url = base_url
        self.timeout = timeout
        self.headers = {"Content-Type": "application/json"}  # Заголовки по умолчанию
        self.session = requests.Session()

    def request(self, method: str, endpoint: str, **kwargs) -> Response | None:
        """
        Отправляет Http-запросы к api
        :param method: http-метод(get, post, put, patch, delete
        :param endpoint: конечная точка api(/user, /user/1)
        :param kwargs: доп. параметры
        :return: Объект Response
        """

        url = f"{self.base_url}{endpoint}"
        kwargs.setdefault("headers", self.headers) # Используем заголовки по умолчанию
        kwargs.setdefault("timeout", self.timeout) # Устанавливаем таймаут

        try:
            logger.info(f"Выполнение {method}-запроса к {url} с параметрами {kwargs}")
            response = self.session.request(method, url, **kwargs)
            logger.info(f"Статус ответа: {response.status_code}")
            # response.raise_for_status()
            if response.status_code >= 400:
                logger.error(f"Ошибка запроса: {response.status_code} - {response.text}")
            return response
        except requests.RequestException as e:
            # error_message = f"Ошибка запроса: {e}"
            # if isinstance(e, requests.HTTPError) and e.response is not None:
            #     error_message += f" | Тело ответа: {e.response.text}"
            # logger.error(error_message, exc_info=True)
            logger.error(f'Ошибка запроса: {e}', exc_info=True)
            return None # Возвращаем None в случае ошибки

    def get(self, endpoint: str, **kwargs) -> Response | None:
        """
        Метод GET
        :param endpoint: Конечная точка
        :param kwargs: Доп. параметры
        :return: Объект Resposne
        """
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> Response | None:
        """
        Метод POST
        :param endpoint: Конечная точка
        :param kwargs: Доп. параметры
        :return: Объект Response
        """
        return self.request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> Response | None:
        """
        Метод PUT
        :param endpoint: Конечная точка
        :param kwargs: Доп. параметры
        :return: Объект Response
        """
        return self.request("PUT", endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs) -> Response | None:
        """
        Метод PATCH
        :param endpoint: Конечная точка
        :param kwargs: Доп. параметры
        :return: Объект Response
        """
        return self.request("PATCH", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> Response | None:
        """
        Метод DELETE
        :param endpoint: Конечная точка
        :param kwargs: Доп. параметры
        :return: Объект Response
        """
        return self.request("DELETE", endpoint, **kwargs)