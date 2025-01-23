import os
import pytest
import allure
import requests

from selenium import webdriver

from src.data.test_data import TestData
from src.api.api_client import ApiClient
from src.pages.login_page import LoginPage
from src.utils.logger_utils import logger


@pytest.fixture(scope="function")
def browser():
    driver = webdriver.Chrome()
    driver.maximize_window()

    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def auth(browser):
    """
    Фикстура для авторизации пользователя перед тестами.
    """
    login_page = LoginPage(browser)
    login_page.open()
    login_page.login(TestData.VALID_EMAIL, TestData.VALID_PASSWORD)
    return browser


@pytest.fixture
def authorized_api_client() -> ApiClient:
    """
    Авторизованный клиент API.
    """

    session = requests.Session()
    token = os.getenv('GLOBAL_TOKEN')
    client = ApiClient(session=session, token=token)

    return client


@pytest.fixture(autouse=False)
def make_screenshot_on_fail(request, authenticated_driver) -> None:
    """
     Фикстура для сбора отладочной информации при падении теста.

     Собирает:
     - Скриншот страницы
     - URL страницы
     - HTML-код страницы

     Args:
         request: объект запроса теста
         authenticated_driver: инициализированный драйвер браузера
     """

    def fin():
        """
        Запускается после завершения теста.
        Если тест завершился с ошибкой, собирает и добавляет скриншот, URL и HTML-код страницы в Allure-отчет.
        Эта функция добавляется в список финализаторов с помощью `request.addfinalizer(fin)`.
        """

        if request.node.rep_setup.failed or request.node.rep_call.failed:
            # Скриншот
            allure.attach(
                authenticated_driver.get_screenshot_as_png(),
                name=f"Скриншот при ошибке: {request.node.name}",
                attachment_type=allure.attachment_type.PNG)

            # URL страницы на момент падения
            allure.attach(
                authenticated_driver.current_url,
                name="URL страницы при сбое",
                attachment_type=allure.attachment_type.TEXT)

            # HTML страницы
            allure.attach(
                authenticated_driver.page_source,
                name="Источник страницы при сбое",
                attachment_type=allure.attachment_type.HTML)

            logger.error(f"Тест '{request.node.name}' завершился с ошибкой. Собраны скриншот, URL и HTML страницы")

    request.addfinalizer(fin)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call) -> None:
    """
    Хук для отслеживания статуса теста.

    Args:
        item: объект теста
        call: информация о текущей фазе выполнения теста

    Каждый тест проходит через 3 фазы:
    - "setup" - подготовка теста
    - "call" - выполнение теста
    - "teardown" - очистка после теста
    """

    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture
def create_personal_event(authorized_api_client) -> dict:
    event_data = TestData.get_personal_event(
        title=f"Событие с валидными данными{TestData.PERSONAL_EVENT_NAME}",
        date=TestData.date(),
        start_at=TestData.PERSONAL_EVENT_START_TIME,
        end_at=TestData.PERSONAL_EVENT_END_TIME
    )

    response = authorized_api_client.post(
        "/createPersonal",
        data=event_data
    )

    return response.json()
