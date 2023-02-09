import databases
import pytest

from databases import Database

from functional.testdata.discount_data import pg_discount_sub_data, pg_discount_film_data
from src.models.discount import SubsDiscount, FilmsDiscount
from src.models.promo_code import PromoCode
from src.models.subscription import Subscription
from tests.functional.testdata.promo_data import pg_promo_data
from tests.functional.testdata.subscription_data import pg_sub_data

from tests.functional.settings import test_settings


@pytest.fixture(scope="session")
async def postgres_client():
    """
    Фикстура для установления соединения с postgresql
    на время тестов
    """
    postgres_url = test_settings.get_postgres_url()
    postgres_client = databases.Database(postgres_url)
    await postgres_client.connect()
    yield postgres_client
    await postgres_client.disconnect()


@pytest.fixture(autouse=True, scope="session")
async def postgres_clear_data(postgres_client: Database):
    """
    Фикстура для удаления записей в таблицах перед началом тестов.
    """
    query = PromoCode.delete()
    await postgres_client.execute(query)

    query = Subscription.delete()
    await postgres_client.execute(query)

    query = SubsDiscount.delete()
    await postgres_client.execute(query)

    query = FilmsDiscount.delete()
    await postgres_client.execute(query)


@pytest.fixture(autouse=True, scope="session")
async def postgres_write_data(postgres_client: Database):
    """
    Фикстура для записи тестовых данных после удаления.
    """
    for each_promo in pg_promo_data:
        query = PromoCode.insert().values(**each_promo)
        await postgres_client.execute(query)

    for each_sub in pg_sub_data:
        query = Subscription.insert().values(**each_sub)
        await postgres_client.execute(query)

    for each_discount in pg_discount_sub_data:
        query = SubsDiscount.insert().values(**each_discount)
        await postgres_client.execute(query)

    for each_discount in pg_discount_film_data:
        query = FilmsDiscount.insert().values(**each_discount)
        await postgres_client.execute(query)
