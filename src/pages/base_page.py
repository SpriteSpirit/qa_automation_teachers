import allure
import logging

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    NoSuchElementException
)
from src.config.config import config
from typing import List


class BasePage:
    """
    Базовый класс для страницы сайта.
    Содержит общие методы для работы с элементами страницы.
    """

    def __init__(self, driver):
        self.driver = driver
        self.base_url = config.BASE_URL

    def refresh_page(self):
        """
        Обновляет текущую страницу
        """
        self.driver.refresh()

    @allure.step("Поиск элемента {locator}")
    def find_element(self, locator: tuple[str, str], timeout: int = 10) -> WebElement:
        """
        Поиск элемента на странице.

        Args:
            locator: кортеж с локатором (By.ID, 'id')
            timeout: время ожидания элемента
        """
        custom_wait = WebDriverWait(self.driver, timeout)

        try:
            return custom_wait.until(
                ec.presence_of_element_located(locator),
                message=f"Не найден элемент по локатору {locator}"
            )
        except TimeoutException as e:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="screenshot_error",
                attachment_type=allure.attachment_type.PNG
            )
            raise TimeoutException(f"Элемент {locator} не найден на странице") from e

    @allure.step("Поиск элементов {locator}")
    def find_elements(self, locator: tuple[str, str], timeout: int = 10) -> List[WebElement]:
        """
        Поиск всех элементов на странице по локатору.
        """
        custom_wait = WebDriverWait(self.driver, timeout)

        try:
            return custom_wait.until(
                ec.presence_of_all_elements_located(locator),
                message=f"Не найдены элементы по локатору {locator}"
            )
        except TimeoutException as e:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="screenshot_error",
                attachment_type=allure.attachment_type.PNG
            )
            raise TimeoutException(f"Элементы {locator} не найдены на странице") from e

    @allure.step("Клик по элементу {locator}")
    def click(self, locator: tuple[str, str], timeout: int = 10):
        """
        Клик по элементу с предварительным ожиданием кликабельности элемента.
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                ec.element_to_be_clickable(locator)
            )
            element.click()
        except TimeoutException:
            raise AssertionError(
                f"Не удалось найти или кликнуть по элементу: {locator} за {timeout} секунд.")
        except StaleElementReferenceException:
            try:
                element = WebDriverWait(self.driver, timeout).until(
                    ec.element_to_be_clickable(locator)
                )
                element.click()
            except TimeoutException:
                raise AssertionError(
                    f"Не удалось кликнуть по элементу: {locator} за {timeout} секунд после повторной попытки.")

    @allure.step("Ввод текста '{text}' в поле {locator}")
    def input_text(self, locator: tuple[str, str], text: str, timeout: int = 10) -> None:
        """
        Вводит текст в текстовое поле, используя явные ожидания.

        Args:
            locator: Кортеж (By, value) для поиска элемента.
            text: Текст для ввода.
            timeout: Максимальное время ожидания (в секундах).
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                ec.visibility_of_element_located(locator)
            )
            element.clear()
            element.send_keys(text)
        except TimeoutException:
            raise AssertionError(f"Не удалось найти текстовое поле: {locator} за {timeout} секунд.")

        except StaleElementReferenceException:
            try:
                element = WebDriverWait(self.driver, timeout).until(
                    ec.visibility_of_element_located(locator)
                )
                element.clear()
                element.send_keys(text)
            except TimeoutException:
                raise AssertionError(
                    f"Не удалось ввести текст в поле: {locator} за {timeout} секунд после повторной попытки.")

    @allure.step("Проверка наличия элемента {locator}")
    def is_element_present(self, locator: tuple[str, str], timeout: int = 10) -> bool:
        """
        Проверка наличия элемента на странице.
        """
        try:
            self.find_element(locator, timeout)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    @allure.step("Получение текста элемента {locator}")
    def get_text(self, locator: tuple[str, str], timeout: int = 10) -> str:
        """
        Получение текста элемента.
        """
        try:
            element = self.wait_for_element_visible(locator, timeout)
            return element.text
        except (TimeoutException, StaleElementReferenceException) as e:
            logging.error(f"Ошибка: {e}")
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="get_text_error",
                attachment_type=allure.attachment_type.PNG
            )
            raise

    def wait_for_element_visible(self, locator: tuple[str, str], timeout: int = 10):
        """
        Ожидание видимости элемента.
        """
        custom_wait = WebDriverWait(self.driver, timeout)

        return custom_wait.until(
            ec.visibility_of_element_located(locator),
            message=f"Элемент {locator} не стал видимым"
        )

    def wait_for_element_disappear(self, locator: tuple[str, str], timeout: int = 10):
        """
        Ожидание исчезновения элемента.
        """
        custom_wait = WebDriverWait(self.driver, timeout)

        return custom_wait.until(
            ec.invisibility_of_element_located(locator),
            message=f"Элемент {locator} не исчез"
        )

    def wait_for_element_clickable(self, locator: tuple[str, str], timeout: int = 10) -> WebElement:
        """
        Ожидание кликабельности элемента.

        Args:
            locator: кортеж с локатором (By.ID, 'id')
            timeout: время ожидания в секундах
        """
        return WebDriverWait(self.driver, timeout).until(
            ec.element_to_be_clickable(locator),
            message=f"Элемент {locator} не кликабелен"
        )
