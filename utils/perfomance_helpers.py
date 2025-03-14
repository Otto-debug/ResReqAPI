import allure

def attach_perf_stats(endpoint_name: str, request_count: int, durations: list):
    total = sum(durations)
    avg = total / len(durations)
    max_time = max(durations)
    min_time = min(durations)

    stats_text = (
        f"📌 Эндпоинт: {endpoint_name}\n"
        f"🔁 Количество запросов: {request_count}\n"
        f"⏱ Общее время: {total:.2f} сек\n"
        f"📊 Среднее время: {avg:.3f} сек\n"
        f"🔺 Макс: {max_time:.3f} сек | 🔻 Мин: {min_time:.3f} сек"
    )

    allure.attach(
        stats_text,
        name=f"Статистика производительности ({endpoint_name})",
        attachment_type=allure.attachment_type.TEXT
    )