from pydantic import BaseSettings


class TestData(BaseSettings):
    """Класс тестовых данных"""

    # Лист тестовых пользователей user_id: {}
    user_subs: dict = {
        '6de44714-b38c-4467-9b0b-925a769bfde8': {
            "is_trial_used": True,
            "subscription_until": '2023-02-31'
        },
        '6de44714-b38c-4467-9b0b-925a769bfde9': {
            "is_trial_used": False,
            "subscription_until": '2023-01-31'
        },
        '6de44714-b38c-4467-9b0b-925a769bfde7': {
            "is_trial_used": False,
            "subscription_until": '2023-01-31'
        },
    }


test_data = TestData()
