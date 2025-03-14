import pytest
import allure
from http import HTTPStatus
from faker import Faker

fake = Faker()

@allure.epic("Безопасность API")
@allure.feature("Фаззинг заголовков и форматов")
class TestFuzzHeadersFormats:

    @allure.story("Отправка запросов с вредоносными заголовками")
    @pytest.mark.parametrize("headers", [
        {"User-Agent": "' OR 1=1--"},
        {"User-Agent": "<script>alert('XSS')</script>"},
        {"X-Custom-Header": "☠️💀🔥"},
        {"Content-Type": "text/html<script>alert(1)</script>"},
        {"Authorization": "Bearer <svg/onload=alert(1)>"},
    ])
    def test_post_users_with_fuzz_headers(self, user_api, headers, logger):
        payload = {"name": fake.first_name(), "job": fake.job()}

        with allure.step(f"POST /api/users с заголовками: {headers}"):
            response = user_api.session.post(
                url=user_api.base_url + "/api/users",
                json=payload,
                headers=headers
            )

            logger.info(f"[Fuzz Headers] Заголовки: {headers}")
            logger.info(f"[Fuzz Headers] Ответ: {response.status_code} - {response.text}")

            assert response.status_code in [
                HTTPStatus.CREATED,
                HTTPStatus.BAD_REQUEST,
                HTTPStatus.UNSUPPORTED_MEDIA_TYPE
            ]

    @allure.story("Отправка запросов с невалидными JSON")
    @pytest.mark.parametrize("body", [
        "}{",  # ломаный JSON
        fake.text(max_nb_chars=500),  # текст вместо JSON
        "<xml><data>123</data></xml>",  # XML вместо JSON
        None,  # пустое тело
    ])
    def test_post_with_malformed_body(self, user_api, body, logger):
        headers = {"Content-Type": "application/json"}

        with allure.step(f"POST /api/users с телом: {body}"):
            response = user_api.session.post(
                url=user_api.base_url + "/api/users",
                data=body, # data для сырых тел
                headers=headers
            )

            logger.info(f"[Malformed Body] Payload: {body}")
            logger.info(f"[Malformed Body] Ответ: {response.status_code} - {response.text}")

            assert response.status_code in [
                HTTPStatus.BAD_REQUEST,
                HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
                HTTPStatus.INTERNAL_SERVER_ERROR
            ]

    @allure.story("Отправка с неправильным Content-Type")
    @pytest.mark.parametrize("content_type", [
        "text/plain",
        "application/xml",
        "multipart/form-data",
        "application/x-www-form-urlencoded",
        "image/png"
    ])
    def test_post_with_wrong_content_type(self, user_api, content_type, logger):
        headers = {"Content-Type": content_type}
        payload = '{"name": "Test", "job": "hacker"}'

        with allure.step(f'POST /api/users с Content-Type: {content_type}'):
            response = user_api.session.post(
                url=user_api.base_url + "/api/users",
                data=payload,
                headers=headers
            )

            logger.info(f"[Wrong Content-Type] Content-Type: {content_type}")
            logger.info(f"[Wrong Content-Type] Ответ: {response.status_code} - {response.text}")

            assert response.status_code in [HTTPStatus.BAD_REQUEST,
                                            HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
                                            HTTPStatus.INTERNAL_SERVER_ERROR]

