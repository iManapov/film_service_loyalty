from dataclasses import dataclass

from fastapi import Query, Path
from pydantic import Required


@dataclass
class Params:
    """
    Класс параметров запроса API
    """

    user_id: Query = Query(
        default=Required,
        title="Id пользователя"
    )

    price: Query = Query(
        default=Required,
        title="Цена фильма/подписки",
        ge=0
    )

    promo_code: Query = Query(
        default=Required,
        title="Код промокода"
    )

    promo_id: Path = Path(
        default=Required,
        title="UUID промокода"
    )

    subs_id: Path = Path(
        default=Required,
        title="UUID подписки"
    )

    film_tag: Query = Query(
        default=Required,
        title="Тэг фильма"
    )


params = Params()
