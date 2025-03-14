import allure
import pytest
from http import HTTPStatus


@allure.epic("Функциональное тестирование регистрации")
@allure.feature("Регистрация")
class TestRegistrationAPI:

    @allure.story('Регистрация пользователя')
    @allure.title('Проверка на регистрацию пользователя')
    @allure.description('Данный тест проверяет, как данный API регистрирует нового пользователя')
    @pytest.mark.parametrize("email, password, expected_status", [
        ("eve.holt@reqres.in", "pistol", HTTPStatus.OK),  # Корректные данные
        ("", "", HTTPStatus.BAD_REQUEST),  # Пустые данные
        ("test@test.com", "", HTTPStatus.BAD_REQUEST),  # Только email, без пароля
        ('anna.jonesgmail.com', "Anna123", HTTPStatus.BAD_REQUEST),  # Невалидный формат email
        ('jone123smith@gmail.com', 'j1', HTTPStatus.BAD_REQUEST),  # Короткий пароль (1-2) символа
        ('harry-osborn@gmail.com', "        ", HTTPStatus.BAD_REQUEST),  # Пароль из пробелов
        ('!@#$%%%^)(*&^-=@gmail.com', "##$!$$!%!%%!%!'''''", HTTPStatus.BAD_REQUEST),
        # Данные состоящие из спец. символов
        ('sql.injector@gmail.com', "; DROP TABLE users;--", HTTPStatus.BAD_REQUEST), # SQL-инъекция
        ('markus_farmer@gmail.com', "A" * 256, HTTPStatus.BAD_REQUEST), # Пароль состоящий из 256 символов
        ("eve.holt@reqres.in", "pistol", HTTPStatus.BAD_REQUEST) # Повторная регистрация
    ])
    def test_register_user(self, register_api, email, password, expected_status, logger):
        with allure.step(f'Отправляем POST-запрос на /api/register с email={email}'):
            response = register_api.register_user(email=email, password=password)
            logger.info(f"Запрос: POST /api/register с email={email}")
            assert response is not None, "Ошибка: API вернул None вместо ответа"

            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status}, "
                                                             f"но получен: {response.status_code}")

            if response.status_code == HTTPStatus.OK:
                with allure.step('Проверяем, что в ответе есть токен'):
                    response_data = response.json()
                    assert 'token' in response_data, 'В ответе отсутствует токен'
