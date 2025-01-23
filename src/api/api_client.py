import requests
from src.config.config import config


class ApiClient:
    """
    Клиент для взаимодействия с API.

    Предоставляет методы для отправки GET, POST, PUT и DELETE запросов к API.
    """

    def __init__(self, session: requests.Session, token=None):
        self.session = session
        self.base_url = config.API_URL
        self.token = token
        self.session.headers.update({
            "Cookie": f'token_global={token}' if token else "",
            "Content-Type": "application/json"
        })

    def get(self, endpoint, params=None):
        """
        Отправляет GET запрос к API.

        Args:
            endpoint (str): Конечная точка API.
            params (dict, optional): Параметры запроса. Defaults to None.

        Returns:
            requests.Response: Ответ от API.
        """
        url = self.base_url + endpoint
        response = self.session.get(url, params=params)
        return response

    def post(self, endpoint, data=None):
        """
        Отправляет POST запрос к API.

        Args:
            endpoint (str): Конечная точка API.
            data (dict, optional): Данные для отправки. Defaults to None.

        Returns:
            requests.Response: Ответ от API.
        """
        url = self.base_url + endpoint
        response = self.session.post(url, json=data)
        return response

    def put(self, endpoint, data=None):
        """
        Отправляет PUT запрос к API.

        Args:
            endpoint (str): Конечная точка API.
            data (dict, optional): Данные для отправки. Defaults to None.

        Returns:
            requests.Response: Ответ от API.
        """
        url = self.base_url + endpoint
        response = self.session.put(url, json=data)
        return response

    def delete(self, endpoint):
        """
        Отправляет DELETE запрос к API.

        Args:
            endpoint (str): Конечная точка API.

        Returns:
            requests.Response: Ответ от API.
        """
        url = self.base_url + endpoint
        response = self.session.delete(url,)
        return response
