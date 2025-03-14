import pytest
import allure
from http import HTTPStatus
from faker import Faker

fake = Faker()

@allure.epic('Тестирование безопасности/Логин')
@allure.feature('Фаззинг логина')
class TestLoginFuzzing:

    @allure.story("Фаззинг SQL/XSS инъекции")
    @pytest.mark.parametrize("email, password", [
        ("' OR '1'='1", "password"), #SQLi
        ("test@test.com", "' OR 1=1--"),
        ("admin@example.com", "<script>alert('xss')</script>"), #XSS
        ("<img src=x onerror=alert(1)>", "123456"),
        ("<svg/onload=alert(1)>", "pass"),
        ("../../../../etc/passwd", "root"), #Path traversal
        ("test'; DROP TABLE users;--", "test"),
        ("\"; exec xp_cmdshell('dir');--", "test"),
        ("<iframe src=javascript:alert(1)>", "pass"),
        ("☠️💀🔥", "💣💥"), #Нестандартное юникод
    ])
    def test_login_with_fuzzing_payloads(self, login_api, email, password, logger):
        with allure.step(f"Попытка входа с email={email}"):
            response = login_api.login_user(email=email, password=password)
            logger.info(f"[Fuzz] Email: {email}, Password: {password}")
            logger.info(f"[Fuzz] Ответ: {response.status_code} - {response.text}")

            # Ожидаем, что сервис корректно отвергнет некорректный код
            assert response.status_code in [HTTPStatus.BAD_REQUEST, HTTPStatus.UNAUTHORIZED]
            assert "<script>" not in response.text
            assert "DROP TABLE" not in response.text

    @allure.story("Фаззинг случайными строками с помощью faker")
    @pytest.mark.parametrize("attempt", range(10)) # Генерируем 10 рандомных пар
    def test_login_with_random_input(self, login_api, attempt, logger):
        email = fake.user_name() + fake.random_element(elements=["@test.com", "@example.com"])
        password = fake.password(length=32, special_chars=True, digits=True, upper_case=True, lower_case=True)

        with allure.step(f"Faker логин попытка #{attempt + 1}"):
            response = login_api.login_user(email=email, password=password)
            logger.info(f"[Faker #{attempt}] Email: {email}, Password: {password}")
            logger.info(f"[Faker #{attempt}] Ответ: {response.status_code} - {response.text}")

            assert response.status_code in [HTTPStatus.BAD_REQUEST, HTTPStatus.UNAUTHORIZED]
