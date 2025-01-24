import allure
import pytest

from src.data.test_data import TestData
from src.pages.main_page import MainPage
from src.utils.logger_utils import logger
from src.pages.login_page import LoginPage
from src.pages.schedule_page import SchedulePage


FEATURE = "UI tests"
STORY_LOGIN = "Login"
STORY_SCHEDULE = "Schedule"


@allure.feature(FEATURE)
@allure.story(STORY_LOGIN)
@pytest.mark.ui
def test_successful_login(browser):
    """
    Тест успешной авторизации
    """
    with allure.step("Открыть страницу авторизации"):
        login_page = LoginPage(browser)
        login_page.open()

    with allure.step("Переключиться на форму входа по email"):
        login_page.switch_to_username_password()

    with allure.step("Ввести email"):
        login_page.enter_email(TestData.VALID_EMAIL)

    with allure.step("Ввести пароль"):
        login_page.enter_password(TestData.VALID_PASSWORD)

    with allure.step("Нажать на кнопку войти"):
        login_page.click_login_button()

    with allure.step("Проверить успешную авторизацию"):
        main_page = MainPage(browser)
        assert main_page.is_user_logged_in(), "Пользователь не авторизован"


@allure.feature(FEATURE)
@allure.story(STORY_LOGIN)
@pytest.mark.ui
def test_failed_login_invalid_email(browser):
    """
    Тест неудачной авторизации с невалидным email.
    """
    with allure.step("Открыть страницу авторизации"):
        login_page = LoginPage(browser)
        login_page.open()

    with allure.step("Переключиться на форму входа по email"):
        login_page.switch_to_username_password()

    with allure.step("Ввести невалидный email"):
        login_page.enter_email(TestData.INVALID_EMAIL)

    with allure.step("Ввести пароль"):
        login_page.enter_password(TestData.VALID_PASSWORD)

    with allure.step("Нажать на кнопку 'Войти'"):
        login_page.click_login_button()

    with allure.step("Проверить, что авторизация не прошла"):
        assert not login_page.is_user_logged_in(), "Пользователь авторизован, хотя не должен был"


@allure.feature(FEATURE)
@allure.story(STORY_LOGIN)
@pytest.mark.ui
def test_failed_login_invalid_password(browser):
    """
    Тест неудачной авторизации с невалидным паролем.
    """
    with allure.step("Открыть страницу авторизации"):
        login_page = LoginPage(browser)
        login_page.open()

    with allure.step("Переключиться на форму входа по email"):
        login_page.switch_to_username_password()

    with allure.step("Ввести email"):
        login_page.enter_email(TestData.VALID_EMAIL)

    with allure.step("Ввести невалидный пароль"):
        login_page.enter_password(TestData.INVALID_PASSWORD)

    with allure.step("Нажать на кнопку 'Войти'"):
        login_page.click_login_button()

    with allure.step("Проверить, что авторизация не прошла"):
        assert not login_page.is_user_logged_in(), "Пользователь авторизован, хотя не должен был"


@allure.feature(FEATURE)
@allure.story(STORY_LOGIN)
@pytest.mark.ui
def test_create_personal_event(auth):
    """
    Тест создания личного события.
    """
    with allure.step("Открыть страницу с расписанием"):
        schedule_page = SchedulePage(auth)
        schedule_page.open()

    with allure.step("Создать личное событие"):
        schedule_page.create_personal_event(
            event_name=TestData.PERSONAL_EVENT_NAME,
            event_description=TestData.PERSONAL_EVENT_DESCRIPTION,
            date=TestData.date(),
            start_time=TestData.PERSONAL_EVENT_START_TIME,
            end_time=TestData.PERSONAL_EVENT_END_TIME
        )

    with allure.step("Проверить создание события"):
        assert schedule_page.is_personal_event_created(TestData.PERSONAL_EVENT_NAME), \
            "Событие не найдено в расписании"


@allure.feature(FEATURE)
@allure.story(STORY_SCHEDULE)
@pytest.mark.ui
def test_delete_personal_event(auth):
    """
    Тест удаления личного события.
    """
    with allure.step("Открыть страницу с расписанием"):
        schedule_page = SchedulePage(auth)
        schedule_page.open()

    with allure.step("Создать личное событие"):
        event_name = TestData.PERSONAL_EVENT_NAME

        schedule_page.create_personal_event(
            event_name=event_name,
            event_description=TestData.PERSONAL_EVENT_DESCRIPTION,
            date=TestData.date(),
            start_time=TestData.PERSONAL_EVENT_START_TIME,
            end_time=TestData.PERSONAL_EVENT_END_TIME
        )

    # with allure.step("Обновить страницу"):
    #     schedule_page.driver.refresh()

    with allure.step("Найти и удалить созданное событие"):
        event = schedule_page.get_personal_event_from_schedule(
            event_name,
            TestData.PERSONAL_EVENT_START_TIME,
            TestData.PERSONAL_EVENT_END_TIME
        )
        logger.debug(event)
        if event:
            schedule_page.scroll_to_element(event)
            schedule_page.delete_personal_event(event)

    with allure.step("Проверить, что событие удалено"):
        schedule_page.driver.refresh()
        assert schedule_page.is_doesnt_exist_personal_event(
            TestData.PERSONAL_EVENT_NAME,
            TestData.PERSONAL_EVENT_START_TIME,
            TestData.PERSONAL_EVENT_END_TIME
        ), "Событие не было удалено"
