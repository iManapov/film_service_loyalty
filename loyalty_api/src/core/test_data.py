from pydantic import BaseSettings


class TestData(BaseSettings):
    """Test data class"""

    user_subs: dict = {
        '6de44714-b38c-4467-9b0b-925a769bfde8': {
            "is_trial_used": True,
            "subscription_until": '2023-02-20'
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

    films: dict = {
        '6de44714-b38c-4467-9b0b-925a769bfde8': {
            "title": "Star Tours",
            "imdb_rating": 8.0,
            "price": 977.75,
            "description": "Groups of visitors are taken on \"Star Tours\", a space tour bus set in the Star Wars universe. Thanks to an inexperienced and thoroughly incompetent robot pilot, what is billed as a leisurely tour to the Endor Moon becomes a wild ride as the tour gets caught up in a battle between the Empire and the rebels.",
            "genre": [],
            "actors": [],
            "writers": [],
            "director": ["Dennis Muren"],
        },
        '6de44714-b38c-4467-9b0b-925a769bfde9': {
            "title": "Star Tours",
            "imdb_rating": 8.0,
            "price": 977.75,
            "description": "Groups of visitors are taken on \"Star Tours\", a space tour bus set in the Star Wars universe. Thanks to an inexperienced and thoroughly incompetent robot pilot, what is billed as a leisurely tour to the Endor Moon becomes a wild ride as the tour gets caught up in a battle between the Empire and the rebels.",
            "genre": [],
            "actors": [],
            "writers": [],
            "director": ["Dennis Muren"],
            "tag": "fantastic"
        }
    }


test_data = TestData()
