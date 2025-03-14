import pytest
import allure
from http import HTTPStatus
from faker import Faker

fake = Faker()

@allure.epic("Безопасность API/Пользователи")
@allure.feature("Фаззинг пользователей")
class TestUsersFuzzing:

    @allure.story("Создание пользователей с вредоносным строками")
    @pytest.mark.parametrize("payload", [
        {"name": "' OR 1=1--", "job": "admin"},
        {"name": "<script>alert(1)</script>", "job": "developer"},
        {"name": fake.name(), "job": "<svg/onload=alert(1)>"},
        {"name": "../../etc/passwd", "job": "root"},
        {"name": fake.text(max_nb_chars=1000), "job": fake.text(max_nb_chars=1000)},  # Очень длинные данные
        {"name": fake.pystr(min_chars=1, max_chars=1), "job": ""},  # Минимальные значения
        {"name": "☠️💀🔥", "job": "💣💥"}
    ])
    def test_create_user_with_fuzz_data(self, user_api, payload, logger):
        with allure.step(f"Создание пользователя с нестандартными данными: {payload}"):
            response = user_api.create_user(payload)
            logger.info(f"[Fuzz Create] Payload: {payload}")
            logger.info(f"[Fuzz Create] Ответ: {response.status_code} - {response.text}")

            assert response.status_code in [
                HTTPStatus.CREATED,
                HTTPStatus.BAD_REQUEST,
                HTTPStatus.UNAUTHORIZED,
                HTTPStatus.UNPROCESSABLE_ENTITY]

            if response.status_code == HTTPStatus.CREATED:
                json_data = response.json()
                # Проверяем, что ответ не содержит вредоносных отражений
                for val in payload.values():
                    assert val not in (json_data.values()), "Обнаружены отраженные данные"

    @allure.story("Обновление пользователей вредоносными строками")
    @pytest.mark.parametrize("update_data", [
        {"name": "'; DROP TABLE users;--", "job": "intruder"},
        {"name": "<iframe src='evil.com'>", "job": "xss_test"},
        {"name": fake.name(), "job": fake.text(max_nb_chars=500)},
        {"name": "", "job": " "},
        {"name": "💀💀💀", "job": "🔥🔥🔥"},
    ])
    def test_update_user_with_fuzz_data(self, user_api, update_data, logger):
        user_id = 2

        with allure.step(f"Обновляем пользователя ID={user_id} с данными: {update_data}"):
            response = user_api.update_user(user_id=user_id, user_data=update_data)
            logger.info(f"[Fuzz Update] Payload: {update_data}")
            logger.info(f"[Fuzz Update] Ответ: {response.status_code} - {response.text}")

            assert response.status_code in [
                HTTPStatus.OK,
                HTTPStatus.BAD_REQUEST,
                HTTPStatus.UNPROCESSABLE_ENTITY
            ]

            if response.status_code == HTTPStatus.OK:
                response_data = response.json()
                for val in update_data.values():
                    assert val in response_data.values(), "Найдено отражение вредоносных данных"

    @allure.story("Удаление пользователей с подозрительным ID")
    @pytest.mark.parametrize("user_id", [
        "1; DROP TABLE users",
        "abc<script>",
        "../../etc/passwd",
        "💀💣🔥",
        999999999999999999,  # Очень большой ID
        "",  # пустая строка
        None
    ])
    def test_delete_user_with_fuzzed_id(self, user_api, user_id, logger):
        with allure.step(f"Пытаемся удалить пользователя"):
            try:
                response = user_api.delete_user(user_id=user_id)
            except Exception as e:
                logger.warning(f"Исключение при DELETE /api/users/{user_id}: {e}")

            logger.info(f"[Fuzz Delete] Ответ: {response.status_code}")
            assert response.status_code in [
                HTTPStatus.NO_CONTENT,
                HTTPStatus.BAD_REQUEST,
                HTTPStatus.NOT_FOUND
            ]