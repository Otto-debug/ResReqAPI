import pytest
import logging

from src.api.user_api import UserAPI
from src.api.register_api import RegisterAPI
from src.api.login_api import LoginAPI

@pytest.fixture(scope='session')
def base_url():
    """
    Базовый URL API
    """
    return 'https://reqres.in'

@pytest.fixture(scope='session')
def user_api(base_url):
    return UserAPI(base_url=base_url)

@pytest.fixture(scope='session')
def register_api(base_url):
    return RegisterAPI(base_url=base_url)

@pytest.fixture(scope='session')
def login_api(base_url):
    return LoginAPI(base_url=base_url)

@pytest.fixture(scope='session', autouse=True)
def logger():
    """
    Настройка логирования для тестов.
    Логи отображаются в консоли для упрощения отладки
    """
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    # Логирование в файл
    file_handler = logging.FileHandler('logs/api.log', encoding='utf-8', mode='a')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """
    Конфигурация Pytest для интеграции Allure
    """

    # Настройка allure
    if hasattr(config, "option"):
        allure_dir = getattr(config.option, 'alluredir', None)
        if allure_dir:
            logging.info(f"Allure reports will be saved in: {allure_dir}")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Хук для добавления шагов в Allure на основании статуса теста
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == 'call' and report.failed:
        from allure_commons._allure import attach
        from allure_commons.types import AttachmentType

        # Добавление данных в отчёт при провале теста
        attach(body=str(report.longrepr),
               name="Test Failure Log",
               attachment_type=AttachmentType.TEXT)