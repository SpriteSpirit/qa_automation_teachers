import pytest
import allure

from src.data.test_data import TestData
from src.utils.logger_utils import logger


@allure.feature("API тесты")
@allure.story("Личные события")
@allure.title("Создание события с валидными данными")
@pytest.mark.api
@pytest.mark.positive
def test_create_personal_event(authorized_api_client):
    with allure.step("Создание события с валидными данными"):
        response = authorized_api_client.post(
            "/createPersonal",
            data=TestData.get_personal_event(
                title=f"Событие с валидными данными{TestData.PERSONAL_EVENT_NAME}",
                date=TestData.date(),
                start_at="14:00",
                end_at="14:50"
            ))
        logger.debug(f"Response: {response.text}")

        assert response.status_code == 200
        event_id = response.json().get('id')

        return event_id


@allure.feature("API тесты")
@allure.story("Личные события")
@allure.title("Создание двух личных событий на одно время")
@pytest.mark.api
@pytest.mark.positive
def test_create_duplicate_event(authorized_api_client):
    with allure.step("Создание двух личных событий на одно время"):
        with allure.step("Создание первого события"):
            response1 = authorized_api_client.post(
                "/createPersonal",
                data=TestData.get_personal_event(
                    title=f"Первое событие{TestData.PERSONAL_EVENT_NAME}",
                    date=TestData.date(),
                    start_at="14:00",
                    end_at="14:50"
                ))
            assert response1.status_code == 200
            event_id1 = response1.json().get('data').get('payload').get('id')

        with allure.step("Создание второго события"):
            response2 = authorized_api_client.post(
                "/createPersonal",
                data=TestData.get_personal_event(
                    title=f"Второе событие{TestData.PERSONAL_EVENT_NAME}",
                    date=TestData.date(),
                    start_at="14:00",
                    end_at="14:50"
                ))

            assert response2.status_code == 200
            event_id2 = response2.json().get('data').get('payload').get('id')

        assert event_id1 != event_id2, "ID событий должны быть разными"


@allure.feature("API тесты")
@allure.story("Личные события")
@allure.title("Создание события без указания даты и времени")
@pytest.mark.api
@pytest.mark.negative
def test_create_event_without_time(authorized_api_client):
    with allure.step("Создание события без указания времени"):
        response = authorized_api_client.post(
            "/createPersonal",
            data=TestData.get_personal_event(
                title=TestData.PERSONAL_EVENT_NAME,
                date=TestData.date()
            ))
        assert response.json().get('data') is None, "Событие создано без времени"


@allure.feature("API тесты")
@allure.story("Личные события")
@allure.title("Редактирование события с изменением всех полей")
@pytest.mark.api
@pytest.mark.positive
def test_edit_event(authorized_api_client, create_personal_event):
    with allure.step("Получение id события"):
        created_event = create_personal_event.get('data')
        event_id = created_event.get('payload').get('id')
        event_old_start_at = created_event.get('startAt')

        assert event_id is not None, "ID события отсутствует"

        created_event = create_personal_event.get('data')
        logger.debug(f"Созданное событие: {created_event}")

    with allure.step("Редактирование события с изменением всех полей"):
        test_data = TestData.get_personal_event_by_id(
            title=f"Редактирование_{TestData.PERSONAL_EVENT_NAME}",
            event_id=event_id,
            date=TestData.date(),
            start_at="15:00",
            end_at="17:00",
            background_color="#FDF2EB",
            color="#B65843",
            description="Обновленное описание",
            old_start_at=event_old_start_at

        )
        logger.debug(f"Тестовые данные для изменений: {test_data}")

        response = authorized_api_client.post("/updatePersonal", data=test_data)
        response_data = response.json()
        response_payload = response_data.get('data').get('payload').get('payload')
        logger.debug(f'{response_data}, {response_payload}')

        assert response.status_code == 200
        assert response_payload.get('backgroundColor') == "#FDF2EB"
        assert response_payload.get('color') == "#B65843"
        assert response_payload.get('description') == "Обновленное описание"
        assert response_payload.get('title') == test_data['title']


@allure.feature("API тесты")
@allure.story("Личные события")
@allure.title("Удаление личного события")
@pytest.mark.api
@pytest.mark.positive
def test_delete_event(authorized_api_client, create_personal_event):
    with allure.step("Получение id события"):
        event_id = create_personal_event.get('data').get('payload').get('id')

        assert event_id is not None

    with allure.step("Удаление личного события"):
        response = authorized_api_client.post(
            "/removePersonal",
            data={
                'id': event_id,
                'start_at': f"{TestData.date()}T{TestData.PERSONAL_EVENT_START_TIME}:00+03:00"
            })
        assert response.status_code == 200
