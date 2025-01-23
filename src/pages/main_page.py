import allure

from src.config.config import config
from src.pages.base_page import BasePage
from selenium.webdriver.common.by import By


class MainPage(BasePage):
    """
    Класс для работы с главной страницей приложения.
    Содержит методы для взаимодействия с основными элементами главной страницы.
    """

    AVATAR_LOCATOR = (By.CLASS_NAME, "avatar")
    SCHEDULE_TAB_LOCATOR = (By.ID, "left-menu-item:Расписание")

    def __init__(self, driver):
        """
        Инициализация главной страницы.

        Args:
            driver: экземпляр веб-драйвера
        """
        super().__init__(driver)
        self.url = config.BASE_URL

    @allure.step("Открытие главной страницы")
    def open(self) -> None:
        """
        Открывает главную страницу приложения.

        Returns:
            None
        """
        self.driver.get(self.url)

    @allure.step("Проверка авторизации пользователя")
    def is_user_logged_in(self) -> bool:
        """
        Проверяет, авторизован ли пользователь, по наличию аватара.

        Returns:
            bool: True если пользователь авторизован, False если нет
        """
        return self.is_element_present(self.AVATAR_LOCATOR)

    @allure.step("Проверка наличия вкладки расписания")
    def has_schedule_tab(self) -> bool:
        """
        Проверяет наличие вкладки с расписанием на странице.

        Returns:
            bool: True если вкладка присутствует, False если отсутствует
        """
        return self.is_element_present(self.SCHEDULE_TAB_LOCATOR)

    @allure.step("Переход на вкладку расписания")
    def click_to_schedule_tab(self) -> None:
        """
        Осуществляет переход на вкладку с расписанием.

        Returns:
            None

        Raises:
            TimeoutException: если элемент не найден за отведенное время
            ElementClickInterceptedException: если элемент не кликабелен
        """
        self.click(self.SCHEDULE_TAB_LOCATOR)
