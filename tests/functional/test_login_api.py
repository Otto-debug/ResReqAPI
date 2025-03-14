import allure
import pytest
from http import HTTPStatus

@allure.epic('Функциональное тестирование логина')
@allure.feature('Логин')
class TestLoginAPI:

    @allure.story('Логин пользователя')
    @allure.title('Проверка на вход пользователя')
    @allure.description('Данные тест проверяет, как API работает с логином')
    @pytest.mark.parametrize("email, password, expected_status", [
        ("eve.holt@reqres.in", "pistol", HTTPStatus.OK),  # Корректные данные
        ("", "", HTTPStatus.BAD_REQUEST),  # Пустые данные
        ("test@test.com", "", HTTPStatus.BAD_REQUEST),  # Только email, без пароля
        ('anna.jonesgmail.com', "Anna123", HTTPStatus.BAD_REQUEST),  # Невалидный формат email
        ('jone123smith@gmail.com', 'j1', HTTPStatus.BAD_REQUEST),  # Короткий пароль (1-2 символа)
        ('harry-osborn@gmail.com', "        ", HTTPStatus.BAD_REQUEST),  # Пароль из пробелов
        ('!@#$%%%^)(*&^-=@gmail.com', "##$!$$!%!%%!%!'''''", HTTPStatus.BAD_REQUEST),  # Спец. символы
        ('sql.injector@gmail.com', "; DROP TABLE users;--", HTTPStatus.UNAUTHORIZED),  # SQL-инъекция
        ('markus_farmer@gmail.com', "A" * 256, HTTPStatus.UNPROCESSABLE_ENTITY),  # Длинный пароль (256 символов)
        ("eve.holt@reqres.in", "pistol", HTTPStatus.OK)  # Повторный вход (зависит от API, если запрещено - 401)
    ])
    def test_login_user(self, login_api, email, password, expected_status, logger):
        with allure.step(f'Отправляем POST-запрос на /api/login с email={email}'):
            response = login_api.login_user(email=email, password=password)
            logger.info(f'Запрос: POST /api/login с email={email}')
            assert response is not None, "Ошибка: API вернул None вместо ответа"

            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status}, "
                                                             f"но получен: {response.status_code}")

            if response.status_code == HTTPStatus.OK:
                with allure.step('Проверяем, что в ответе есть токен'):
                    resp_data = response.json()
                    assert 'token' in resp_data, 'В ответе отсутствует токен'