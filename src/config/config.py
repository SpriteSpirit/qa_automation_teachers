class Config:
    """
    Базовая конфигурация для тестов кабинета Teacher Skyeng API и пользовательского интерфейса.
    """

    BASE_URL = "https://teacher.skyeng.ru"
    LOGIN_URL = "https://id.skyeng.ru/login"
    SCHEDULE_URL = "https://teachers.skyeng.ru"
    API_URL = "https://api-teachers.skyeng.ru/v2/schedule"


config = Config()
