import pytest
import allure
from http import HTTPStatus
from fake_useragent import UserAgent

@allure.epic('Тестирование совместимости/Пользователи')
@allure.feature('User-Agent')
class TestUserAgentHeader:

    @allure.story("Создание пользователя с разными User-Agent")
    @allure.title("Проверка создание пользователя с разными клиентами")
    @allure.description("Данный тест проверяет, как работает API с разными клиентами")
    @pytest.mark.parametrize("user_agent_type", [
        "chrome",
        "firefox",
        "safari",
        "opera",
        "edge",
        "ie",
        "android",
        "iphone"
    ])
    def test_login_with_different_user_agents(self, user_api, user_agent_type, logger):
        ua = UserAgent()
        user_agent_value = getattr(ua, user_agent_type, ua.random)

        headers = {
            "User-Agent": user_agent_value,
            "Content-Type": "application/json"
        }

        payload = {
            "name": "Tomas",
            "job": "tester"
        }

        with allure.step(f"Отправляем POST-запрос /api/users с User-Agent {user_agent_value}"):
            response = user_api.create_user(user_data=payload, headers=headers)
            logger.info(f"User-Agent: {user_agent_value}")
            assert response is not None, "API вернул None"
            assert response.status_code == HTTPStatus.CREATED, f"Ожидался 201, но получен {response.status_code}"

        with allure.step("Проверка структуры ответа"):
            data = response.json()
            assert "id" in data, "В ответе нет ID"
            assert "createdAt" in data, "В ответе нет createdAt"