import pytest
import allure
import time
from http import HTTPStatus
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.perfomance_helpers import attach_perf_stats

@allure.epic("Тестирование производительности")
@allure.feature("Регистрация")
@allure.story("Нагрузка на /api/register")
@allure.title("Тест производительности registration API")
@allure.description("Тест проверяет, выдержит ли эндпоинт /api/register нагрузку из 10-50-100 одновременных запросов")
@pytest.mark.parametrize("request_count", [10, 50, 100])
def test_register_user_performance(register_api, request_count, logger):
    data = {
        "email": "eve.holt@reqres.in",
        "password": "pistol"
    }

    durations = []

    def send_request():
        start = time.perf_counter()
        response = register_api.register_user(**data)
        duration = time.perf_counter() - start
        return response, duration

    with allure.step(f"Отправка {request_count} параллельных запросов на /api/register"):
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(send_request) for _ in range(request_count)]
            for future in as_completed(futures):
                response, duration = future.result()
                durations.append(duration)

                assert response is not None, "Ошибка: API вернул None"
                assert response.status_code == HTTPStatus.OK, \
                    f"Ожидался статус 200, но был {response.status_code}"
                assert "token" in response.json(), "Ответ не содержит token"

    attach_perf_stats("Регистрация", request_count, durations)