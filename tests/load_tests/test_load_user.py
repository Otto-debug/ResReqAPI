import pytest
import allure
import time
from http import HTTPStatus
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.perfomance_helpers import attach_perf_stats

@allure.epic('Нагрузочное тестирование')
@allure.feature('Создание пользователя')
@allure.story('Нагрузка на /api/users')
@allure.title("Тест производительности user creation API")
@allure.description("Тест проверяет, выдержит ли эндпоинт /api/users нагрузку из 10-50-100 одновременных запросов")
@pytest.mark.parametrize("request_count", [10, 50, 100])
def test_load_users(user_api, request_count, logger):
    new_user_data = {
        "name": "Tomas",
        "job": "tester"
    }

    durations = []

    def send_request():
        start = time.perf_counter()
        response = user_api.create_user(new_user_data)
        duration = time.perf_counter() - start
        return response, duration

    with allure.step(f'Отправка {request_count} параллельных запросов на /api/users'):
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(send_request) for _ in range(request_count)]
            for future in as_completed(futures):
                response, duration = future.result()
                durations.append(duration)

                assert response is not None, "Ошибка: API вернул None"
                assert response.status_code == HTTPStatus.CREATED, \
                    f"Ожидался статус 201, но был {response.status_code}"
                assert "id" in response.json(), "Ответ не содержит id"

    attach_perf_stats("Создание пользователя", request_count, durations)
