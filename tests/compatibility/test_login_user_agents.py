import pytest
import allure
from http import HTTPStatus
from fake_useragent import UserAgent

@allure.epic('Тестирование совместимости/Логин')
@allure.feature('User-Agent')
class TestLoginUserAgentHeader:

    @allure.story("Логин с разными User-Agent")
    @allure.title("Проверка работы API с разными клиентами")
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
    def test_login_with_different_user_agents(self, login_api, user_agent_type, logger):
        ua = UserAgent()
        user_agent_value = getattr(ua, user_agent_type, ua.random)

        headers = {
            "User-Agent": user_agent_value,
            "Content-Type": "application/json"
        }

        with allure.step(f"Отправляем POST-запрос /api/login с User-Agent {user_agent_value}"):
            response = login_api.login_user(email="eve.holt@reqres.in", password='pistol', headers=headers)
            logger.info(f"User-Agent: {user_agent_value}")
            assert response is not None, "API вернул None"
            assert response.status_code == HTTPStatus.OK, f"Ожидался 200, но получен {response.status_code}"

        with allure.step("Проверка на наличие токена"):
            response_data = response.json()
            assert "token" in response_data, "Токен отсутствует в ответе"