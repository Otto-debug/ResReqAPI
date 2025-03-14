# ReqRes API Testing Project 🧪

Проект для тестирования публичного API: [reqres.in](https://reqres.in/)  
Покрытие: функциональные, нагрузочные, совместимые, фаззинг и тесты по безопасности.

---

## 📁 Структура проекта

```
ResReqAPI/
│
├── logs/                  # Логи выполнения тестов
├── reports/               # Allure отчёты
│   └── allure-results/
├── schemas/               # Pydantic-схемы для валидации ответов
├── src/
│   └── api/               # Базовые и специфические API-классы
├── tests/
│   ├── compatibility/     # Тесты на совместимость с различными данными
│   ├── functional/        # Основные функциональные тесты
│   ├── load_tests/        # Нагрузочные тесты
│   ├── security/          # Тесты по безопасности (фаззинг, инъекции)
│   └── conftest.py        # Общие фикстуры и настройки
├── utils/                 # Вспомогательные утилиты (например, performance_helpers)
├── Dockerfile             # Docker-инструкция для запуска тестов
├── pytest.ini             # Pytest настройки
└── requirements.txt       # Зависимости проекта
```

---

## 🚀 Установка

```bash
git clone https://github.com/Otto-debug/reqres-api-tests.git
cd ReqResAPI
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate на Windows
pip install -r requirements.txt
```

---

## 🧪 Запуск тестов

### Функциональные тесты:

```bash
pytest tests/functional --alluredir=reports/allure-results
```

### Нагрузочные:

```bash
pytest tests/load_tests --alluredir=reports/allure-results
```

### Тесты на безопасность (фаззинг, XSS, SQL):

```bash
pytest tests/security --alluredir=reports/allure-results
```

---

## 🐳 Docker

### Сборка образа:

```bash
docker build -t reqres-tests .
```

### Запуск тестов внутри Docker:

```bash
docker run --rm reqres-tests
```

Можно изменить `CMD` в Dockerfile под определённую директорию тестов.

---

## 🧾 Allure-отчёты

После запуска можно посмотреть отчёт:

```bash
allure serve reports/allure-results
```

---

## 🔐 Покрытие тестами

- ✅ Регистрация (`/api/register`)
- ✅ Логин (`/api/login`)
- ✅ Пользователи (`/api/users`)
- ✅ Позитивные/негативные сценарии
- ✅ Валидация схем через Pydantic
- ✅ Fuzzing-атаки (XSS, SQL-инъекции)
- ✅ Тесты с минимальными и экстремальными данными
- ✅ Тесты на нагрузку (concurrent users)
- ✅ Docker-интеграция
- ✅ Логгирование

---



---

## 🧑‍💻 Автор

Griffith/Otto-Debug — тестировщик и разработчик ❤️# ResReqAPI
# ResReqAPI
