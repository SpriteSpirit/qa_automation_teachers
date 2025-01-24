from typing import Optional

import allure
import pytz

from src.config.config import config
from datetime import datetime, timezone
from src.pages.base_page import BasePage
from src.utils.logger_utils import logger

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec


class SchedulePage(BasePage):
    """
    Страница с расписанием.
    Содержит методы для работы с личными событиями в расписании.
    """

    # Локаторы основных элементов
    ADD_EVENT_BUTTON = (By.CSS_SELECTOR, "ds-icon[target='schedule page - icon plus - click']")
    PERSONAL_EVENT_TAB = (
        By.XPATH, "//*[@id='cdk-overlay-0']/cabinet-schedule-class-slot-modal/sky-ui-popup/div/div/div[2]\
        /div/div[1]/div/sky-ui-tabs/div/sky-ui-tab[2]")

    # Локаторы формы личного события
    EVENT_NAME_INPUT = (By.XPATH, "//*[@id='cdk-overlay-0']/cabinet-schedule-class-slot-modal/sky-ui-popup/div\
    /div/div[2]/div/div[2]/cabinet-schedule-personal-event-form/div/div[1]/input")
    EVENT_DESCRIPTION = (By.XPATH, "//*[@id='cdk-overlay-0']/cabinet-schedule-class-slot-modal/sky-ui-popup/div\
    /div/div[2]/div/div[2]/cabinet-schedule-personal-event-form/div/div[4]/textarea")
    DAY_DROPDOWN = (By.XPATH, "//*[@id='cdk-overlay-0']/cabinet-schedule-class-slot-modal/sky-ui-popup/div/div/div[2]\
    /div/div[2]/cabinet-schedule-personal-event-form/div/div[2]/select")

    # Локаторы времени
    TIME_PICKER_START_HH = "//app-time-picker[1]//input[contains(@class, 'input-hours')]"
    TIME_PICKER_START_MM = "//app-time-picker[1]//input[contains(@class, 'input-minutes')]"
    TIME_PICKER_END_HH = "//app-time-picker[2]//input[contains(@class, 'input-hours')]"
    TIME_PICKER_END_MM = "//app-time-picker[2]//input[contains(@class, 'input-minutes')]"
    PERSONAL_EVENT_CONTAINER = (By.CSS_SELECTOR, "tcc-calendar-event-personal")
    SAVE_SUBMIT_BUTTON = (By.XPATH,
                          "//*[@id='cdk-overlay-0']/cabinet-schedule-class-slot-modal/sky-ui-popup/div/div/div[2]\
                          /div/div[2]/cabinet-schedule-personal-event-form/div/div[6]/sky-ui-button/button")

    DELETE_CONFIRM_BUTTON = (By.CSS_SELECTOR,
                             'sky-ui-button[target="schedule page - personal event modal - remove button - click"] \
                             button')

    def __init__(self, driver):
        """
        Инициализация страницы расписания.

        Args:
            driver: экземпляр веб-драйвера
        """
        super().__init__(driver)
        self.url = config.SCHEDULE_URL

    @allure.step("Открытие страницы расписания")
    def open(self) -> None:
        """
        Открывает страницу расписания.

        Returns:
            None
        """
        self.driver.get(self.url)

    @allure.step("Проверка наличия кнопки создания события")
    def is_add_event_in(self) -> bool:
        """
        Проверяет наличие кнопки добавления события на странице.

        Returns:
            bool: True если кнопка присутствует, False если отсутствует
        """
        return self.is_element_present(self.ADD_EVENT_BUTTON)

    @allure.step("Нажатие кнопки добавления события")
    def click_add_event_button(self) -> None:
        """
        Нажимает кнопку добавления нового события.

        Returns:
            None
        """
        WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable(self.ADD_EVENT_BUTTON)
        )
        self.click(self.ADD_EVENT_BUTTON)

    @allure.step("Переключение на вкладку 'Личные события'")
    def switch_to_personal_event_tab(self) -> None:
        """
        Переключает на вкладку личных событий.

        Returns:
            None
        """
        WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable(self.PERSONAL_EVENT_TAB)
        )
        self.click(self.PERSONAL_EVENT_TAB)

    @allure.step("Ввод названия личного события: {personal_event_name}")
    def enter_personal_event_name(self, personal_event_name: str) -> None:
        """
        Вводит название личного события.

        Args:
            personal_event_name: название события

        Returns:
            None
        """
        WebDriverWait(self.driver, 10).until(
            ec.visibility_of_element_located(self.EVENT_NAME_INPUT)
        )
        self.input_text(self.EVENT_NAME_INPUT, personal_event_name)

    @allure.step("Ввод описания личного события")
    def enter_personal_event_description(self, personal_event_description: str) -> None:
        """
        Вводит описание личного события.

        Args:
            personal_event_description: описание события

        Returns:
            None
        """
        self.input_text(self.EVENT_DESCRIPTION, personal_event_description)

    @allure.step("Открытие выпадающего списка дат")
    def click_on_day_dropdown_list(self) -> None:
        """
        Открывает выпадающий список для выбора даты.

        Returns:
            None
        """
        WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable(self.DAY_DROPDOWN)
        )
        self.click(self.DAY_DROPDOWN)

    @allure.step("Выбор даты: {date}")
    def click_day_options_from_drop_down_list(self, date: str) -> None:
        """
        Выбирает дату из выпадающего списка.

        Args:
            date: дата в формате 'YYYY-MM-DD' (локальное время Москвы).
        """
        select_element = self.find_element(self.DAY_DROPDOWN)
        WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable(select_element)
        )
        select = Select(select_element)
        options = select.options

        local_tz = pytz.timezone("Europe/Moscow")

        for option in options:
            # Получаем значение атрибута value (UTC дата)
            option_value_utc = option.get_attribute("value")
            # Парсим UTC дату
            utc_date = datetime.fromisoformat(option_value_utc.replace("Z", ""))
            utc_date = utc_date.replace(tzinfo=timezone.utc)
            # Конвертируем в московское время
            local_date = utc_date.astimezone(local_tz)
            # Форматируем в 'YYYY-MM-DD'
            option_date = local_date.strftime("%Y-%m-%d")

            if date == option_date:
                logger.debug(f'Найдена дата: {option_date}, значение: {option_value_utc}')
                option.click()
                return

    @allure.step("Прокрутка к элементу на странице")
    def scroll_to_element(self, element):
        """
        Прокрутка к элементу на странице
        """
        actions = ActionChains(self.driver)
        actions.scroll_to_element(element).perform()
        # actions.move_to_element(element).perform()

    @allure.step("Выбор времени начала: {start_time} и окончания: {end_time}")
    def select_time_picker(self, start_time: str, end_time: str) -> None:
        """
        Выбирает время начала и окончания события.

        Args:
            start_time: время начала в формате "HH:MM"
            end_time: время окончания в формате "HH:MM"
        """

        start_hh, start_mm = start_time.split(":")
        end_hh, end_mm = end_time.split(":")

        start_hh_element = self.driver.find_element(By.XPATH, self.TIME_PICKER_START_HH)
        start_mm_element = self.driver.find_element(By.XPATH, self.TIME_PICKER_START_MM)

        start_hh_element.click()
        start_hh_element.clear()
        start_hh_element.send_keys(start_hh)

        start_mm_element.click()
        start_mm_element.clear()
        start_mm_element.send_keys(start_mm)

        end_hh_element = self.driver.find_element(By.XPATH, self.TIME_PICKER_END_HH)
        end_mm_element = self.driver.find_element(By.XPATH, self.TIME_PICKER_END_MM)

        end_hh_element.click()
        end_hh_element.clear()
        end_hh_element.send_keys(end_hh)

        end_mm_element.click()
        end_mm_element.clear()
        end_mm_element.send_keys(end_mm)

    @allure.step("Подтверждение создания личного события")
    def click_create_personal_event_submit_button(self) -> None:
        """
        Нажимает кнопку подтверждения создания события.

        Returns:
            None
        """
        WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable(self.SAVE_SUBMIT_BUTTON)
        )
        self.click(self.SAVE_SUBMIT_BUTTON)

    @allure.step("Создание личного события")
    def create_personal_event(self, event_name: str, event_description: str, date: str, start_time: str,
                              end_time: str) -> None:
        """
        Создает новое личное событие
        """
        self.click_add_event_button()
        self.switch_to_personal_event_tab()
        self.enter_personal_event_name(event_name)
        self.enter_personal_event_description(event_description)
        self.click_on_day_dropdown_list()
        self.click_day_options_from_drop_down_list(date)
        self.select_time_picker(start_time, end_time)
        self.click_create_personal_event_submit_button()

    @allure.step("Проверка создания личного события")
    def is_personal_event_created(self, event_name: str) -> bool:
        """
        Проверяет, создано ли личное событие
        """
        event_locator = (By.XPATH, f"//div[contains(text(), '{event_name}')]")
        return self.is_element_present(event_locator)

    @allure.step("Удаление личного события")
    def delete_personal_event(self, event: WebElement) -> None:
        """
        Удаляет личное событие.

        Args:
            event: Событие
        """
        try:
            self.click(event)
            delete_button = WebDriverWait(self.driver, 10).until(
                ec.element_to_be_clickable(self.DELETE_CONFIRM_BUTTON)
            )
            delete_button.click()
            logger.debug("Кнопка удаления нажата.")

            try:
                WebDriverWait(self.driver, 10).until(ec.invisibility_of_element_located((By.XPATH,
                                                                                         "//div[@class='event' and contains(.,'Test Событие')]")))
                logger.debug("Событие успешно удалено (ожидание завершено)")
            except TimeoutException:
                logger.warning("Ожидание удаления события истекло.")

        except TimeoutException:
            logger.error(
                f"Не удалось найти или кликнуть по кнопке удаления события.  Локатор: {self.DELETE_CONFIRM_BUTTON}")
            raise

        except NoSuchElementException:
            logger.error(f"Кнопка удаления не найдена для события {event}.  Локатор: {self.DELETE_CONFIRM_BUTTON}")
            raise

    @allure.step("Получение личного события из расписания")
    def get_personal_event_from_schedule(self, event_name: str, event_start_time: str,
                                         event_end_time: str) -> Optional[WebElement]:
        """
        Возвращает личное событие по имени и времени из расписания.
        Возвращает None, если событие не найдено.
        """
        calendar_events = self.find_elements(self.PERSONAL_EVENT_CONTAINER)
        logger.debug(f'Найдено {len(calendar_events)} личных событий')

        for event in calendar_events:
            try:
                long_view_container = event.find_element(By.CSS_SELECTOR, 'div.long-view')
                event_title = long_view_container.find_element(By.CSS_SELECTOR, '.long-view__title').text
                event_time = long_view_container.find_element(By.CSS_SELECTOR, '.long-view__time').text
            except NoSuchElementException:
                logger.debug("Элемент 'div.long-view' или его потомки не найдены в текущем блоке.")
                continue  # Skip this event

            if event_title == event_name:
                start_event_time = event_time.split()[0]
                end_event_time = event_time.split()[2]

                if event_start_time == start_event_time and event_end_time == end_event_time:
                    logger.debug(f'Найдено событие: {event}')
                    return event

        logger.debug(f"Событие {event_name} c временем {event_start_time} - {event_end_time} не найдено.")
        return None

    @allure.step("Проверка существования личного события в расписании")
    def is_doesnt_exist_personal_event(self, event_name: str, event_start_time: str,
                                       event_end_time: str) -> bool:
        """
        Проверка существования личного события в расписании
        """
        return self.get_personal_event_from_schedule(event_name, event_start_time, event_end_time) is None
