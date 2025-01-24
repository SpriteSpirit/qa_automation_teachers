import os
import uuid
import pytz

from src.utils.logger_utils import logger

from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

load_dotenv()


class TestData:
    """
    Перечисляемые значения для тестирования
    """

    VALID_EMAIL = os.getenv("SKYENG_EMAIL")
    VALID_PASSWORD = os.getenv("SKYENG_PASSWORD")

    INVALID_EMAIL = "test@skyeng.ru"
    INVALID_PASSWORD = "testTEST"

    PERSONAL_EVENT_NAME = f"_{str(uuid.uuid4())[:8]}"
    PERSONAL_EVENT_DESCRIPTION = "Описание события"
    PERSONAL_EVENT_START_TIME = '11:00'
    PERSONAL_EVENT_END_TIME = '11:30'

    @classmethod
    def date(cls):
        """
        Возвращает завтрашнюю дату с учетом смещения часового пояса на -4 часа
        """
        local_tz = pytz.timezone("Europe/Moscow")
        now_utc = datetime.now(timezone.utc)
        local_time = now_utc.astimezone(local_tz)
        tomorrow = local_time + timedelta(days=1)

        logger.debug(f"Текущее UTC время: {now_utc.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.debug(f"Локальное время ({local_tz}): {local_time.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.debug(f"Завтрашняя дата ({local_tz}): {tomorrow.strftime('%Y-%m-%d')}")

        return tomorrow.strftime("%Y-%m-%d")

    @classmethod
    def get_personal_event(cls, background_color: str = "#EBFDF2", color: str = "#43B658", description: str = "",
                           title: str = "", date: str = "", start_at: str = "", end_at: str = ""):
        """
        Генерация события
        """
        return {
            "backgroundColor": background_color,
            "color": color,
            "description": description,
            "title": title,
            "startAt": f"{date}T{start_at}:00+03:00",
            "endAt": f"{date}T{end_at}:00+03:00"
        }

    @classmethod
    def get_personal_event_by_id(cls,
                                 background_color: str = "#EBFDF2",
                                 color: str = "#43B658",
                                 description: str = "",
                                 title: str = "",
                                 event_id: int = None,
                                 date: str = "",
                                 start_at: str = "",
                                 end_at: str = "",
                                 is_edit: bool = True,
                                 old_start_at: str = ""):
        """
        Генерация события c id для изменения или для удаления события

        is_edit : bool = True - вернет значения для редактирования события
        is_edit : bool = False - вернет значения для удаления события
        old_start_at : str = "" - для редактирования, необходимо передать старое время начала события
        """

        if is_edit:
            return {
                "backgroundColor": background_color,
                "color": color,
                "description": description,
                "title": title,
                "id": event_id,
                "startAt": f"{date}T{start_at}:00+03:00",
                "endAt": f"{date}T{end_at}:00+03:00",
                "oldStartAt": datetime.fromisoformat(old_start_at)
                .astimezone(timezone(timedelta(hours=3)))
                .isoformat()
            }
        return {
            "backgroundColor": background_color,
            "color": color,
            "description": description,
            "title": title,
            "id": event_id,
            "startAt": f"{date}T{start_at}:00+03:00",
            "endAt": f"{date}T{end_at}:00+03:00"
        }
