import allure
import pytest
from http import HTTPStatus

from pydantic import ValidationError
from schemas.user import UserResponse, UserListResponse, User


@allure.epic("Функциональное тестирование пользователей")
@allure.feature("Получения пользователя")
class TestUserAPI:

    @allure.story('Получение одного пользователя')
    @allure.title('Проверка получения пользователя')
    @allure.description('Этот тест проверяет, что API корректно возвращает данные о пользователе по ID')
    @pytest.mark.parametrize("user_id, expected_status", [
        (1, HTTPStatus.OK),  # Пользователь существует
        (2, HTTPStatus.OK),  # Пользователь существует
        (9999, HTTPStatus.NOT_FOUND)  # Пользователь не найден
    ])
    def test_get_user(self, user_api, user_id, expected_status, logger):
        with allure.step(f'Отправляем GET-запрос на /api/users/{user_id}'):
            response = user_api.get_single_user(user_id)
            logger.info(f"Запрос: GET /api/users/{user_id}")
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status

        if response.status_code == HTTPStatus.OK:
            with allure.step('Проверка структуры данных'):

                try:
                    user_data = UserResponse(**response.json())
                    logger.info(f"Данные пользователя успешно валидированы: {user_data}")
                    assert user_data.data.id == user_id, f"ID пользователя в ответе {user_data.data.id}, ожидалось {user_id}"
                except ValidationError as e:
                    logger.error(f"Ошибка валидации данных пользователя: {e}")
                    pytest.fail(f"Ошибка валидации: {e}")

    @allure.story("Получение всех пользователей")
    @allure.title("Проверка получения всех пользователей")
    @allure.description('Этот тест проверяет, что API корректно возвращает данные о пользователях по ID')
    @pytest.mark.parametrize("page, expected_status", [
        (1, HTTPStatus.OK),
        (2, HTTPStatus.OK),
        (3, HTTPStatus.OK),  # Доп. проверка
        (100, HTTPStatus.OK),  # API всегда возвращает 200, даже если страница пуста
        (0, HTTPStatus.OK),  # Граничное значение (API интерпретирует как page=1)
        (-1, HTTPStatus.OK),  # Отрицательное значение (API может интерпретировать
        ("text", HTTPStatus.OK)  # Некорректный формат (API, может вернуть 200
    ])
    def test_get_users_list(self, user_api, page, expected_status, logger):
        with allure.step(f'Отправляем GET-запрос на /api/users/?page={page}'):
            response = user_api.get_list_users(page)
            logger.info(f"Запрос: GET /api/users?page={page}")
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидался статус {expected_status}, "
                                                             f"но получен {response.status_code}")
        if response.status_code == HTTPStatus.OK:
            with allure.step('Проверка структуры данных'):
                try:
                    users_list = UserListResponse(**response.json())
                    logger.info(f"Данные пользователя успешно валидированы: {users_list}")

                    assert users_list.page == page or page <= 0, f"Ожидалась страница {page}, но в ответе {users_list.page}"
                    assert isinstance(users_list.data, list), "Поле 'data' должно быть списком"
                    if users_list.data:  # Если пользователи есть, проверим ID первого
                        assert isinstance(users_list.data[0].id, int), "ID пользователя должен быть числом"

                except ValidationError as e:
                    logger.error(f"Ошибка валидации данных пользователей: {e}")
                    pytest.fail(f"Ошибка валидации: {e}")

    @allure.story("Создание пользователя")
    @allure.title("Проверка создания пользователя")
    @allure.description("Этот тест проверяет, может ли этот API корректно создать нового пользователя")
    @pytest.mark.parametrize("new_user, expected_status", [
        ({
             "name": "Tomas",
             "job": "tester"
         }, HTTPStatus.CREATED),  # Успешное создание
        ({}, HTTPStatus.BAD_REQUEST),  # Пустое тело
        ({'name': "test_name"}, HTTPStatus.BAD_REQUEST),  # Неполные данные
        ({'name': 'Michael', 'job': ""}, HTTPStatus.BAD_REQUEST),  # Пользователь с пустым полем job
        ({'name': '', 'job': 'dev'}, HTTPStatus.BAD_REQUEST),  # Пользователь с пустым именем
        ({'job': 'lead'}, HTTPStatus.BAD_REQUEST),  # Отсутствует name
        ({"name": "a" * 256, 'job': 'b' * 256}, HTTPStatus.BAD_REQUEST),  # Длинные данные
        ({'name': "      ", "job": "          "}, HTTPStatus.BAD_REQUEST),  # Данные состоящие из пробелов
        ({'name': '12515151', "job": '1351561361'}, HTTPStatus.BAD_REQUEST),  # Данные состоящие из цифр
        ({'name': '!@#$!%!%!%!@#))((*', 'job': '$!$!%!%!%(!(@(#!(#'}, HTTPStatus.BAD_REQUEST),
        # Данные состоящие из спец. симоволов
        ({'name': "'; DROP TABLE users;--", "job": 'QA'}, HTTPStatus.BAD_REQUEST)

    ])
    def test_create_user(self, user_api, new_user, expected_status, logger):
        with allure.step(f'Отправляем POST-запрос на /api/users'):
            response = user_api.create_user(new_user)
            logger.info(f"Запрос: POST /api/users")
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status}, "
                                                             f"но получен: {response.status_code}")

        if response.status_code == HTTPStatus.CREATED:
            with allure.step('Проверка структуры данных'):
                try:
                    user_data = response.json()
                    assert 'id' in user_data, "В ответе отсутствует поле id"
                    assert 'createdAt' in user_data, 'В ответе отсутствует поле CreatedAt'

                    # Валидация полей name и job
                    user = User(id=user_data['id'],
                                email="",
                                first_name=new_user.get('name', ''),
                                last_name='',
                                avatar='')
                    logger.info(f'Созданные пользователь: {user}')
                except ValidationError as e:
                    logger.error(f'Ошибка валидации ответа API: {e}')
                    pytest.fail(f'Ошибка валидации: {e}')

    @allure.story('Обновление пользователя')
    @allure.title('Проверка обновления пользователя')
    @allure.description('Этот тест проверяет, может ли этот API, корректно обновить данные пользователя')
    @pytest.mark.parametrize('user_id, update_user, expected_status', [
        (2, {'name': 'Luka', 'job': 'resident'}, HTTPStatus.OK),
        (9999, {'name': "Tom", "job": "dev"}, HTTPStatus.OK),
        (1, {}, HTTPStatus.OK)
    ])
    def test_updated_user(self, user_api, user_id, update_user, expected_status, logger):
        with allure.step(f'Отправляем PUT-запрос на /api/users/{user_id}'):
            response = user_api.update_user(user_id, update_user)
            logger.info(f"Запрос: PUT /api/users/{user_id}")
            logger.info(f'Ответ: {response.status_code} - {response.text}')
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status},"
                                                             f"но получен: {response.status_code}")

        if response.status_code == HTTPStatus.OK:
            with allure.step('Проверка структуры данных'):
                try:
                    user_data = response.json()
                    assert 'updatedAt' in user_data, "В ответе отсутствует поле updatedAt"

                    logger.info(f"Обновлённые данные пользователя: {user_data}")

                except ValidationError as e:
                    logger.error(f'Ошибка валидации ответа API: {e}')
                    pytest.fail(f'Ошибка валидации: {e}')

    @allure.story("Удаление пользователя")
    @allure.title("Проверка на удаление пользователя")
    @allure.description("Этот тест проверяет, может ли этот API удалить пользователя")
    @pytest.mark.parametrize("user_id, expected_status", [
        (1, HTTPStatus.NO_CONTENT),
        (9999, HTTPStatus.NO_CONTENT)
    ])
    def test_delete_user(self, user_api, user_id, expected_status, logger):
        with allure.step(f'Отправляем DELETE-запрос на /api/users/{user_id}'):
            response = user_api.delete_user(user_id)
            logger.info(f'Запрос: DELETE /api/users{user_id}')
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидаемый ответ: {expected_status},"
                                                             f"но получен: {response.status_code}")

        with allure.step('Проверяем, что пользователь удалён'):
            response_check = user_api.get_single_user(user_id)
            logger.info(f'Запрос: GET /api/users{user_id}')
            logger.info(f'Ответ: {response_check.status_code} - {response_check.text}')
            assert response_check.status_code == HTTPStatus.NOT_FOUND, "Удалённый пользователь всё ещё существует!"
