import pytest
import allure
import time
from http import HTTPStatus
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.perfomance_helpers import attach_perf_stats

@allure.epic("Тестирование производительности")
@allure.feature("Логин")
@allure.story("Нагрузка на /api/login")
@allure.title("Тест производительности user creation API")
@allure.description("Тест проверяет, выдержит ли эндпоинт /api/login нагрузку из 10-50-100 одновременных запросов")
@pytest.mark.parametrize("request_count", [10, 50, 100])
def test_load_login(login_api, request_count, logger):
    email = "eve.holt@reqres.in"
    password = "pistol"

    durations = []

    def send_request():
        start_time = time.perf_counter()
        response = login_api.login_user(email=email, password=password)
        duration = time.perf_counter() - start_time
        return response, duration

    with allure.step(f"Отправка {request_count} параллельных login-запросов"):
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(send_request) for _ in range(request_count)]
            for future in as_completed(futures):
                response, duration = future.result()
                durations.append(duration)
                assert response is not None, "Ошибка: API вернул None"
                assert response.status_code == HTTPStatus.OK, f"Ожидался статус 200, но был {response.status_code}"
                assert "token" in response.json(), "Ответ не содержит токен"

    attach_perf_stats("Логин", request_count, durations)

# def test_login_load(login_api, logger):
#     email = "eve.holt@reqres.in"
#     password = "pistol"
#     number_of_requests = 50
#     max_response_time = 1.5
#
#     results = []
#     errors = []
#
#     start_time = time.time()
#
#     def send_login():
#         start = time.time()
#         response = login_api.login_user(email=email, password=password)
#         duration = time.time() - start
#
#         if response is None:
#             return {"status": "error", "time": duration, "reason": "No response"}
#         if response.status_code != HTTPStatus.OK:
#             return {"status": "error", "time": duration, "reason": f"Status {response.status_code}"}
#         return {"status": "ok", "time": duration}
#
#     with ThreadPoolExecutor(max_workers=10) as executor:
#         futures = [executor.submit(send_login) for _ in range(number_of_requests)]
#         for future in as_completed(futures):
#             result = future.result()
#             results.append(result)
#             if result["status"] == "error":
#                 errors.append(result)
#
#     total_time = time.time() - start_time
#     avg_response_time = sum([r["time"] for r in results]) / len(results)
#
#     logger.info(f"Общее время выполнения: {total_time:.2f} сек")
#     logger.info(f"Среднее время ответа: {avg_response_time:.2f} сек")
#     logger.info(f"Ошибки: {errors}")
#
#     with allure.step("Проверка, что не было ошибок в запросах"):
#         assert len(errors) == 0, f"Обнаружены ошибки при нагрузке: {errors}"
#
#     with allure.step(f"Проверка, что среднее время ответа < {max_response_time} сек"):
#         assert avg_response_time < max_response_time, f"Слишком долгое время отклика: {avg_response_time:.2f} сек"