import allure

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from src.config.config import config
from src.pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Страница входа в систему.
    Содержит методы для взаимодействия с элементами страницы входа.
    """
    # Локаторы элементов страницы входа
    AVATAR_LOCATOR = (By.CLASS_NAME, "avatar")
    SWITCH_TO_EMAIL_FORM = (By.CSS_SELECTOR, ".js-phone-form-to-username-password")
    EMAIL_PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='password']")
    LOGIN_PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='username']")
    LOGIN_BUTTON_SUBMIT = (By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[1]/div/form/div[5]/button")
    LOGIN_FORM = (By.CLASS_NAME, "js-authentication-form-window")

    def __init__(self, driver):
        """
        Инициализирует LoginPage, наследуя от BasePage

        Args:
            driver: Объект веб-драйвера
        """
        super().__init__(driver)
        self.url = config.LOGIN_URL

    @allure.step("Открытие страницы входа")
    def open(self) -> None:
        """
        Открывает страницу входа по URL, указанному в атрибуте url
        """
        self.driver.get(self.url)

    @allure.step("Переключение на форму входа по email и паролю")
    def switch_to_username_password(self) -> None:
        """
        Нажимает на кнопку, чтобы переключиться на форму входа по email и паролю
        """
        self.click(self.SWITCH_TO_EMAIL_FORM)
        WebDriverWait(self.driver, 10).until(
            ec.visibility_of_element_located(self.EMAIL_PASSWORD_INPUT))

    @allure.step("Ввод email: {email}")
    def enter_email(self, email: str) -> None:
        """
        Вводит email в соответствующее поле

        Args:
            email: Строка с email
        """
        self.input_text(self.LOGIN_PASSWORD_INPUT, email)

    @allure.step("Ввод пароля")
    def enter_password(self, password: str) -> None:
        """
        Вводит пароль в соответствующее поле

        Args:
            password: Строка с паролем
        """
        self.input_text(self.EMAIL_PASSWORD_INPUT, password)

    @allure.step("Нажатие кнопки 'Войти'")
    def click_login_button(self) -> None:
        """
        Нажимает на кнопку "Войти"
        """
        self.click(self.LOGIN_BUTTON_SUBMIT)

    @allure.step("Проверка наличия формы входа")
    def is_login_form_present(self) -> bool:
        """
        Проверяет, присутствует ли на странице форма входа
        """
        return self.is_element_present(self.LOGIN_FORM)

    @allure.step("Проверка авторизации пользователя")
    def is_user_logged_in(self) -> bool:
        return self.is_element_present(self.AVATAR_LOCATOR)

    @allure.step("Выполнение входа в систему")
    def login(self, email: str, password: str) -> None:
        """
        Выполняет полный процесс входа в систему.

        Args:
            email: email пользователя
            password: пароль пользователя
        """
        self.open()
        self.switch_to_username_password()
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()
