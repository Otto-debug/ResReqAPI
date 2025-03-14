import pytest
import allure
from http import HTTPStatus
from faker import Faker

fake = Faker()

@allure.epic("Безопасность API/Регистрация")
@allure.feature("Фаззинг регистрации")
class TestRegisterFuzzing:

    @allure.story("Фаззинг SQL/XSS инъекциями")
    @pytest.mark.parametrize("email, password", [
        ("' OR '1'='1", "password"),
        ("<script>alert('xss')</script>", "123456"),
        ("../../../../etc/passwd", "admin"),
        ("'; DROP TABLE users;--", "admin"),
        ("<img src=x onerror=alert(1)>", "qwerty"),
        ("<svg/onload=alert(1)>", "qwe123"),
        ("☠️💀🔥", "💣💥"),
        ("test@test.com", "' OR 1=1--"),
        ("<iframe src=javascript:alert(1)>", "pass")
    ])
    def test_register_with_fuzz_payloads(self, register_api, email, password, logger):
        with allure.step(f'Регистрация с вредоносными данными: {email} / {password}'):
            response = register_api.register_user(email=email, password=password)
            logger.info(f"[Fuzz Register] Email: {email}, Password: {password}")
            logger.info(f"[Fuzz Register] Ответ: {response.status_code} - {response.text}")

            assert response.status_code in [HTTPStatus.BAD_REQUEST, HTTPStatus.UNAUTHORIZED]

    @allure.story("Фаззинг случайными значениями")
    @pytest.mark.parametrize("attempt", range(10))
    def test_register_with_random_data(self, register_api, attempt, logger):
        email = fake.user_name() + "@example.com"
        password = fake.password(length=32, special_chars=True, digits=True, upper_case=True, lower_case=True)

        with allure.step(f"Fake регистрация #{attempt + 1}"):
            response = register_api.register_user(email=email, password=password)
            logger.info(f"[Faker #{attempt}] Email: {email} Password: {password}")
            logger.info(f"[Faker #{attempt}] Ответ: {response.status_code} - {response.text}")

            assert response.status_code in [HTTPStatus.BAD_REQUEST, HTTPStatus.UNAUTHORIZED]